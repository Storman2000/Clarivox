"""
trace_logger.py
Logging with trace IDs for audit and debugging.
Provides consistent logging across the pipeline with unique trace identifiers.
"""

import logging
import os
from datetime import datetime
from uuid import uuid4
import hashlib
from typing import Optional, Dict

# Configuration
LOG_LEVEL = os.getenv("TRACE_LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s | %(levelname)s | %(trace_id)s | %(message)s"
LOG_DIR = os.getenv("LOG_DIR", "./logs")

# Ensure log directory exists
os.makedirs(LOG_DIR, exist_ok=True)

TRACE_LOG_FILE = os.path.join(LOG_DIR, "trace.log")

# Configure root logger
logger = logging.getLogger("clarivox_trace")
logger.setLevel(LOG_LEVEL)

# Create handlers
console_handler = logging.StreamHandler()
file_handler = logging.FileHandler(TRACE_LOG_FILE)

# Create formatter
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Add handlers
if not logger.handlers:
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)


class TraceContextFilter(logging.Filter):
    def __init__(self, trace_id: str):
        super().__init__()
        self.trace_id = trace_id

    def filter(self, record):
        record.trace_id = self.trace_id
        return True


class TraceLogger:
    def __init__(self, trace_id: str = None):
        self.trace_id = trace_id or self._generate_trace_id()
        self.filter = TraceContextFilter(self.trace_id)
        self.logger = logger
        self.logger.addFilter(self.filter)

    def _generate_trace_id(self):
        return f"CLV-{uuid4().hex[:12].upper()}"

    def log_info(self, message: str):
        self.logger.info(f"[{self.trace_id}] {message}")

    def log_warning(self, message: str):
        self.logger.warning(f"[{self.trace_id}] {message}")

    def log_error(self, message: str):
        self.logger.error(f"[{self.trace_id}] {message}")

    def log_debug(self, message: str):
        self.logger.debug(f"[{self.trace_id}] {message}")

    def log_stage_timing(self, stage: str, duration_ms: float):
        self.logger.info(f"[{self.trace_id}] Stage '{stage}' completed in {duration_ms:.2f} ms")

    def attach_trace_to_response(self, response: dict) -> dict:
        response["trace_id"] = self.trace_id
        response["timestamp"] = datetime.utcnow().isoformat()
        return response


def hash_audio_file(file_path: str) -> str:
    """Return SHA-256 hash of audio file contents"""
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def log_trace(
    trace_id: str,
    stage: str,
    message: str,
    extra: Optional[Dict] = None,
    level: str = "info"
):
    """
    Log a trace-level message with consistent metadata.

    Args:
        trace_id (str): Unique trace ID
        stage (str): Pipeline stage (e.g. transcription, NLP, FHIR)
        message (str): Human-readable message
        extra (dict, optional): Additional metadata
        level (str): Logging level (info, warning, error)
    """
    payload = {
        "trace_id": trace_id,
        "stage": stage,
        "message": message,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

    if extra:
        payload.update(extra)

    log_func = getattr(logging, level.lower(), logging.info)
    log_func(f"[{trace_id}] [{stage}] {message}")


def log_pipeline_summary(trace_id: str, summary: Dict):
    """
    Log a full pipeline execution summary for auditing.

    Args:
        trace_id (str): Unique trace ID
        summary (dict): Summary of pipeline execution
    """
    log_trace(
        trace_id=trace_id,
        stage="pipeline_summary",
        message="Pipeline execution complete",
        extra=summary,
        level="info"
    )


def log_error(trace_id: str, stage: str, error: Exception):
    """
    Log an error that occurred in a specific pipeline stage.

    Args:
        trace_id (str): Trace ID
        stage (str): Pipeline stage
        error (Exception): Error object
    """
    log_trace(
        trace_id=trace_id,
        stage=stage,
        message=f"Error occurred: {str(error)}",
        extra={"error_type": type(error).__name__},
        level="error"
    )


def log_pipeline_trace(
    trace_id: str,
    metadata: dict,
    transcription: dict,
    intent_result,
    fhir_bundle: dict,
    routing: dict
):
    """Log complete pipeline trace for auditing."""
    log_trace(trace_id, "metadata", f"Audio validated: {metadata}")
    log_trace(trace_id, "transcription", f"Transcribed: {len(transcription.get('text', ''))} chars")
    log_trace(trace_id, "nlp", f"Intent: {intent_result.primary_intent}, Urgency: {intent_result.urgency}")
    log_trace(trace_id, "fhir", f"Generated FHIR bundle with {len(fhir_bundle)} resources")
    log_trace(trace_id, "routing", f"Routed to: {routing.get('primary_target', 'unknown')}")


# Alias for compatibility
def trace_log(data: dict):
    """Simple trace log function."""
    logger.info(str(data))
