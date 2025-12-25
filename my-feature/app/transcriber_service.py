"""
transcriber_service.py
Transcription service using faster-whisper (OpenAI Whisper variant)
Includes integration with audio validator and optional PII sanitizer
"""

import os
import hashlib
import logging
from typing import Optional, Dict, Any
from datetime import datetime
from dotenv import load_dotenv
from faster_whisper import WhisperModel

from app.audio_validator import validate_audio_file, AudioValidationResult

# Optional: If using a PII sanitizer module
try:
    from app.pii_sanitizer import sanitize_transcript
except ImportError:
    sanitize_transcript = lambda text: text  # No-op fallback

# Load environment variables
load_dotenv()

# Logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Whisper model config from .env
MODEL_SIZE = os.getenv("WHISPER_MODEL_SIZE", "base")
COMPUTE_TYPE = os.getenv("WHISPER_COMPUTE_TYPE", "int8")
DEVICE = os.getenv("WHISPER_DEVICE", "cpu")
BEAM_SIZE = int(os.getenv("WHISPER_BEAM_SIZE", 5))
TEMPERATURE = float(os.getenv("WHISPER_TEMPERATURE", 0.0))
VAD_FILTER = os.getenv("WHISPER_VAD_FILTER", "true").lower() == "true"

# Load Whisper model
logger.info(f"Loading Whisper model: {MODEL_SIZE} ({DEVICE})")
model = None


def get_model():
    global model
    if model is None:
        model = WhisperModel(model_size_or_path=MODEL_SIZE, device=DEVICE, compute_type=COMPUTE_TYPE)
    return model


def generate_audio_hash(filepath: str) -> str:
    with open(filepath, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


class TranscriptionResult:
    def __init__(self, text: str, segments: list, language: str, duration: float,
                 audio_hash: str, trace_id: str, timestamp: str, model_version: str,
                 confidence_score: float, sanitized: bool):
        self.text = text
        self.segments = segments
        self.language = language
        self.duration = duration
        self.audio_hash = audio_hash
        self.trace_id = trace_id
        self.timestamp = timestamp
        self.model_version = model_version
        self.confidence_score = confidence_score
        self.sanitized = sanitized

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__


class TranscriptionService:
    def __init__(self):
        self.model_size = os.getenv("WHISPER_MODEL_SIZE", "base")
        self.device = os.getenv("WHISPER_DEVICE", "cpu")
        self.compute_type = os.getenv("WHISPER_COMPUTE_TYPE", "int8")
        self.model = None

    def _get_model(self):
        if self.model is None:
            self.model = WhisperModel(self.model_size, device=self.device, compute_type=self.compute_type)
        return self.model

    def transcribe_from_file(self, file_path: str, language: Optional[str] = None, sanitize_pii: bool = True) -> TranscriptionResult:
        # Hash for traceability
        audio_hash = generate_audio_hash(file_path)
        trace_id = f"TXN-{audio_hash[:8].upper()}"
        timestamp = datetime.utcnow().isoformat() + 'Z'

        # Transcribe
        model = self._get_model()
        segments_gen, info = model.transcribe(
            file_path,
            language=language,
            beam_size=BEAM_SIZE,
            vad_filter=VAD_FILTER
        )

        segments = list(segments_gen)
        full_text = " ".join([seg.text.strip() for seg in segments])
        
        # Calculate confidence
        if segments:
            confidence = sum([seg.avg_logprob for seg in segments]) / len(segments)
        else:
            confidence = -1.0

        # Sanitize
        if sanitize_pii:
            full_text = sanitize_transcript(full_text)

        segment_list = []
        for seg in segments:
            segment_list.append({
                "start": seg.start,
                "end": seg.end,
                "text": sanitize_transcript(seg.text) if sanitize_pii else seg.text,
                "confidence": seg.avg_logprob
            })

        return TranscriptionResult(
            text=full_text,
            segments=segment_list,
            language=info.language,
            duration=info.duration,
            audio_hash=audio_hash,
            trace_id=trace_id,
            timestamp=timestamp,
            model_version=f"faster-whisper-{self.model_size}",
            confidence_score=confidence,
            sanitized=sanitize_pii
        )


_transcriber_instance: Optional[TranscriptionService] = None


def get_transcription_service() -> TranscriptionService:
    global _transcriber_instance
    if _transcriber_instance is None:
        _transcriber_instance = TranscriptionService()
    return _transcriber_instance


def transcribe_audio(filepath: str, language: Optional[str] = None, sanitize_pii: bool = True) -> Dict[str, Any]:
    """Convenience function to transcribe audio file"""
    service = get_transcription_service()
    result = service.transcribe_from_file(filepath, language, sanitize_pii)
    return result.to_dict()
