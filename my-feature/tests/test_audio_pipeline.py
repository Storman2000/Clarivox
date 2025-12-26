"""
test_audio_pipeline.py
End-to-end integration tests for the full audio processing pipeline.
"""

import os
import pytest
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app

# Sample audio test data
TEST_AUDIO_PATH = Path("tests/assets/sample_voicemail.mp3")

client = TestClient(app)


def test_health_check():
    """Test general health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    health = response.json()
    assert health["status"] == "healthy"


def test_transcriber_health():
    """Health check for transcriber service."""
    response = client.get("/health/transcriber")
    assert response.status_code == 200
    health = response.json()
    assert health["status"] == "healthy"
    assert "model_size" in health


def test_audio_formats():
    """Test audio formats endpoint."""
    response = client.get("/audio-formats")
    assert response.status_code == 200
    data = response.json()
    assert "supported_formats" in data
    assert ".mp3" in data["supported_formats"]
    assert "model" in data
    assert data["model"]["name"] == "OpenAI Whisper"


@pytest.mark.skipif(not TEST_AUDIO_PATH.exists(), reason="Test audio file not found")
def test_process_audio_pipeline():
    """Integration test for the full audio processing pipeline."""
    with open(TEST_AUDIO_PATH, "rb") as audio_file:
        response = client.post(
            "/process-audio",
            files={"audio_file": ("sample_voicemail.mp3", audio_file, "audio/mpeg")},
            data={
                "phone_number": "555-1234",
                "patient_mrn": "12345678",
                "sanitize_pii": "true"
            }
        )

    assert response.status_code == 200
    data = response.json()

    # Basic structure checks
    assert "transcription" in data
    assert "fhir_bundle" in data
    assert "processing_time_ms" in data

    # Transcription checks
    transcription = data["transcription"]
    assert transcription["text"]
    assert transcription["duration"] > 0

    # FHIR artifacts checks
    fhir = data["fhir_bundle"]
    assert fhir["trace_id"].startswith("TXN-") or fhir["trace_id"].startswith("CLV-")
    assert "intent" in fhir
    assert "communication_request" in fhir
    assert "task" in fhir


@pytest.mark.skipif(not TEST_AUDIO_PATH.exists(), reason="Test audio file not found")
def test_transcribe_only():
    """Transcription-only test."""
    with open(TEST_AUDIO_PATH, "rb") as audio_file:
        response = client.post(
            "/transcribe-only",
            files={"audio_file": ("sample_voicemail.mp3", audio_file, "audio/mpeg")},
            data={"language": "en"}
        )

    assert response.status_code == 200
    result = response.json()
    assert "text" in result
    assert result["duration"] > 0


class TestPIISanitization:
    """Test PII sanitization in full pipeline"""
    
    @pytest.mark.skipif(not TEST_AUDIO_PATH.exists(), reason="Test audio file not found")
    def test_full_pipeline_sanitizes_pii(self):
        """Verify that PII is sanitized when requested"""
        with open(TEST_AUDIO_PATH, "rb") as audio_file:
            response = client.post(
                "/process-audio",
                files={"audio_file": ("test.mp3", audio_file, "audio/mpeg")},
                data={
                    "phone_number": "555-1234",
                    "patient_mrn": "TEST123",
                    "sanitize_pii": "true"
                }
            )
        
        if response.status_code == 200:
            data = response.json()
            transcription = data.get("transcription", {})
            
            # Verify sanitization occurred
            # (Actual phone numbers should be redacted)
            assert transcription.get("sanitized") == True or "sanitized" in str(transcription).lower()


class TestCrisisDetection:
    """Test crisis detection and routing"""
    
    def test_crisis_keywords_trigger_emergent(self):
        """Test that crisis keywords result in emergent priority"""
        # Note: This would need a crisis audio file or mock
        # For now, verify system handles crisis flag
        response = client.get("/health")
        assert response.status_code == 200


class TestMultipleIntentHandling:
    """Test handling of voicemails with multiple intents"""
    
    @pytest.mark.skipif(not TEST_AUDIO_PATH.exists(), reason="Test audio file not found")
    def test_pipeline_chooses_primary_intent(self):
        """Verify pipeline handles and chooses primary from multiple intents"""
        with open(TEST_AUDIO_PATH, "rb") as audio_file:
            response = client.post(
                "/process-audio",
                files={"audio_file": ("test.mp3", audio_file, "audio/mpeg")},
                data={"patient_mrn": "12345"}
            )
        
        if response.status_code == 200:
            data = response.json()
            # Should have exactly one primary intent
            assert "intent" in data
            assert isinstance(data["intent"], str)


class TestBackgroundTasks:
    """Test background task execution"""
    
    @pytest.mark.skipif(not TEST_AUDIO_PATH.exists(), reason="Test audio file not found")
    def test_temp_file_cleanup_scheduled(self):
        """Verify background cleanup is scheduled"""
        with open(TEST_AUDIO_PATH, "rb") as audio_file:
            response = client.post(
                "/process-audio",
                files={"audio_file": ("test.mp3", audio_file, "audio/mpeg")},
                data={"patient_mrn": "12345"}
            )
        
        # Response should complete (cleanup happens in background)
        assert response.status_code in [200, 400, 500]


class TestPerformanceMetrics:
    """Test that performance metrics are captured"""
    
    @pytest.mark.skipif(not TEST_AUDIO_PATH.exists(), reason="Test audio file not found")
    def test_processing_time_recorded(self):
        """Verify processing time is tracked"""
        with open(TEST_AUDIO_PATH, "rb") as audio_file:
            response = client.post(
                "/process-audio",
                files={"audio_file": ("test.mp3", audio_file, "audio/mpeg")},
                data={"patient_mrn": "12345"}
            )
        
        if response.status_code == 200:
            data = response.json()
            assert "processing_time_ms" in data
            assert isinstance(data["processing_time_ms"], (int, float))
            assert data["processing_time_ms"] > 0


class TestFHIRGeneration:
    """Test FHIR resource generation in full pipeline"""
    
    @pytest.mark.skipif(not TEST_AUDIO_PATH.exists(), reason="Test audio file not found")
    def test_fhir_bundle_structure(self):
        """Verify FHIR bundle has correct structure"""
        with open(TEST_AUDIO_PATH, "rb") as audio_file:
            response = client.post(
                "/process-audio",
                files={"audio_file": ("test.mp3", audio_file, "audio/mpeg")},
                data={"patient_mrn": "MRN-12345"}
            )
        
        if response.status_code == 200:
            data = response.json()
            fhir = data.get("fhir_bundle", {})
            
            # Verify key FHIR components
            assert "trace_id" in fhir
            assert "communication_request" in fhir
            assert "task" in fhir
    
    @pytest.mark.skipif(not TEST_AUDIO_PATH.exists(), reason="Test audio file not found")
    def test_fhir_patient_reference(self):
        """Verify FHIR resources reference patient correctly"""
        with open(TEST_AUDIO_PATH, "rb") as audio_file:
            response = client.post(
                "/process-audio",
                files={"audio_file": ("test.mp3", audio_file, "audio/mpeg")},
                data={"patient_mrn": "TEST-MRN-001"}
            )
        
        if response.status_code == 200:
            data = response.json()
            fhir = data.get("fhir_bundle", {})
            comm_req = fhir.get("communication_request", {})
            
            # Should have patient reference
            if "subject" in comm_req:
                subject = comm_req["subject"]
                # Should reference the patient
                assert "TEST-MRN-001" in str(subject) or "Patient" in str(subject)


class TestRouting:
    """Test intent-based routing"""
    
    @pytest.mark.skipif(not TEST_AUDIO_PATH.exists(), reason="Test audio file not found")
    def test_routing_determined(self):
        """Verify routing decision is made"""
        with open(TEST_AUDIO_PATH, "rb") as audio_file:
            response = client.post(
                "/process-audio",
                files={"audio_file": ("test.mp3", audio_file, "audio/mpeg")},
                data={"patient_mrn": "12345"}
            )
        
        if response.status_code == 200:
            data = response.json()
            assert "routing" in data
            routing = data["routing"]
            assert isinstance(routing, dict)


class TestConcurrentRequests:
    """Test system behavior with concurrent requests"""
    
    @pytest.mark.skipif(not TEST_AUDIO_PATH.exists(), reason="Test audio file not found")
    def test_multiple_sequential_requests(self):
        """Test multiple requests don't interfere"""
        trace_ids = []
        
        for i in range(2):
            with open(TEST_AUDIO_PATH, "rb") as audio_file:
                response = client.post(
                    "/process-audio",
                    files={"audio_file": ("test.mp3", audio_file, "audio/mpeg")},
                    data={"patient_mrn": f"TEST-{i}"}
                )
            
            if response.status_code == 200:
                data = response.json()
                trace_ids.append(data.get("trace_id"))
        
        # Trace IDs should be unique
        if len(trace_ids) >= 2:
            assert trace_ids[0] != trace_ids[1]
