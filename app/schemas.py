"""
schemas.py
Pydantic models for FastAPI request/response validation and Swagger documentation.
Ensures API correctness and type safety across the Clarivox pipeline.
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any


# =============================================================================
# REQUEST SCHEMAS
# =============================================================================

class ProcessAudioRequest(BaseModel):
    """Request schema for audio processing endpoint."""
    phone_number: Optional[str] = Field(None, description="Caller phone number")
    patient_mrn: Optional[str] = Field(None, description="Patient Medical Record Number")
    facility_code: Optional[str] = Field(None, description="Facility identifier")
    language: str = Field("en", description="Language code for transcription")
    sanitize_pii: bool = Field(True, description="Whether to sanitize PII from transcript")


# =============================================================================
# RESPONSE SCHEMAS
# =============================================================================

class TranscriptionResponse(BaseModel):
    """Schema for transcription result."""
    text: str = Field(..., description="Transcribed text")
    segments: List[Dict[str, Any]] = Field(default_factory=list, description="Timestamped segments")
    language: str = Field(..., description="Detected or specified language")
    duration: float = Field(..., description="Audio duration in seconds")
    audio_hash: str = Field(..., description="SHA256 hash of audio file")
    trace_id: str = Field(..., description="Transaction trace ID")
    timestamp: str = Field(..., description="Processing timestamp (ISO format)")
    model_version: str = Field(..., description="Whisper model version used")
    confidence_score: float = Field(..., description="Average transcription confidence")
    sanitized: bool = Field(..., description="Whether PII was sanitized")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "text": "Hi, I need to refill my blood pressure medication.",
                "segments": [{"start": 0.0, "end": 3.5, "text": "Hi, I need to refill", "confidence": -0.25}],
                "language": "en",
                "duration": 5.2,
                "audio_hash": "abc123def456",
                "trace_id": "TXN-ABC12345",
                "timestamp": "2026-01-08T14:30:00Z",
                "model_version": "faster-whisper-base",
                "confidence_score": -0.25,
                "sanitized": True
            }
        }
    )


class RoutingResponse(BaseModel):
    """Schema for routing decision."""
    primary_target: str = Field(..., description="Primary routing target system")
    secondary_targets: List[str] = Field(default_factory=list, description="Secondary routing targets")
    description: str = Field(..., description="Routing rule description")
    intent: str = Field(..., description="Intent that triggered this routing")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "primary_target": "VISTA_REFILL",
                "secondary_targets": [],
                "description": "Route to VistA medication refill system",
                "intent": "medication_refill"
            }
        }
    )


class FHIRBundleResponse(BaseModel):
    """Schema for FHIR bundle output."""
    trace_id: str = Field(..., description="Transaction trace ID")
    intent: str = Field(..., description="Extracted intent")
    urgency: str = Field(..., description="Urgency level")
    communication_request: Dict[str, Any] = Field(..., description="FHIR CommunicationRequest resource")
    task: Dict[str, Any] = Field(..., description="FHIR Task resource")
    medication_requests: List[Dict[str, Any]] = Field(default_factory=list, description="FHIR MedicationRequest resources")
    observations: List[Dict[str, Any]] = Field(default_factory=list, description="FHIR Observation resources for symptoms")


class ProcessAudioResponse(BaseModel):
    """Complete response from the audio processing pipeline."""
    trace_id: str = Field(..., description="Unique transaction trace ID")
    transcription: TranscriptionResponse = Field(..., description="Transcription result")
    intent: str = Field(..., description="Primary extracted intent")
    urgency: str = Field(..., description="Urgency classification")
    medications: List[str] = Field(default_factory=list, description="Extracted medication mentions")
    symptoms: List[str] = Field(default_factory=list, description="Extracted symptom mentions")
    fhir_bundle: FHIRBundleResponse = Field(..., description="Generated FHIR resources")
    routing: RoutingResponse = Field(..., description="Routing decision")
    processing_time_ms: float = Field(..., description="Total processing time in milliseconds")


class TranscribeOnlyResponse(BaseModel):
    """Response for transcription-only endpoint."""
    text: str = Field(..., description="Transcribed text")
    segments: List[Dict[str, Any]] = Field(default_factory=list, description="Timestamped segments")
    language: str = Field(..., description="Detected or specified language")
    duration: float = Field(..., description="Audio duration in seconds")
    audio_hash: str = Field(..., description="SHA256 hash of audio file")
    trace_id: str = Field(..., description="Transaction trace ID")
    timestamp: str = Field(..., description="Processing timestamp")
    model_version: str = Field(..., description="Whisper model version")
    confidence_score: float = Field(..., description="Transcription confidence")
    sanitized: bool = Field(..., description="Whether PII was sanitized")


class ModelInfoResponse(BaseModel):
    """Information about the transcription model."""
    name: str = Field("OpenAI Whisper", description="Model name")
    variant: str = Field("faster-whisper", description="Model variant")
    size: str = Field(..., description="Model size (tiny, base, small, medium, large)")
    compute_type: str = Field(..., description="Compute type (int8, float16, float32)")


class FeaturesResponse(BaseModel):
    """Supported features information."""
    multilingual: bool = Field(True, description="Supports multiple languages")
    timestamps: bool = Field(True, description="Provides word-level timestamps")
    pii_sanitization: bool = Field(True, description="Can sanitize PII")
    speaker_diarization: bool = Field(False, description="Speaker identification support")


class AudioFormatsResponse(BaseModel):
    """Response for audio formats endpoint."""
    supported_formats: List[str] = Field(..., description="Supported audio file extensions")
    max_file_size_mb: int = Field(..., description="Maximum file size in MB")
    min_duration_seconds: float = Field(..., description="Minimum audio duration")
    max_duration_seconds: float = Field(..., description="Maximum audio duration")
    model: Dict[str, str] = Field(..., description="Model configuration")
    features: Dict[str, bool] = Field(..., description="Supported features")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "supported_formats": [".mp3", ".wav", ".m4a", ".ogg", ".flac", ".webm"],
                "max_file_size_mb": 50,
                "min_duration_seconds": 1.0,
                "max_duration_seconds": 600.0,
                "model": {
                    "name": "OpenAI Whisper",
                    "variant": "faster-whisper",
                    "size": "base",
                    "compute_type": "int8"
                },
                "features": {
                    "multilingual": True,
                    "timestamps": True,
                    "pii_sanitization": True,
                    "speaker_diarization": False
                }
            }
        }
    )


class HealthResponse(BaseModel):
    """General health check response."""
    status: str = Field(..., description="Health status")
    service: str = Field("clarivox", description="Service name")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "healthy",
                "service": "clarivox"
            }
        }
    )


class TranscriberHealthResponse(BaseModel):
    """Health check response for transcriber service."""
    status: str = Field(..., description="Transcriber health status")
    model_loaded: bool = Field(True, description="Whether model is loaded")
    model_size: str = Field("base", description="Loaded model size")
    error: Optional[str] = Field(None, description="Error message if unhealthy")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "healthy",
                "model_loaded": True,
                "model_size": "base",
                "error": None
            }
        }
    )


class ErrorResponse(BaseModel):
    """Standard error response schema."""
    detail: str = Field(..., description="Error message")
    error_type: str = Field(..., description="Error classification")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "detail": "Audio file is too large: 55.2MB (max 50MB)",
                "error_type": "AudioValidationError"
            }
        }
    )


class ValidationErrorResponse(BaseModel):
    """Validation error response schema."""
    detail: List[Dict[str, Any]] = Field(..., description="Validation error details")
    error_type: str = Field("ValidationError", description="Error type")
