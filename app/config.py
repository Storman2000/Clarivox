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
