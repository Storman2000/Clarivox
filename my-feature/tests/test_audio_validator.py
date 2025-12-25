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
