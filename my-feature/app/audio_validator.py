import os
import tempfile
import mimetypes
import hashlib
import logging
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError
from typing import Optional, Tuple
from fastapi import UploadFile, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

# Setup logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Allowed extensions and settings
ALLOWED_EXTENSIONS = {".mp3", ".wav", ".m4a", ".ogg", ".flac", ".webm"}
MAX_AUDIO_FILE_SIZE_MB = float(os.getenv("MAX_AUDIO_FILE_SIZE_MB", 50))
MIN_AUDIO_DURATION_SEC = float(os.getenv("MIN_AUDIO_DURATION_SEC", 1.0))
MAX_AUDIO_DURATION_SEC = float(os.getenv("MAX_AUDIO_DURATION_SEC", 600.0))
TARGET_SAMPLE_RATE = 16000
TARGET_CHANNELS = 1


class AudioValidationResult:
    def __init__(
        self,
        file_path: str,
        audio: AudioSegment,
        duration_sec: float,
        sha256: Optional[str],
        sample_rate: int,
        channels: int,
    ):
        self.file_path = file_path
        self.audio = audio
        self.duration_sec = duration_sec
        self.sha256 = sha256
        self.sample_rate = sample_rate
        self.channels = channels


class AudioValidationError(Exception):
    pass


def get_file_extension(filename: str) -> str:
    return os.path.splitext(filename)[-1].lower()


def verify_mime_type(file: UploadFile):
    mime_type, _ = mimetypes.guess_type(file.filename)
    if mime_type and not mime_type.startswith("audio"):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f"Invalid MIME type: {mime_type}. Only audio files allowed."
        )


def check_file_size(file: UploadFile):
    file.file.seek(0, os.SEEK_END)
    size_mb = file.file.tell() / (1024 * 1024)
    file.file.seek(0)
    if size_mb > MAX_AUDIO_FILE_SIZE_MB:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f"Audio file is too large: {size_mb:.2f}MB (max {MAX_AUDIO_FILE_SIZE_MB}MB)"
        )


def hash_file(file_path: str) -> str:
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def convert_to_wav(audio: AudioSegment, output_path: str):
    audio = audio.set_frame_rate(TARGET_SAMPLE_RATE).set_channels(TARGET_CHANNELS)
    audio.export(output_path, format="wav")


def is_silent(audio: AudioSegment, silence_threshold_db: float = -45.0) -> bool:
    return audio.dBFS < silence_threshold_db


def validate_audio_file(file: UploadFile, compute_hash: bool = True) -> AudioValidationResult:
    verify_mime_type(file)

    ext = get_file_extension(file.filename)
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file extension: {ext}"
        )

    check_file_size(file)

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
            tmp.write(file.file.read())
            tmp_path = tmp.name
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f"Failed to store uploaded audio: {str(e)}"
        )

    try:
        audio = AudioSegment.from_file(tmp_path)
    except CouldntDecodeError:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Failed to decode audio file. The file may be corrupted or unsupported."
        )

    duration_sec = audio.duration_seconds
    if duration_sec < MIN_AUDIO_DURATION_SEC or duration_sec > MAX_AUDIO_DURATION_SEC:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f"Audio duration must be between {MIN_AUDIO_DURATION_SEC}s and {MAX_AUDIO_DURATION_SEC}s (got {duration_sec:.2f}s)"
        )

    if is_silent(audio):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Audio appears to be silent or too quiet to process."
        )

    if audio.frame_rate != TARGET_SAMPLE_RATE:
        logger.warning(f"Sample rate is {audio.frame_rate}Hz (expected {TARGET_SAMPLE_RATE}Hz)")

    if audio.channels != TARGET_CHANNELS:
        logger.warning(f"Audio is not mono (channels = {audio.channels})")

    sha256 = hash_file(tmp_path) if compute_hash else None

    return AudioValidationResult(
        file_path=tmp_path,
        audio=audio,
        duration_sec=duration_sec,
        sha256=sha256,
        sample_rate=audio.frame_rate,
        channels=audio.channels
    )


class AudioValidator:
    SUPPORTED_EXTENSIONS = {".mp3", ".wav", ".m4a", ".ogg", ".flac", ".webm"}
    SUPPORTED_MIME_TYPES = {
        "audio/mpeg", "audio/wav", "audio/x-wav", "audio/x-m4a",
        "audio/ogg", "audio/flac", "audio/webm"
    }

    def __init__(self):
        from app.config import settings
        self.max_file_size_mb = settings.MAX_AUDIO_FILE_SIZE_MB
        self.min_duration_sec = settings.MIN_AUDIO_DURATION_SEC
        self.max_duration_sec = settings.MAX_AUDIO_DURATION_SEC

    def validate_audio_file(self, file: UploadFile) -> Tuple[str, float, str]:
        logger.debug(f"Validating uploaded audio file: {file.filename}")

        ext = os.path.splitext(file.filename)[-1].lower()
        if ext not in self.SUPPORTED_EXTENSIONS:
            raise AudioValidationError(f"Unsupported file extension: {ext}")

        file.file.seek(0, os.SEEK_END)
        file_size_mb = file.file.tell() / (1024 * 1024)
        file.file.seek(0)

        if file_size_mb > self.max_file_size_mb:
            raise AudioValidationError(f"File size {file_size_mb:.2f}MB exceeds maximum {self.max_file_size_mb}MB")

        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
            tmp.write(file.file.read())
            tmp_path = tmp.name

        try:
            audio = AudioSegment.from_file(tmp_path)
        except Exception as e:
            os.remove(tmp_path)
            raise AudioValidationError(f"Failed to decode audio file: {str(e)}")

        duration_sec = len(audio) / 1000.0

        if duration_sec < self.min_duration_sec:
            os.remove(tmp_path)
            raise AudioValidationError(f"Audio duration {duration_sec:.2f}s is below minimum {self.min_duration_sec}s")

        if duration_sec > self.max_duration_sec:
            os.remove(tmp_path)
            raise AudioValidationError(f"Audio duration {duration_sec:.2f}s exceeds maximum {self.max_duration_sec}s")

        file_hash = self._hash_file(tmp_path)

        logger.info(f"Audio file validated: duration={duration_sec:.2f}s, sha256={file_hash}")

        wav_path = self._convert_to_standard_format(audio)
        os.remove(tmp_path)

        return wav_path, duration_sec, file_hash

    def _convert_to_standard_format(self, audio: AudioSegment) -> str:
        output = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        output_path = output.name
        output.close()
        audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)
        audio.export(output_path, format="wav")
        logger.debug(f"Audio auto-converted to 16kHz mono WAV: {output_path}")
        return output_path

    def _hash_file(self, filepath: str) -> str:
        sha256_hash = hashlib.sha256()
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()


def get_audio_validator() -> AudioValidator:
    return AudioValidator()
