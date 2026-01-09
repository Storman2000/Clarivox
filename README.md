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

- Python 3.9+ (3.10 or 3.11 recommended)
- FFmpeg (for audio processing)
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

### Installation

#### Step 1: Install FFmpeg

**macOS:**

```bash
brew install ffmpeg
```

**Windows:**
Download from https://ffmpeg.org/download.html and add to PATH

**Linux (Ubuntu/Debian):**

```bash
sudo apt update && sudo apt install ffmpeg
```

#### Step 2: Install uv (Recommended)

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### Step 3: Set Up Project

**Using uv (Recommended):**

```bash
cd clarivox

# Sync all dependencies (creates .venv automatically, includes spaCy model)
uv sync

# Copy environment config
cp .env.example .env  # Windows: copy .env.example .env
```

**Using pip (Alternative):**

```bash
cd clarivox

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies (including spaCy model)
pip install --upgrade pip
pip install -e . --find-links https://github.com/explosion/spacy-models/releases/expanded_assets/en_core_web_sm-3.8.0

# Copy environment config
cp .env.example .env
```

### Running the Server

```bash
# With uv (no need to activate venv)
uv run uvicorn app.main:app --reload --port 8000

# With pip (after activating venv)
uvicorn app.main:app --reload --port 8000
```

Access the API documentation at: http://localhost:8000/docs

---

## Troubleshooting

### macOS: Python Command Not Found

If `python3.9` is not found but `python3` works:

```bash
# Just use python3 instead
python3 -m venv venv
source venv/bin/activate
```

### macOS: blis/spacy Build Errors

If you get compilation errors for `blis` or `spacy`:

```bash
# Install Xcode command line tools first
xcode-select --install

# Install with binary wheels only (avoid compilation)
pip install --prefer-binary spacy

# If still failing, try installing spacy separately first
pip install spacy==3.8.4 --prefer-binary
pip install -r requirements.txt
```

### macOS M1/M2 (Apple Silicon): Additional Steps

```bash
# Ensure you're using ARM-native Python
python3 -c "import platform; print(platform.machine())"
# Should output: arm64

# If having issues, install with Rosetta compatibility
arch -x86_64 pip install -r requirements.txt
```

### Missing Module Errors (fastapi, uvicorn, etc.)

This usually means the virtual environment isn't activated or the install failed:

```bash
# Verify venv is activated (should show (venv) in prompt)
which python  # Should point to venv/bin/python

# Reinstall everything
pip install --no-cache-dir -r requirements.txt

# Verify installation
pip list | grep fastapi
pip list | grep uvicorn
```

### FFmpeg Not Found

If you get FFmpeg-related errors at startup:

```bash
# Verify FFmpeg is installed
ffmpeg -version

# If not found, install it (see Step 1 above)
```

## API Endpoints

| Endpoint              | Method | Description                                              |
| --------------------- | ------ | -------------------------------------------------------- |
| `/process-audio`      | POST   | Full pipeline: transcribe, extract intent, generate FHIR |
| `/transcribe-only`    | POST   | Transcription only                                       |
| `/audio-formats`      | GET    | Supported audio formats and configuration                |
| `/health`             | GET    | General health check                                     |
| `/health/transcriber` | GET    | Transcriber service health                               |

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

| Variable                 | Default | Description                                           |
| ------------------------ | ------- | ----------------------------------------------------- |
| `WHISPER_MODEL_SIZE`     | base    | Whisper model size (tiny, base, small, medium, large) |
| `MAX_AUDIO_FILE_SIZE_MB` | 50      | Maximum audio file size                               |
| `MIN_AUDIO_DURATION_SEC` | 1.0     | Minimum audio duration                                |
| `MAX_AUDIO_DURATION_SEC` | 600.0   | Maximum audio duration                                |
| `SANITIZE_PII`           | true    | Enable PII sanitization                               |

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

| Intent                   | Description                            |
| ------------------------ | -------------------------------------- |
| `medication_refill`      | Patient requesting prescription refill |
| `appointment_schedule`   | Scheduling new appointment             |
| `appointment_reschedule` | Changing existing appointment          |
| `symptom_report`         | Reporting symptoms                     |
| `test_results`           | Inquiring about test results           |
| `callback_request`       | General callback request               |
| `crisis_suicide`         | Crisis detection (emergency routing)   |

## FHIR Resources Generated

- **CommunicationRequest** - For callback and communication needs
- **Task** - For follow-up items
- **MedicationRequest** - For prescription refills
- **Observation** - For symptom reports

## License

Proprietary - All rights reserved.
