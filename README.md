# Clarivox

Healthcare Voicemail Processing System with Speech-to-Text, Intent Extraction, and FHIR Generation.

## Overview

Clarivox is an automated voicemail processing pipeline for healthcare settings. It:
1. **Transcribes** audio voicemails using OpenAI Whisper
2. **Sanitizes** PII/PHI from transcripts
3. **Extracts** clinical intents, urgency levels, medications, and symptoms
4. **Generates** FHIR R4 compliant resources
5. **Routes** to appropriate backend systems (Cerner, VistA, REACH VET)

## Quick Start

### Prerequisites
- Python 3.9+
- FFmpeg (for audio processing)

### Installation

```bash
# Clone the repository
cd clarivox

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Copy environment config
cp .env.example .env  # Or use existing .env
```

### Running the Server

```bash
# Start the development server
uvicorn app.main:app --reload --port 8000
```

Access the API documentation at: http://localhost:8000/docs

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/process-audio` | POST | Full pipeline: transcribe, extract intent, generate FHIR |
| `/transcribe-only` | POST | Transcription only |
| `/audio-formats` | GET | Supported audio formats and configuration |
| `/health` | GET | General health check |
| `/health/transcriber` | GET | Transcriber service health |

## Project Structure

```
clarivox/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI entrypoint
│   ├── config.py               # Environment configuration
│   ├── audio_validator.py      # Audio validation (MIME, duration, size)
│   ├── transcriber_service.py  # Whisper ASR integration
│   ├── pii_sanitizer.py        # PII/PHI redaction
│   ├── intent_extractor.py     # NLP intent extraction
│   ├── fhir_generator.py       # FHIR resource generation
│   ├── router.py               # Intent-based routing
│   ├── mock_services.py        # Mock Cerner/VistA/REACH VET
│   ├── trace_logger.py         # Logging with trace IDs
│   ├── error_handler.py        # Custom exception handling
│   ├── metrics.py              # CloudWatch/Prometheus metrics
│   ├── background_tasks.py     # Async cleanup tasks
│   ├── language_detector.py    # Language detection
│   └── diarization_utils.py    # Speaker diarization (stub)
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # Pytest fixtures
│   ├── test_audio_pipeline.py  # E2E tests
│   ├── test_audio_validator.py # Unit tests
│   ├── test_intent_extractor.py
│   └── test_fhir_generator.py
├── data/                       # Sample audio files
├── .env                        # Environment configuration
├── requirements.txt            # Python dependencies
└── README.md
```

## Configuration

Key environment variables (see `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `WHISPER_MODEL_SIZE` | base | Whisper model size (tiny, base, small, medium, large) |
| `MAX_AUDIO_FILE_SIZE_MB` | 50 | Maximum audio file size |
| `MIN_AUDIO_DURATION_SEC` | 1.0 | Minimum audio duration |
| `MAX_AUDIO_DURATION_SEC` | 600.0 | Maximum audio duration |
| `SANITIZE_PII` | true | Enable PII sanitization |

## Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=app --cov-report=term-missing
```

## Supported Audio Formats

- MP3 (.mp3)
- WAV (.wav)
- M4A (.m4a)
- OGG (.ogg)
- FLAC (.flac)
- WebM (.webm)

## Intent Types

| Intent | Description |
|--------|-------------|
| `medication_refill` | Patient requesting prescription refill |
| `appointment_schedule` | Scheduling new appointment |
| `appointment_reschedule` | Changing existing appointment |
| `symptom_report` | Reporting symptoms |
| `test_results` | Inquiring about test results |
| `callback_request` | General callback request |
| `crisis_suicide` | Crisis detection (emergency routing) |

## FHIR Resources Generated

- **CommunicationRequest** - For callback and communication needs
- **Task** - For follow-up items
- **MedicationRequest** - For prescription refills
- **Observation** - For symptom reports

## License

Proprietary - All rights reserved.
