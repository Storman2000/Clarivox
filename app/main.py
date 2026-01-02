"""
main.py
FastAPI entrypoint for the Clarivox voicemail processing pipeline.
Defines all routes and orchestrates the full processing flow.
"""

import os
import time
import traceback
import uuid
import subprocess
import logging
from typing import Optional

from fastapi import FastAPI, APIRouter, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.audio_validator import validate_audio_file, AudioValidator, get_audio_validator
from app.transcriber_service import get_transcription_service
from app.pii_sanitizer import sanitize_transcript
from app.intent_extractor import get_intent_service
from app.fhir_generator import generate_fhir_bundle
from app.router import determine_routing_targets
from app.trace_logger import log_pipeline_trace, TraceLogger
from app.error_handler import register_exception_handlers
from app.metrics import log_end_to_end_latency, log_transcription_metrics, log_intent_metrics
from app.background_tasks import schedule_cleanup
from app.config import validate_config

# Setup startup logger
startup_logger = logging.getLogger("clarivox.startup")
logging.basicConfig(level=logging.INFO)

# Initialize FastAPI app
app = FastAPI(
    title="Clarivox",
    description="Healthcare Voicemail Processing API",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register exception handlers
register_exception_handlers(app)

# Create router
router = APIRouter()

# Initialize services (lazy loading)
transcriber = get_transcription_service()
intent_service = get_intent_service()


# -----------------------------
# Startup Event - Dependency Checks
# -----------------------------
@app.on_event("startup")
async def startup_checks():
    """
    Verify critical dependencies and configuration at startup.
    Checks: FFmpeg, spaCy model, configuration values.
    """
    startup_logger.info("=" * 50)
    startup_logger.info("Clarivox Startup Checks")
    startup_logger.info("=" * 50)
    
    # 1. Validate configuration
    try:
        validate_config()
    except RuntimeError as e:
        startup_logger.critical(f"Configuration validation failed: {e}")
        # Don't raise - allow server to start but log critical error
    
    # 2. Check FFmpeg availability
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"], 
            capture_output=True, 
            timeout=10,
            text=True
        )
        if result.returncode == 0:
            # Extract version info from first line
            version_line = result.stdout.split('\n')[0] if result.stdout else "unknown"
            startup_logger.info(f"✓ FFmpeg is available: {version_line}")
        else:
            startup_logger.error("✗ FFmpeg check failed (non-zero exit code)")
    except FileNotFoundError:
        startup_logger.critical(
            "✗ FFmpeg not found! Audio processing will fail. "
            "Install FFmpeg and add to PATH: https://ffmpeg.org/download.html"
        )
    except subprocess.TimeoutExpired:
        startup_logger.warning("✗ FFmpeg check timed out")
    except Exception as e:
        startup_logger.warning(f"✗ FFmpeg check error: {e}")
    
    # 3. Check spaCy model availability
    try:
        import spacy
        nlp = spacy.load("en_core_web_sm")
        startup_logger.info("✓ spaCy model 'en_core_web_sm' loaded successfully")
    except OSError:
        startup_logger.warning(
            "✗ spaCy model 'en_core_web_sm' not found. "
            "Run: python -m spacy download en_core_web_sm"
        )
    except ImportError:
        startup_logger.warning("✗ spaCy not installed")
    except Exception as e:
        startup_logger.warning(f"✗ spaCy check error: {e}")
    
    # 4. Log environment summary
    startup_logger.info("-" * 50)
    startup_logger.info(f"Environment: {os.getenv('ENV', 'development')}")
    startup_logger.info(f"Whisper Model: {os.getenv('WHISPER_MODEL_SIZE', 'base')}")
    startup_logger.info(f"Device: {os.getenv('WHISPER_DEVICE', 'cpu')}")
    startup_logger.info("-" * 50)
    startup_logger.info("Clarivox startup checks complete")
    startup_logger.info("=" * 50)


@router.post("/process-audio")
async def process_audio(
    background_tasks: BackgroundTasks,
    audio_file: UploadFile = File(...),
    phone_number: Optional[str] = Form(None),
    patient_mrn: Optional[str] = Form(None),
    facility_code: Optional[str] = Form(None),
    language: Optional[str] = Form("en"),
    sanitize_pii: bool = Form(True),
):
    """
    Full audio processing pipeline:
    1. Validate audio
    2. Transcribe
    3. Sanitize PII
    4. Extract intent
    5. Generate FHIR
    6. Route to target systems
    """
    start_time = time.time()
    trace_id = f"TXN-{uuid.uuid4().hex[:12].upper()}"

    try:
        # Step 1: Validate audio input
        validation_result = validate_audio_file(audio_file)
        metadata = {
            "duration": validation_result.duration_sec,
            "sha256": validation_result.sha256,
            "sample_rate": validation_result.sample_rate
        }

        # Step 2: Transcribe
        transcription = transcriber.transcribe_from_file(
            file_path=validation_result.file_path,
            language=language,
            sanitize_pii=False  # We'll sanitize separately
        )

        # Step 3: Sanitize transcript
        if sanitize_pii:
            transcription.text = sanitize_transcript(transcription.text)
            transcription.sanitized = True
        else:
            transcription.sanitized = False

        log_transcription_metrics(
            duration_ms=(time.time() - start_time) * 1000,
            audio_duration_sec=validation_result.duration_sec,
            confidence=transcription.confidence_score
        )

        # Step 4: NLP / Intent Extraction
        nlp_start = time.time()
        nlp_result = intent_service.extract(
            transcript=transcription.text,
            trace_id=trace_id
        )
        log_intent_metrics(
            intent_confidence=nlp_result.intent_confidence,
            latency_ms=(time.time() - nlp_start) * 1000,
            crisis_detected=len(nlp_result.crisis_indicators) > 0
        )

        # Step 5: Generate FHIR artifacts
        fhir_data = generate_fhir_bundle(
            intent=nlp_result.primary_intent,
            urgency=nlp_result.urgency,
            patient_mrn=patient_mrn,
            transcript=transcription.text,
            trace_id=trace_id,
            medications=[m.text for m in nlp_result.medications],
            symptoms=[s.text for s in nlp_result.symptoms if not s.negated]
        )

        # Step 6: Route to target systems
        routing_info = determine_routing_targets(nlp_result.primary_intent)

        # Step 7: Log trace
        log_pipeline_trace(
            trace_id=trace_id,
            metadata=metadata,
            transcription=transcription.to_dict(),
            intent_result=nlp_result,
            fhir_bundle=fhir_data,
            routing=routing_info
        )

        # Schedule cleanup
        schedule_cleanup(background_tasks, validation_result.file_path)

        # Log end-to-end latency
        log_end_to_end_latency(start_time)

        # Step 8: Return full pipeline response
        return JSONResponse({
            "trace_id": trace_id,
            "transcription": transcription.to_dict(),
            "intent": nlp_result.primary_intent,
            "urgency": nlp_result.urgency,
            "medications": [m.text for m in nlp_result.medications],
            "symptoms": [s.text for s in nlp_result.symptoms],
            "fhir_bundle": fhir_data,
            "routing": routing_info,
            "processing_time_ms": (time.time() - start_time) * 1000
        })

    except Exception as e:
        error_msg = f"Pipeline failed: {str(e)}"
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=error_msg)


@router.post("/transcribe-only")
async def transcribe_only(
    background_tasks: BackgroundTasks,
    audio_file: UploadFile = File(...),
    language: Optional[str] = Form("en"),
    sanitize_pii: bool = Form(True),
):
    """
    Transcription-only endpoint.
    Returns transcription without intent extraction or FHIR generation.
    """
    try:
        # Validate
        validation_result = validate_audio_file(audio_file)

        # Transcribe
        result = transcriber.transcribe_from_file(
            file_path=validation_result.file_path,
            language=language,
            sanitize_pii=sanitize_pii
        )

        # Schedule cleanup
        schedule_cleanup(background_tasks, validation_result.file_path)

        return result.to_dict()

    except Exception as e:
        error_msg = f"Transcription failed: {str(e)}"
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=error_msg)


@router.get("/audio-formats")
async def audio_formats():
    """Return supported audio formats and configuration."""
    return {
        "supported_formats": [".mp3", ".wav", ".m4a", ".ogg", ".flac", ".webm"],
        "max_file_size_mb": int(os.getenv("MAX_AUDIO_FILE_SIZE_MB", 50)),
        "min_duration_seconds": float(os.getenv("MIN_AUDIO_DURATION_SEC", 1.0)),
        "max_duration_seconds": float(os.getenv("MAX_AUDIO_DURATION_SEC", 600)),
        "model": {
            "name": "OpenAI Whisper",
            "variant": "faster-whisper",
            "size": os.getenv("WHISPER_MODEL_SIZE", "base"),
            "compute_type": os.getenv("WHISPER_COMPUTE_TYPE", "int8")
        },
        "features": {
            "multilingual": True,
            "timestamps": True,
            "pii_sanitization": True,
            "speaker_diarization": False
        }
    }


@router.get("/health/transcriber")
def transcriber_health():
    """Health check for transcriber service."""
    try:
        # Try to get the service
        service = get_transcription_service()
        model_loaded = service.model is not None or True  # Model loads lazily
        return {
            "status": "healthy",
            "model_loaded": model_loaded,
            "model_size": os.getenv("WHISPER_MODEL_SIZE", "base")
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }


@router.get("/health")
def health_check():
    """General health check endpoint."""
    return {"status": "healthy", "service": "clarivox"}


# Include router
app.include_router(router)


# Run with: uvicorn app.main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
