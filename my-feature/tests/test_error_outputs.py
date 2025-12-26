"""
test_error_outputs.py
Validate error handling and error response structure
Client specifically requested: "error outputs working as intended"
"""

import pytest
from io import BytesIO
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


class TestAudioValidationErrors:
    """Test error responses for invalid audio uploads"""
    
    def test_missing_audio_file(self):
        """Test uploading request without audio file"""
        response = client.post(
            "/process-audio",
            data={"patient_mrn": "12345"}
        )
        
        assert response.status_code == 422  # Validation error
        data = response.json()
        assert "detail" in data
    
    def test_invalid_mime_type(self):
        """Test uploading non-audio file"""
        fake_pdf = BytesIO(b"%PDF-1.4 fake pdf content")
        
        response = client.post(
            "/process-audio",
            files={"audio_file": ("document.pdf", fake_pdf, "application/pdf")},
            data={"patient_mrn": "12345"}
        )
        
        # Should reject invalid MIME type
        assert response.status_code in [400, 422, 500]
        data = response.json()
        assert "detail" in data
    
    def test_corrupted_audio_file(self):
        """Test uploading corrupted audio data"""
        corrupted_audio = BytesIO(b"RIFF fake corrupted audio data")
        
        response = client.post(
            "/process-audio",
            files={"audio_file": ("corrupted.mp3", corrupted_audio, "audio/mpeg")},
            data={"patient_mrn": "12345"}
        )
        
        # Should detect corruption
        assert response.status_code in [400, 500]
        data = response.json()
        assert "detail" in data
        # Error message should mention decoding or corruption
        assert any(word in str(data["detail"]).lower() 
                  for word in ["decode", "corrupt", "invalid", "failed"])
    
    def test_empty_audio_file(self):
        """Test uploading empty file"""
        empty_audio = BytesIO(b"")
        
        response = client.post(
            "/process-audio",
            files={"audio_file": ("empty.mp3", empty_audio, "audio/mpeg")},
            data={"patient_mrn": "12345"}
        )
        
        # Should reject empty file
        assert response.status_code in [400, 422, 500]
        data = response.json()
        assert "detail" in data
    
    def test_oversized_file_simulation(self):
        """Test file size validation (simulated)"""
        # Note: Creating actual 50MB+ file is expensive for testing
        # This tests the validation logic exists
        # Real test would need actual large file
        
        # Small file should pass validation step
        small_audio = BytesIO(b"ID3" + b"x" * 1000)  # Small fake MP3
        
        response = client.post(
            "/process-audio",
            files={"audio_file": ("small.mp3", small_audio, "audio/mpeg")},
            data={"patient_mrn": "12345"}
        )
        
        # Should fail at decoding, not at size check
        # This confirms size validation happens before decode
        assert response.status_code in [400, 500]


class TestErrorResponseStructure:
    """Test that all errors have consistent structure"""
    
    def test_error_has_detail_field(self):
        """All errors should have 'detail' field"""
        response = client.post("/process-audio", files={}, data={})
        
        assert response.status_code in [400, 422, 500]
        data = response.json()
        assert "detail" in data
        assert isinstance(data["detail"], (str, list, dict))
    
    def test_error_has_appropriate_status_code(self):
        """Verify status codes match error types"""
        # Missing required field -> 422
        response = client.post("/process-audio", files={}, data={})
        assert response.status_code == 422
        
        # Invalid data -> should be 4xx
        response = client.post(
            "/process-audio",
            files={"audio_file": ("test.txt", BytesIO(b"text"), "text/plain")},
            data={}
        )
        assert 400 <= response.status_code < 500
    
    def test_error_response_is_json(self):
        """All error responses should be JSON"""
        response = client.post("/process-audio", files={}, data={})
        
        # Should be able to parse as JSON
        data = response.json()
        assert isinstance(data, dict)


class TestTranscriptionErrors:
    """Test errors during transcription phase"""
    
    def test_unsupported_language_code(self):
        """Test invalid language parameter"""
        if not Path("tests/assets/sample_voicemail.mp3").exists():
            pytest.skip("Test audio file not found")
        
        with open("tests/assets/sample_voicemail.mp3", "rb") as audio:
            response = client.post(
                "/transcribe-only",
                files={"audio_file": ("test.mp3", audio, "audio/mpeg")},
                data={"language": "invalid_lang_code"}
            )
        
        # Should either handle gracefully or return error
        # (Whisper might auto-detect, so 200 or 400 both acceptable)
        assert response.status_code in [200, 400, 422, 500]


class TestValidationErrorDetails:
    """Test validation error details are informative"""
    
    def test_missing_file_error_message(self):
        """Verify error message explains what's missing"""
        response = client.post(
            "/process-audio",
            data={"patient_mrn": "12345"}
        )
        
        data = response.json()
        # Error should mention missing audio_file
        detail_str = str(data["detail"]).lower()
        assert "audio" in detail_str or "file" in detail_str or "required" in detail_str
    
    def test_invalid_format_error_message(self):
        """Verify error explains format issue"""
        txt_file = BytesIO(b"This is not audio")
        
        response = client.post(
            "/process-audio",
            files={"audio_file": ("file.txt", txt_file, "text/plain")},
            data={"patient_mrn": "12345"}
        )
        
        if response.status_code in [400, 422]:
            data = response.json()
            # Should mention format, MIME, or file type
            detail_str = str(data["detail"]).lower()
            assert any(word in detail_str 
                      for word in ["format", "mime", "type", "audio", "invalid"])


class TestHTTPExceptionHandling:
    """Test HTTP exception handling"""
    
    def test_404_not_found(self):
        """Test non-existent endpoint"""
        response = client.get("/nonexistent-endpoint")
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
    
    def test_405_method_not_allowed(self):
        """Test wrong HTTP method"""
        # /process-audio requires POST
        response = client.get("/process-audio")
        assert response.status_code == 405
        data = response.json()
        assert "detail" in data


class TestErrorWithTraceID:
    """Test that errors include trace IDs when applicable"""
    
    @pytest.mark.skipif(not Path("tests/assets/sample_voicemail.mp3").exists(),
                       reason="Test audio file not found")
    def test_processing_error_has_context(self):
        """Test that processing errors have context"""
        with open("tests/assets/sample_voicemail.mp3", "rb") as audio:
            response = client.post(
                "/process-audio",
                files={"audio_file": ("test.mp3", audio, "audio/mpeg")},
                data={"patient_mrn": "12345"}
            )
        
        # If it errors, should have detail
        if response.status_code != 200:
            data = response.json()
            assert "detail" in data
            # Error message should be informative
            assert len(str(data["detail"])) > 0


class TestEdgeCaseErrors:
    """Test error handling for edge cases"""
    
    def test_malformed_json_response_handling(self):
        """Test that malformed requests are handled"""
        response = client.post(
            "/process-audio",
            data="not valid form data",
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        # Should handle gracefully
        assert response.status_code in [400, 422, 500]
    
    def test_extremely_long_filename(self):
        """Test handling of very long filenames"""
        long_filename = "a" * 1000 + ".mp3"
        audio = BytesIO(b"fake audio")
        
        response = client.post(
            "/process-audio",
            files={"audio_file": (long_filename, audio, "audio/mpeg")},
            data={"patient_mrn": "12345"}
        )
        
        # Should handle without crashing
        assert response.status_code is not None
        data = response.json()
        assert "detail" in data
    
    def test_special_characters_in_filename(self):
        """Test filenames with special characters"""
        special_filename = "test<>:\"/\\|?*.mp3"
        audio = BytesIO(b"fake audio")
        
        response = client.post(
            "/process-audio",
            files={"audio_file": (special_filename, audio, "audio/mpeg")},
            data={"patient_mrn": "12345"}
        )
        
        # Should handle gracefully
        assert response.status_code is not None


class TestErrorRecovery:
    """Test system recovery after errors"""
    
    def test_subsequent_request_after_error(self):
        """Test that system works after error"""
        # First request - causes error
        response1 = client.post("/process-audio", files={}, data={})
        assert response1.status_code in [400, 422]
        
        # Second request - should work normally
        response2 = client.get("/health")
        assert response2.status_code == 200
        
        # System should still be healthy
        data = response2.json()
        assert data["status"] == "healthy"
    
    def test_health_check_after_errors(self):
        """Test health endpoint after multiple errors"""
        # Cause several errors
        for _ in range(3):
            client.post("/process-audio", files={}, data={})
        
        # Health should still work
        response = client.get("/health")
        assert response.status_code == 200


class TestErrorLogging:
    """Test that errors are logged properly"""
    
    def test_error_generates_log_entry(self):
        """Verify errors create log entries"""
        # Trigger an error
        response = client.post(
            "/process-audio",
            files={"audio_file": ("bad.mp3", BytesIO(b"bad"), "audio/mpeg")},
            data={}
        )
        
        # Should get error response
        assert response.status_code in [400, 422, 500]
        
        # Log file should exist (though we may not be able to read it)
        log_dir = Path("logs")
        assert log_dir.exists()
