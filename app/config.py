import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# -----------------------------
# General App Configuration
# -----------------------------
APP_NAME = "Clarivox"
ENV = os.getenv("ENV", "development")
DEBUG = ENV != "production"

# -----------------------------
# Whisper ASR Model Configuration
# -----------------------------
WHISPER_MODEL_SIZE = os.getenv("WHISPER_MODEL_SIZE", "base")
WHISPER_COMPUTE_TYPE = os.getenv("WHISPER_COMPUTE_TYPE", "int8")
WHISPER_DEVICE = os.getenv("WHISPER_DEVICE", "cpu")
WHISPER_BEAM_SIZE = int(os.getenv("WHISPER_BEAM_SIZE", 5))
WHISPER_TEMPERATURE = float(os.getenv("WHISPER_TEMPERATURE", 0.0))
WHISPER_VAD_FILTER = os.getenv("WHISPER_VAD_FILTER", "true").lower() == "true"

# -----------------------------
# Audio Processing Limits
# -----------------------------
MAX_AUDIO_FILE_SIZE_MB = int(os.getenv("MAX_AUDIO_FILE_SIZE_MB", 50))
MIN_AUDIO_DURATION_SEC = float(os.getenv("MIN_AUDIO_DURATION_SEC", 1.0))
MAX_AUDIO_DURATION_SEC = float(os.getenv("MAX_AUDIO_DURATION_SEC", 600.0))
SUPPORTED_AUDIO_FORMATS = [".mp3", ".wav", ".m4a", ".ogg", ".flac", ".webm"]
STANDARD_SAMPLE_RATE = 16000
STANDARD_CHANNELS = 1

# -----------------------------
# NLP and Intent Extraction
# -----------------------------
INTENT_CONFIDENCE_THRESHOLD = float(os.getenv("INTENT_CONFIDENCE_THRESHOLD", 0.75))
ENTITY_CONFIDENCE_THRESHOLD = float(os.getenv("ENTITY_CONFIDENCE_THRESHOLD", 0.70))
ENABLE_PII_SANITIZATION = os.getenv("SANITIZE_PII", "true").lower() == "true"

# -----------------------------
# Logging and Auditing
# -----------------------------
ENABLE_TRACE_LOGGING = os.getenv("ENABLE_TRACE_LOGGING", "true").lower() == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_DIR = os.getenv("LOG_DIR", "./logs")

# -----------------------------
# External Service URLs (mock or real)
# -----------------------------
MOCK_CERNER_URL = os.getenv("MOCK_CERNER_URL", "http://localhost:9001")
MOCK_VISTA_URL = os.getenv("MOCK_VISTA_URL", "http://localhost:9002")
MOCK_REACH_VET_URL = os.getenv("MOCK_REACH_VET_URL", "http://localhost:9003")

# -----------------------------
# Miscellaneous
# -----------------------------
HASHING_ALGORITHM = "sha256"
DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "en")

# Archive directory for audio files
ARCHIVE_DIR = os.getenv("ARCHIVE_DIR", "./archive")

# Settings class for compatibility
class Settings:
    MAX_AUDIO_FILE_SIZE_MB = MAX_AUDIO_FILE_SIZE_MB
    MIN_AUDIO_DURATION_SEC = MIN_AUDIO_DURATION_SEC
    MAX_AUDIO_DURATION_SEC = MAX_AUDIO_DURATION_SEC
    ARCHIVE_DIR = ARCHIVE_DIR

settings = Settings()


# -----------------------------
# Configuration Validation
# -----------------------------
def validate_config():
    """
    Validate all required configuration at startup.
    Raises RuntimeError if critical configuration is invalid.
    """
    import logging
    logger = logging.getLogger("clarivox.config")
    errors = []
    warnings = []
    
    # Check Whisper model size is valid
    valid_sizes = {"tiny", "base", "small", "medium", "large", "large-v2", "large-v3"}
    if WHISPER_MODEL_SIZE not in valid_sizes:
        errors.append(f"WHISPER_MODEL_SIZE '{WHISPER_MODEL_SIZE}' not in {valid_sizes}")
    
    # Check Whisper compute type
    valid_compute_types = {"int8", "float16", "float32"}
    if WHISPER_COMPUTE_TYPE not in valid_compute_types:
        warnings.append(f"WHISPER_COMPUTE_TYPE '{WHISPER_COMPUTE_TYPE}' may not be supported")
    
    # Check Whisper device
    valid_devices = {"cpu", "cuda", "auto"}
    if WHISPER_DEVICE not in valid_devices:
        warnings.append(f"WHISPER_DEVICE '{WHISPER_DEVICE}' may not be supported")
    
    # Check numeric ranges
    if MAX_AUDIO_FILE_SIZE_MB <= 0:
        errors.append("MAX_AUDIO_FILE_SIZE_MB must be positive")
    if MIN_AUDIO_DURATION_SEC < 0:
        errors.append("MIN_AUDIO_DURATION_SEC cannot be negative")
    if MAX_AUDIO_DURATION_SEC <= 0:
        errors.append("MAX_AUDIO_DURATION_SEC must be positive")
    if MIN_AUDIO_DURATION_SEC >= MAX_AUDIO_DURATION_SEC:
        errors.append("MIN_AUDIO_DURATION_SEC must be less than MAX_AUDIO_DURATION_SEC")
    
    # Check confidence thresholds
    if not (0.0 <= INTENT_CONFIDENCE_THRESHOLD <= 1.0):
        warnings.append(f"INTENT_CONFIDENCE_THRESHOLD {INTENT_CONFIDENCE_THRESHOLD} should be between 0 and 1")
    if not (0.0 <= ENTITY_CONFIDENCE_THRESHOLD <= 1.0):
        warnings.append(f"ENTITY_CONFIDENCE_THRESHOLD {ENTITY_CONFIDENCE_THRESHOLD} should be between 0 and 1")
    
    # Log warnings
    for warn in warnings:
        logger.warning(f"Config warning: {warn}")
    
    # Log errors and raise if any
    if errors:
        for err in errors:
            logger.error(f"Config error: {err}")
        raise RuntimeError(f"Configuration validation failed: {errors}")
    
    logger.info("✓ Configuration validated successfully")
    return True
