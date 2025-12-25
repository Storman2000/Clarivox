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
