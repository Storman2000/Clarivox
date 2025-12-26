# Clarivox MVP - Implementation Documentation

## Project Overview

Clarivox is a healthcare voicemail processing system that automates the handling of patient voicemails through speech-to-text transcription, clinical intent extraction, and FHIR resource generation.

---

## Implementation Summary

### What Was Built

A complete FastAPI-based backend with 16 core modules:

| Module | Purpose |
|--------|---------|
| `main.py` | FastAPI entrypoint with all routes |
| `config.py` | Environment configuration loader |
| `audio_validator.py` | Audio validation (MIME, size, duration, format) |
| `transcriber_service.py` | Whisper ASR integration |
| `pii_sanitizer.py` | PII/PHI redaction from transcripts |
| `intent_extractor.py` | Clinical intent extraction using spaCy NLP |
| `fhir_generator.py` | FHIR R4 resource generation |
| `router.py` | Intent-based routing logic |
| `mock_services.py` | Mock Cerner/VistA/REACH VET services |
| `trace_logger.py` | Logging with trace IDs |
| `error_handler.py` | Custom exception handling |
| `metrics.py` | CloudWatch/Prometheus metrics |
| `background_tasks.py` | Async cleanup and logging tasks |
| `diarization_utils.py` | Speaker diarization (placeholder) |
| `language_detector.py` | Language detection (EN/ES) |

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/process-audio` | POST | Full pipeline: transcribe → extract intent → generate FHIR |
| `/transcribe-only` | POST | Transcription only |
| `/audio-formats` | GET | Supported audio formats info |
| `/health` | GET | General health check |
| `/health/transcriber` | GET | Transcriber service health |

---

## Directory Structure

```
clarivox/
├── app/                    # All 16 Python modules
├── tests/                  # 5 test files + conftest
├── data/                   # Sample audio files
├── .env                    # Configuration
├── requirements.txt        # Dependencies
├── README.md               # Documentation
└── run.sh                  # Launch script
```

---

## What Was Removed

Redundant folders that were not needed for the MVP:

- `fhir-server-main/` (Java FHIR server)
- `hapi-fhir-jpaserver-starter-master/` (Java)
- `node_modules/` (Node.js packages)
- `backend/` (Duplicate code)
- `clarivox/` (Duplicate code)
- `clarivox-main/` (Duplicate code)
- `utils/` (Old stubs)
- `package.json`, `package-lock.json`, `pnpm-lock.yaml` (Node.js)

---

## Configuration

### Environment Variables (.env)

```
WHISPER_MODEL_SIZE=base
DEBUG=True
MAX_AUDIO_FILE_SIZE_MB=50
MIN_AUDIO_DURATION_SEC=1.0
MAX_AUDIO_DURATION_SEC=600.0
SANITIZE_PII=true
```

### Dependencies (requirements.txt)

```
fastapi, uvicorn, pydantic, python-dotenv, pydub
faster-whisper, langdetect, transformers, torch, spacy
fhir.resources, boto3, pytest, httpx, python-multipart
```

---

## How to Run

```bash
# Install dependencies
uv pip install -r requirements.txt
uv pip install en-core-web-sm@<spacy-model-url>
uv pip install python-multipart

# Start server
uv run uvicorn app.main:app --reload

# Access API docs
http://127.0.0.1:8000/docs
```

---

## Testing

```bash
# Run all tests
uv run pytest tests/ -v

# Run specific tests
uv run pytest tests/test_intent_extractor.py -v
```

---

## Intent Types Supported

- `medication_refill` - Prescription refill requests
- `appointment_schedule` - New appointment booking
- `appointment_reschedule` - Appointment changes
- `appointment_cancel` - Appointment cancellation
- `symptom_report` - Symptom reporting
- `test_results` - Lab/test result inquiries
- `callback_request` - General callback requests
- `crisis_suicide` - Crisis detection (emergency routing)

---

## FHIR Resources Generated

- **CommunicationRequest** - For callbacks and communications
- **Task** - For follow-up items
- **MedicationRequest** - For prescription refills
- **Observation** - For symptom reports

---

## Milestone Status

| Task | Status |
|------|--------|
| Repository organized | ✅ Complete |
| All modules implemented | ✅ Complete |
| Import paths fixed | ✅ Complete |
| `__init__.py` files added | ✅ Complete |
| No circular imports | ✅ Complete |
| FastAPI server starts | ✅ Complete |
| `/docs` loads successfully | ✅ Complete |
| All routes visible | ✅ Complete |
