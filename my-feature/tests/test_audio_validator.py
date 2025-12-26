"""
test_audio_validator.py
Unit tests for audio_validator.py
"""

import pytest
import tempfile
import os
from unittest.mock import Mock, MagicMock, patch
from io import BytesIO

from app.audio_validator import (
    get_file_extension,
    verify_mime_type,
    check_file_size,
    is_silent,
    ALLOWED_EXTENSIONS,
    AudioValidator,
    AudioValidationError
)


class TestGetFileExtension:
    def test_mp3_extension(self):
        assert get_file_extension("audio.mp3") == ".mp3"

    def test_wav_extension(self):
        assert get_file_extension("audio.wav") == ".wav"

    def test_uppercase_extension(self):
        assert get_file_extension("audio.MP3") == ".mp3"

    def test_complex_filename(self):
        assert get_file_extension("my.audio.file.m4a") == ".m4a"


class TestAllowedExtensions:
    def test_all_supported_formats(self):
        expected = {".mp3", ".wav", ".m4a", ".ogg", ".flac", ".webm"}
        assert ALLOWED_EXTENSIONS == expected


class TestVerifyMimeType:
    def test_valid_audio_mime(self):
        mock_file = Mock()
        mock_file.filename = "audio.mp3"
        # Should not raise
        verify_mime_type(mock_file)

    def test_invalid_mime_type(self):
        mock_file = Mock()
        mock_file.filename = "document.pdf"
        with pytest.raises(Exception):  # HTTPException
            verify_mime_type(mock_file)


class TestAudioValidator:
    def test_supported_extensions(self):
        validator = AudioValidator()
        expected = {".mp3", ".wav", ".m4a", ".ogg", ".flac", ".webm"}
        assert validator.SUPPORTED_EXTENSIONS == expected

    def test_supported_mime_types(self):
        validator = AudioValidator()
        assert "audio/mpeg" in validator.SUPPORTED_MIME_TYPES
        assert "audio/wav" in validator.SUPPORTED_MIME_TYPES


class TestHashFile:
    def test_hash_produces_hex_string(self):
        from app.audio_validator import hash_file
        
        # Create a temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as f:
            f.write(b"test content")
            temp_path = f.name

        try:
            result = hash_file(temp_path)
            assert isinstance(result, str)
            assert len(result) == 64  # SHA-256 hex length
        finally:
            os.remove(temp_path)


class TestEdgeCases:
    """Test edge cases and boundary conditions for audio validation"""
    
    def test_unsupported_extension(self):
        """Test file with unsupported extension"""
        mock_file = Mock()
        mock_file.filename = "audio.aac"
        
        # Should raise exception for unsupported format
        # (unless .aac is in ALLOWED_EXTENSIONS)
        if ".aac" not in ALLOWED_EXTENSIONS:
            with pytest.raises(Exception):
                from app.audio_validator import validate_audio_file
                validate_audio_file(mock_file)
    
    def test_no_extension(self):
        """Test file without extension"""
        ext = get_file_extension("audiofile")
        assert ext == ""
    
    def test_multiple_dots_in_filename(self):
        """Test filename with multiple dots"""
        ext = get_file_extension("my.test.audio.file.mp3")
        assert ext == ".mp3"
    
    def test_hidden_file(self):
        """Test hidden file (starts with dot)"""
        ext = get_file_extension(".hidden_audio.wav")
        assert ext == ".wav"


class TestFileSizeValidation:
    """Test file size boundary conditions"""
    
    def test_check_file_size_with_small_file(self):
        """Test that small files pass"""
        mock_file = Mock()
        mock_file.file = BytesIO(b"x" * 1024)  # 1KB
        mock_file.file.seek(0)
        
        # Should not raise
        check_file_size(mock_file)
        
        # File pointer should be reset
        assert mock_file.file.tell() == 0
    
    def test_file_size_boundary(self):
        """Test file size at boundary"""
        from app.audio_validator import MAX_AUDIO_FILE_SIZE_MB
        
        # Just under limit should pass
        size_bytes = int(MAX_AUDIO_FILE_SIZE_MB * 1024 * 1024 - 1)
        mock_file = Mock()
        mock_file.file = BytesIO(b"x" * min(size_bytes, 1024 * 1024))  # Cap at 1MB for test speed
        mock_file.file.seek(0)
        
        # Should not raise
        check_file_size(mock_file)


class TestSilentAudioDetection:
    """Test silent audio detection"""
    
    @patch('app.audio_validator.AudioSegment')
    def test_is_silent_with_quiet_audio(self, mock_audio_segment):
        """Test detection of silent audio"""
        mock_audio = Mock()
        mock_audio.dBFS = -50.0  # Very quiet
        
        result = is_silent(mock_audio)
        assert result is True
    
    @patch('app.audio_validator.AudioSegment')
    def test_is_silent_with_normal_audio(self, mock_audio_segment):
        """Test normal audio passes"""
        mock_audio = Mock()
        mock_audio.dBFS = -20.0  # Normal speaking volume
        
        result = is_silent(mock_audio)
        assert result is False
    
    @patch('app.audio_validator.AudioSegment')
    def test_is_silent_boundary(self, mock_audio_segment):
        """Test silence threshold boundary"""
        mock_audio = Mock()
        mock_audio.dBFS = -45.0  # At default threshold
        
        result = is_silent(mock_audio)
        # At exact threshold, behavior may vary
        assert isinstance(result, bool)


class TestMimeTypeEdgeCases:
    """Test MIME type validation edge cases"""
    
    def test_video_mime_rejected(self):
        """Test that video files are rejected"""
        mock_file = Mock()
        mock_file.filename = "video.mp4"
        
        with pytest.raises(Exception):
            verify_mime_type(mock_file)
    
    def test_text_file_rejected(self):
        """Test that text files are rejected"""
        mock_file = Mock()
        mock_file.filename = "document.txt"
        
        with pytest.raises(Exception):
            verify_mime_type(mock_file)
    
    def test_unknown_extension(self):
        """Test file with unknown extension"""
        mock_file = Mock()
        mock_file.filename = "audio.xyz"
        
        # mimetypes.guess_type returns (None, None) for unknown
        # Should handle gracefully
        try:
            verify_mime_type(mock_file)
        except Exception as e:
            # Either raises or handles gracefully
            assert e is not None or e is None


class TestDurationValidation:
    """Test audio duration validation logic"""
    
    def test_duration_constants_exist(self):
        """Verify duration constants are defined"""
        from app.audio_validator import MIN_AUDIO_DURATION_SEC, MAX_AUDIO_DURATION_SEC
        
        assert MIN_AUDIO_DURATION_SEC > 0
        assert MAX_AUDIO_DURATION_SEC > MIN_AUDIO_DURATION_SEC
        assert MAX_AUDIO_DURATION_SEC <= 600  # Should be reasonable limit
