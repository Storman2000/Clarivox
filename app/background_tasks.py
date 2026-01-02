"""
background_tasks.py
Async post-processing tasks for file cleanup and logging.
"""

import os
import shutil
import logging
import hashlib
from pathlib import Path
from datetime import datetime
from fastapi import BackgroundTasks

from app.config import settings

logger = logging.getLogger(__name__)

# Configuration
AUDIO_TEMP_DIR = os.getenv("AUDIO_TEMP_DIR", "/tmp/clarivox/audio")
TRACE_LOG_DIR = os.getenv("TRACE_LOG_DIR", "/tmp/clarivox/logs")

# Ensure directories exist
Path(AUDIO_TEMP_DIR).mkdir(parents=True, exist_ok=True)
Path(TRACE_LOG_DIR).mkdir(parents=True, exist_ok=True)


def cleanup_temp_file(file_path: str):
    """Remove temporary audio file after processing."""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.debug(f"Deleted temporary file: {file_path}")
    except Exception as e:
        logger.warning(f"Failed to delete temp file {file_path}: {e}")


def delete_temp_file(file_path: str):
    """Alias for cleanup_temp_file."""
    cleanup_temp_file(file_path)


def compute_sha256(file_path: str) -> str:
    """Compute SHA-256 hash of a file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def save_trace_log(trace_id: str, transcript: str, audio_hash: str, model_version: str):
    """Persist audit log for completed transcription."""
    try:
        timestamp = datetime.utcnow().isoformat()
        log_file = os.path.join(TRACE_LOG_DIR, f"{trace_id}.log")
        
        with open(log_file, "w") as f:
            f.write(f"Trace ID: {trace_id}\n")
            f.write(f"Timestamp: {timestamp}\n")
            f.write(f"Model: {model_version}\n")
            f.write(f"Audio SHA-256: {audio_hash}\n")
            f.write(f"Transcript: {transcript}\n")
        
        logger.debug(f"Saved trace log: {log_file}")
    except Exception as e:
        logger.error(f"Error saving trace log for {trace_id}: {e}")


def log_transcription_trace(audio_path: str, transcript: str, trace_id: str):
    """Log trace info after successful transcription."""
    try:
        audio_hash = compute_sha256(audio_path)
        timestamp = datetime.utcnow().isoformat()

        trace_data = {
            "trace_id": trace_id,
            "timestamp": timestamp,
            "audio_hash": audio_hash,
            "transcript_preview": transcript[:100] + "..."
        }

        logger.info(f"Logged trace: {trace_id}")
    except Exception as e:
        logger.error(f"Trace logging failed: {trace_id} -- {str(e)}")


def move_file_to_archive(file_path: str, archive_dir: str = None):
    """Move audio file to archive folder (optional audit log)."""
    archive_dir = archive_dir or settings.ARCHIVE_DIR
    try:
        os.makedirs(archive_dir, exist_ok=True)
        timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        filename = Path(file_path).name
        archived_path = os.path.join(archive_dir, f"{timestamp}_{filename}")
        
        shutil.copy(file_path, archived_path)
        logger.info(f"Archived audio file: {archived_path}")
    except Exception as e:
        logger.warning(f"Failed to archive file: {file_path} -- {str(e)}")


def move_to_archive(file_path: str):
    """Alias for move_file_to_archive."""
    move_file_to_archive(file_path)


def schedule_cleanup(background_tasks: BackgroundTasks, file_path: str):
    """Schedule cleanup of temporary file."""
    background_tasks.add_task(delete_temp_file, file_path)


def schedule_trace_logging(background_tasks: BackgroundTasks, trace_id: str, transcript: str, audio_hash: str, model_version: str):
    """Schedule trace log persistence."""
    background_tasks.add_task(save_trace_log, trace_id, transcript, audio_hash, model_version)


def schedule_background_tasks(
    background_tasks: BackgroundTasks,
    audio_path: str,
    transcript: str,
    trace_id: str,
    archive: bool = False
):
    """Schedule common background tasks after processing."""
    background_tasks.add_task(cleanup_temp_file, audio_path)
    background_tasks.add_task(log_transcription_trace, audio_path, transcript, trace_id)
    
    if archive:
        background_tasks.add_task(move_to_archive, audio_path)


def register_cleanup(background_tasks: BackgroundTasks, file_path: str):
    """Register cleanup task - alias for compatibility."""
    background_tasks.add_task(cleanup_temp_file, file_path)
