"""
conftest.py
Pytest fixtures for Clarivox tests.
"""

import os
import pytest
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """Create test client for FastAPI app."""
    return TestClient(app)


@pytest.fixture
def sample_audio_path():
    """Path to sample audio file for testing."""
    test_assets = Path(__file__).parent / "assets"
    sample_path = test_assets / "sample_voicemail.mp3"
    return sample_path


@pytest.fixture
def mock_transcript():
    """Sample transcript for testing."""
    return "Hi, this is John calling about my medication refill. I need a refill on my lisinopril. Please call me back at 555-123-4567."


@pytest.fixture
def mock_intent_result():
    """Mock intent extraction result."""
    return {
        "primary_intent": "medication_refill",
        "secondary_intents": [],
        "urgency": "routine",
        "intent_confidence": 0.9,
        "medications": [{"text": "lisinopril", "confidence": 0.9}],
        "symptoms": [],
        "crisis_indicators": []
    }
