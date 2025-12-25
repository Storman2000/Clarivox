**[Based on everything you've provided --- including screenshots, file
structures, the error table, and the attached EchoCore Logic.docx ---
here\'s a comprehensive audit of what you need vs. don't need in your
repo, and what should be kept, cleaned up, or removed.]{.mark}**

**[✅ Core Components You NEED (Confirmed via Doc + Logic)]{.mark}**

**[These are the required Clarivox MVP components. Keep and refine
these.]{.mark}**

| **[Folder/File]{.mark}**                | **[Purpose]{.mark}**                                       | **[Keep?]{.mark}**  |
|-----------------------------------------|------------------------------------------------------------|---------------------|
| **[app/main.py]{.mark}**                | **[FastAPI entrypoint, routes + orchestrator]{.mark}**     | **[✅ YES]{.mark}** |
| **[app/audio_validator.py]{.mark}**     | **[Audio validation logic (MIME, duration, etc.)]{.mark}** | **[✅ YES]{.mark}** |
| **[app/transcriber_service.py]{.mark}** | **[Wrapper around ASR (e.g., Whisper)]{.mark}**            | **[✅ YES]{.mark}** |
| **[app/pii_sanitizer.py]{.mark}**       | **[Redacts PHI/PII from transcripts]{.mark}**              | **[✅ YES]{.mark}** |
| **[app/intent_extractor.py]{.mark}**    | **[NLP logic (intent, urgency, entities)]{.mark}**         | **[✅ YES]{.mark}** |
| **[app/fhir_generator.py]{.mark}**      | **[Converts extracted info into FHIR artifacts]{.mark}**   | **[✅ YES]{.mark}** |
| **[app/router.py]{.mark}**              | **[Endpoint and route manager]{.mark}**                    | **[✅ YES]{.mark}** |
| **[app/trace_logger.py]{.mark}**        | **[Logging w/ trace ID, confidence, timestamps]{.mark}**   | **[✅ YES]{.mark}** |
| **[app/error_handler.py]{.mark}**       | **[Custom error handling for FastAPI]{.mark}**             | **[✅ YES]{.mark}** |
| **[app/mock_services.py]{.mark}**       | **[Stub for Cerner/VistA routes]{.mark}**                  | **[✅ YES]{.mark}** |
| **[app/config.py]{.mark}**              | **[Central env config and limits]{.mark}**                 | **[✅ YES]{.mark}** |
| **[app/test_audio_pipeline.py]{.mark}** | **[Full E2E integration test]{.mark}**                     | **[✅ YES]{.mark}** |
| **[app/metrics.py]{.mark}**             | **[Push metrics to CloudWatch/Prometheus]{.mark}**         | **[✅ YES]{.mark}** |
| **[app/diarization_utils.py]{.mark}**   | **[Prep for speaker diarization]{.mark}**                  | **[✅ YES]{.mark}** |
| **[app/language_detector.py]{.mark}**   | **[Language detection fallback (EN/ES)]{.mark}**           | **[✅ YES]{.mark}** |
| **[app/background_tasks.py]{.mark}**    | **[Async cleanup/logging tasks]{.mark}**                   | **[✅ YES]{.mark}** |

**[❌ UNNECESSARY OR DUPLICATE FILES (Costly Bloat)]{.mark}**

**[These were likely inherited from template repos or freelancers.
Unless you are directly using them, delete or archive
externally.]{.mark}**

| **[Folder/File]{.mark}**                                       | **[Why Remove]{.mark}**                                              |
|----------------------------------------------------------------|----------------------------------------------------------------------|
| **[fhir-server-main/]{.mark}**                                 | **[Full Java-based FHIR server repo (not used in Clarivox)]{.mark}** |
| **[hapi-fhir-starter-server/]{.mark}**                         | **[Also Java-based, redundant, not Python-compatible]{.mark}**       |
| **[node_modules/]{.mark}**                                     | **[Node.js packages; Clarivox is Python-based]{.mark}**              |
| **[backend/microsoft-fhir/]{.mark}**                           | **[Microsoft's .NET-based FHIR solution --- not needed]{.mark}**     |
| **[Any .DS_Store, .ipynb_checkpoints/]{.mark}**                | **[Editor/system-generated clutter]{.mark}**                         |
| **[test_fhir_server/ or old tests/ with no relevance]{.mark}** | **[If they don't test Clarivox endpoints]{.mark}**                   |

**[🔧 REQUIRED CLEANUP (For MVP Stability)]{.mark}**

**[Here's what needs attention regardless of what's already in
place:]{.mark}**

**[🧪 Tests]{.mark}**

- **[Make sure all logic modules above have corresponding unit
  tests.]{.mark}**

- **[Your test_audio_pipeline.py must be able to simulate the full
  voicemail → FHIR pipeline.]{.mark}**

**[🔐 .env Setup]{.mark}**

**[Ensure your .env has:]{.mark}**

**[WHISPER_MODEL_SIZE=base]{.mark}**

**[OPENAI_API_KEY=your_key_here]{.mark}**

**[DEBUG=True]{.mark}**

**[📦 requirements.txt]{.mark}**

**[Must include:]{.mark}**

**[fastapi]{.mark}**

**[uvicorn]{.mark}**

**[pydantic]{.mark}**

**[python-dotenv]{.mark}**

**[pydub]{.mark}**

**[fhir.resources]{.mark}**

**[langdetect]{.mark}**

**[transformers]{.mark}**

**[torch]{.mark}**

**[spacy]{.mark}**

**[🚫 WASTED COST: Why You May Have Paid for Redundant Work]{.mark}**

**[You likely paid for unnecessary integration of:]{.mark}**

- **[Java-based HAPI FHIR servers]{.mark}**

- **[Microsoft's backend scaffolding]{.mark}**

- **[Node.js packages or servers (if not for UI)]{.mark}**

- **[General-purpose template clones]{.mark}**

**[If you are not using them to host a full FHIR-compliant backend
yourself (which Clarivox does not require for MVP), they do not belong
in your repo.]{.mark}**

**[✅ YOUR NEXT STEP: REPO FINALIZATION]{.mark}**

**[1. Remove Redundant Folders]{.mark}**

**[Archive externally or delete from repo.]{.mark}**

**[2. Reorganize Structure]{.mark}**

**[/app]{.mark}**

**[main.py]{.mark}**

**[audio_validator.py]{.mark}**

**[transcriber_service.py]{.mark}**

**[pii_sanitizer.py]{.mark}**

**[intent_extractor.py]{.mark}**

**[fhir_generator.py]{.mark}**

**[router.py]{.mark}**

**[trace_logger.py]{.mark}**

**[error_handler.py]{.mark}**

**[mock_services.py]{.mark}**

**[config.py]{.mark}**

**[metrics.py]{.mark}**

**[diarization_utils.py]{.mark}**

**[language_detector.py]{.mark}**

**[background_tasks.py]{.mark}**

**[/tests]{.mark}**

**[test_audio_pipeline.py]{.mark}**

**[\... (test modules per file)]{.mark}**

**[/data (optional for audio)]{.mark}**

**[// .env]{.mark}**

**[// requirements.txt]{.mark}**

**[3. Test and Fix Errors]{.mark}**

**[Refer to the error chart (import issues, runtime bugs, API
mismatches) and task your freelancer or dev to:]{.mark}**

- **[Validate every endpoint via /docs]{.mark}**

- **[Trace logs via trace_logger]{.mark}**

- **[Use pytest with coverage]{.mark}**

**Clarivox Project Directory Structure (Post-Cleanup)**

clarivox/

├── app/

│ ├── \_\_init\_\_.py

│ ├── main.py \# FastAPI entrypoint & routing

│ ├── router.py \# Defines endpoints and connects logic modules

│ ├── config.py \# Environment/config loader

│ │

│ ├── audio_validator.py \# Audio validation (duration, MIME,
corruption)

│ ├── transcriber_service.py \# ASR interface (Whisper, etc.)

│ ├── pii_sanitizer.py \# Redacts PII/PHI from transcript

│ ├── intent_extractor.py \# Extracts clinical intent, urgency, meds,
etc.

│ ├── fhir_generator.py \# Builds FHIR-compliant resources

│ │

│ ├── trace_logger.py \# Logging w/ trace_id, latency, confidence, etc.

│ ├── error_handler.py \# Centralized error and exception handling

│ ├── metrics.py \# Push metrics to CloudWatch or Prometheus

│ ├── mock_services.py \# Fake Cerner/VistA response endpoints

│ │

│ ├── diarization_utils.py \# Stub for speaker diarization logic

│ ├── language_detector.py \# Language detection (e.g. English vs
Spanish)

│ └── background_tasks.py \# Async post-processing (file cleanup,
logging)

│

├── tests/

│ ├── \_\_init\_\_.py

│ ├── test_audio_pipeline.py \# End-to-end pipeline test

│ ├── test_audio_validator.py \# Unit tests for audio_validator.py

│ ├── test_intent_extractor.py \# Unit tests for NLP module

│ └── test_fhir_generator.py \# Unit tests for FHIR creation

│

├── data/ \# (Optional) sample audio files for testing

│ └── sample_voicemail.wav

│

├── .env \# Environment variables (WHISPER_MODEL_SIZE, keys)

├── requirements.txt \# Python dependencies

├── README.md \# Setup, run, and usage instructions

└── run.sh \# (Optional) Script to launch app or pipeline

**🧹 Also Make Sure:**

- ❌ You've **removed** these:

  - fhir-server-main/

  - hapi-fhir-starter-server/

  - node_modules/

  - backend/microsoft-fhir/

  - Any .ipynb, .DS_Store, .idea/, etc.

- ✅ Your requirements.txt reflects real usage (no bloat)

- ✅ All Python files have proper \_\_init\_\_.py for import resolution

- ✅ main.py runs with uvicorn app.main:app \--reload

- ✅ /docs auto-generates and works cleanly (FastAPI Swagger UI)

import os

import tempfile

import mimetypes

import hashlib

import logging

from pydub import AudioSegment

from pydub.exceptions import CouldntDecodeError

from typing import Optional

from fastapi import UploadFile, HTTPException

from starlette.status import HTTP_400_BAD_REQUEST

\# Setup logger

logger = logging.getLogger(\_\_name\_\_)

logger.setLevel(logging.DEBUG)

\# Allowed extensions and settings

ALLOWED_EXTENSIONS = {\".mp3\", \".wav\", \".m4a\", \".ogg\", \".flac\",
\".webm\"}

MAX_AUDIO_FILE_SIZE_MB = float(os.getenv(\"MAX_AUDIO_FILE_SIZE_MB\",
50))

MIN_AUDIO_DURATION_SEC = float(os.getenv(\"MIN_AUDIO_DURATION_SEC\",
1.0))

MAX_AUDIO_DURATION_SEC = float(os.getenv(\"MAX_AUDIO_DURATION_SEC\",
600.0))

TARGET_SAMPLE_RATE = 16000

TARGET_CHANNELS = 1

class AudioValidationResult:

def \_\_init\_\_(

self,

file_path: str,

audio: AudioSegment,

duration_sec: float,

sha256: Optional\[str\],

sample_rate: int,

channels: int,

):

self.file_path = file_path

self.audio = audio

self.duration_sec = duration_sec

self.sha256 = sha256

self.sample_rate = sample_rate

self.channels = channels

def get_file_extension(filename: str) -\> str:

return os.path.splitext(filename)\[-1\].lower()

def verify_mime_type(file: UploadFile):

mime_type, \_ = mimetypes.guess_type(file.filename)

if mime_type and not mime_type.startswith(\"audio\"):

raise HTTPException(

status_code=HTTP_400_BAD_REQUEST,

detail=f\"Invalid MIME type: {mime_type}. Only audio files allowed.\"

)

def check_file_size(file: UploadFile):

file.file.seek(0, os.SEEK_END)

size_mb = file.file.tell() / (1024 \* 1024)

file.file.seek(0)

if size_mb \> MAX_AUDIO_FILE_SIZE_MB:

raise HTTPException(

status_code=HTTP_400_BAD_REQUEST,

detail=f\"Audio file is too large: {size_mb:.2f}MB (max
{MAX_AUDIO_FILE_SIZE_MB}MB)\"

)

def hash_file(file_path: str) -\> str:

hasher = hashlib.sha256()

with open(file_path, \"rb\") as f:

for chunk in iter(lambda: f.read(8192), b\"\"):

hasher.update(chunk)

return hasher.hexdigest()

def convert_to_wav(audio: AudioSegment, output_path: str):

audio =
audio.set_frame_rate(TARGET_SAMPLE_RATE).set_channels(TARGET_CHANNELS)

audio.export(output_path, format=\"wav\")

def is_silent(audio: AudioSegment, silence_threshold_db: float = -45.0)
-\> bool:

return audio.dBFS \< silence_threshold_db

def validate_audio_file(file: UploadFile, compute_hash: bool = True) -\>
AudioValidationResult:

verify_mime_type(file)

ext = get_file_extension(file.filename)

if ext not in ALLOWED_EXTENSIONS:

raise HTTPException(

status_code=HTTP_400_BAD_REQUEST,

detail=f\"Unsupported file extension: {ext}\"

)

check_file_size(file)

try:

with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:

tmp.write(file.file.read())

tmp_path = tmp.name

except Exception as e:

raise HTTPException(

status_code=HTTP_400_BAD_REQUEST,

detail=f\"Failed to store uploaded audio: {str(e)}\"

)

try:

audio = AudioSegment.from_file(tmp_path)

except CouldntDecodeError:

raise HTTPException(

status_code=HTTP_400_BAD_REQUEST,

detail=\"Failed to decode audio file. The file may be corrupted or
unsupported.\"

)

duration_sec = audio.duration_seconds

if duration_sec \< MIN_AUDIO_DURATION_SEC or duration_sec \>
MAX_AUDIO_DURATION_SEC:

raise HTTPException(

status_code=HTTP_400_BAD_REQUEST,

detail=f\"Audio duration must be between {MIN_AUDIO_DURATION_SEC}s and
{MAX_AUDIO_DURATION_SEC}s (got {duration_sec:.2f}s)\"

)

if is_silent(audio):

raise HTTPException(

status_code=HTTP_400_BAD_REQUEST,

detail=\"Audio appears to be silent or too quiet to process.\"

)

if audio.frame_rate != TARGET_SAMPLE_RATE:

logger.warning(f\"Sample rate is {audio.frame_rate}Hz (expected
{TARGET_SAMPLE_RATE}Hz)\")

if audio.channels != TARGET_CHANNELS:

logger.warning(f\"Audio is not mono (channels = {audio.channels})\")

sha256 = hash_file(tmp_path) if compute_hash else None

return AudioValidationResult(

file_path=tmp_path,

audio=audio,

duration_sec=duration_sec,

sha256=sha256,

sample_rate=audio.frame_rate,

channels=audio.channels

)

\# audio_endpoint.py

import os

import traceback

from fastapi import APIRouter, File, UploadFile, Form, HTTPException

from fastapi.responses import JSONResponse

from starlette.status import HTTP_400_BAD_REQUEST,
HTTP_500_INTERNAL_SERVER_ERROR

from typing import Optional

from transcriber import get_transcription_service

from audio_validator import AudioValidator, ValidationError

router = APIRouter()

\# Load environment config

MAX_FILE_SIZE_MB = int(os.getenv(\"MAX_AUDIO_FILE_SIZE_MB\", 50))

MIN_DURATION = float(os.getenv(\"MIN_AUDIO_DURATION_SEC\", 1.0))

MAX_DURATION = float(os.getenv(\"MAX_AUDIO_DURATION_SEC\", 600))

\# Initialize components

validator = AudioValidator(

max_file_size_mb=MAX_FILE_SIZE_MB,

min_duration_sec=MIN_DURATION,

max_duration_sec=MAX_DURATION

)

transcriber = get_transcription_service()

@router.post(\"/transcribe-only\")

async def transcribe_only(

audio_file: UploadFile = File(\...),

language: Optional\[str\] = Form(None),

sanitize_pii: bool = Form(True)

):

try:

\# Step 1: Validate audio file

audio_bytes, audio_meta = await validator.validate(audio_file)

\# Step 2: Transcribe

result = transcriber.transcribe_from_bytes(

audio_bytes,

file_name=audio_file.filename,

language=language,

sanitize_pii=sanitize_pii

)

return JSONResponse(status_code=200, content=result.to_dict())

except ValidationError as e:

raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))

except Exception as e:

traceback.print_exc()

raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR,
detail=\"Internal error during transcription\")

@router.get(\"/audio-formats\")

async def audio_formats():

return {

\"supported_formats\": \[\".mp3\", \".wav\", \".m4a\", \".ogg\",
\".flac\", \".webm\"\],

\"max_file_size_mb\": MAX_FILE_SIZE_MB,

\"min_duration_seconds\": MIN_DURATION,

\"max_duration_seconds\": MAX_DURATION,

\"model\": {

\"name\": \"OpenAI Whisper\",

\"variant\": \"faster-whisper\",

\"size\": os.getenv(\"WHISPER_MODEL_SIZE\", \"base\"),

\"compute_type\": os.getenv(\"WHISPER_COMPUTE_TYPE\", \"int8\")

},

\"features\": {

\"multilingual\": True,

\"timestamps\": True,

\"pii_sanitization\": True,

\"speaker_diarization\": False

}

}

import os

import tempfile

import hashlib

from datetime import datetime

from typing import Optional, Dict, Any

from faster_whisper import WhisperModel

from pydub import AudioSegment

from transcriber_utils.audio_validator import AudioValidator

from transcriber_utils.audio_normalizer import normalize_audio

from transcriber_utils.pii_sanitizer import sanitize_transcript

class TranscriptionResult:

def \_\_init\_\_(self, text: str, segments: list, language: str,
duration: float,

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

def to_dict(self) -\> Dict\[str, Any\]:

return self.\_\_dict\_\_

class TranscriptionService:

def \_\_init\_\_(self):

self.model_size = os.getenv(\"WHISPER_MODEL_SIZE\", \"base\")

self.device = os.getenv(\"WHISPER_DEVICE\", \"cpu\")

self.compute_type = os.getenv(\"WHISPER_COMPUTE_TYPE\", \"int8\")

self.model = WhisperModel(self.model_size, device=self.device,
compute_type=self.compute_type)

def transcribe_from_file(self, file_path: str, language: Optional\[str\]
= None, sanitize_pii: bool = True) -\> TranscriptionResult:

\# Validate

AudioValidator.validate(file_path)

\# Normalize

normalized_path = normalize_audio(file_path)

\# Hash for traceability

audio_hash = self.\_compute_hash(normalized_path)

trace_id = f\"TXN-{audio_hash\[:8\].upper()}\"

timestamp = datetime.utcnow().isoformat() + \'Z\'

\# Transcribe

segments, info = self.model.transcribe(normalized_path,
language=language, beam_size=5, vad_filter=True)

full_text = \" \".join(\[seg.text.strip() for seg in segments\])

confidence = sum(\[seg.avg_logprob for seg in segments\]) /
len(segments) if segments else -1.0

\# Sanitize

if sanitize_pii:

full_text = sanitize_transcript(full_text)

for seg in segments:

seg.text = sanitize_transcript(seg.text)

return TranscriptionResult(

text=full_text,

segments=\[seg.\_asdict() for seg in segments\],

language=info.language,

duration=info.duration,

audio_hash=audio_hash,

trace_id=trace_id,

timestamp=timestamp,

model_version=f\"faster-whisper-{self.model_size}\",

confidence_score=confidence,

sanitized=sanitize_pii

)

@staticmethod

def \_compute_hash(file_path: str) -\> str:

sha256 = hashlib.sha256()

with open(file_path, \"rb\") as f:

for chunk in iter(lambda: f.read(4096), b\"\"):

sha256.update(chunk)

return sha256.hexdigest()

\_transcriber_instance: Optional\[TranscriptionService\] = None

def get_transcription_service() -\> TranscriptionService:

global \_transcriber_instance

if \_transcriber_instance is None:

\_transcriber_instance = TranscriptionService()

return \_transcriber_instance

\# audio_normalizer.py

import os

import tempfile

import subprocess

import logging

from typing import Tuple

from pydub import AudioSegment

from utils.exceptions import AudioProcessingError

logger = logging.getLogger(\_\_name\_\_)

SUPPORTED_FORMATS = \[\".mp3\", \".wav\", \".m4a\", \".ogg\", \".flac\",
\".webm\"\]

TARGET_SAMPLE_RATE = 16000

TARGET_CHANNELS = 1 \# mono

def normalize_audio(input_path: str) -\> Tuple\[str, int\]:

\"\"\"

Normalize audio to 16kHz mono WAV format using ffmpeg.

Args:

input_path (str): Path to the original audio file.

Returns:

Tuple\[str, int\]: Path to the normalized WAV file and duration in
seconds.

Raises:

AudioProcessingError: If normalization fails.

\"\"\"

try:

logger.info(f\"Normalizing audio: {input_path}\")

with tempfile.NamedTemporaryFile(delete=False, suffix=\".wav\") as
tmpfile:

output_path = tmpfile.name

command = \[

\"ffmpeg\", \"-y\",

\"-i\", input_path,

\"-ac\", str(TARGET_CHANNELS),

\"-ar\", str(TARGET_SAMPLE_RATE),

output_path

\]

process = subprocess.run(command, stdout=subprocess.PIPE,
stderr=subprocess.PIPE)

if process.returncode != 0:

raise AudioProcessingError(f\"FFmpeg normalization failed:
{process.stderr.decode()}\")

audio = AudioSegment.from_file(output_path)

duration_sec = len(audio) / 1000.0

logger.info(f\"Audio normalized successfully: {output_path}
({duration_sec:.2f}s)\")

return output_path, duration_sec

except Exception as e:

logger.exception(\"Error normalizing audio\")

raise AudioProcessingError(f\"Normalization failed: {str(e)}\")

def is_supported_format(filename: str) -\> bool:

\_, ext = os.path.splitext(filename.lower())

return ext in SUPPORTED_FORMATS

import mimetypes

import magic

from typing import Optional

class MIMETypeVerifier:

\"\"\"

Verifies the MIME type of an uploaded audio file.

Uses both extension-based and content-based inspection.

\"\"\"

def \_\_init\_\_(self):

self.allowed_mime_types = {

\'audio/mpeg\', \# .mp3

\'audio/wav\', \# .wav

\'audio/x-wav\',

\'audio/x-m4a\', \# .m4a

\'audio/flac\', \# .flac

\'audio/ogg\', \# .ogg

\'audio/webm\', \# .webm

}

def is_mime_type_allowed(self, file_path: str) -\> bool:

\"\"\"

Verifies MIME type using both \`python-magic\` and extension lookup.

Args:

file_path (str): Path to the audio file

Returns:

bool: True if MIME type is valid, else False

\"\"\"

mime_from_magic = self.\_get_mime_type_by_content(file_path)

mime_from_extension = self.\_get_mime_type_by_extension(file_path)

if mime_from_magic in self.allowed_mime_types:

return True

if mime_from_extension in self.allowed_mime_types:

return True

return False

def \_get_mime_type_by_content(self, file_path: str) -\>
Optional\[str\]:

try:

return magic.Magic(mime=True).from_file(file_path)

except Exception:

return None

def \_get_mime_type_by_extension(self, file_path: str) -\>
Optional\[str\]:

mime, \_ = mimetypes.guess_type(file_path)

return mime

\"\"import os

import tempfile

import hashlib

import mimetypes

import magic

from pydub import AudioSegment

from fastapi import UploadFile

from typing import Optional, Tuple

from utils.logger import logger

from config import settings

class AudioValidationError(Exception):

pass

class AudioValidator:

SUPPORTED_EXTENSIONS = {\".mp3\", \".wav\", \".m4a\", \".ogg\",
\".flac\", \".webm\"}

SUPPORTED_MIME_TYPES = {

\"audio/mpeg\", \"audio/wav\", \"audio/x-wav\", \"audio/x-m4a\",

\"audio/ogg\", \"audio/flac\", \"audio/webm\"

}

def \_\_init\_\_(self):

self.max_file_size_mb = settings.MAX_AUDIO_FILE_SIZE_MB

self.min_duration_sec = settings.MIN_AUDIO_DURATION_SEC

self.max_duration_sec = settings.MAX_AUDIO_DURATION_SEC

def validate_audio_file(self, file: UploadFile) -\> Tuple\[str, float,
str\]:

logger.debug(f\"Validating uploaded audio file: {file.filename}\")

ext = os.path.splitext(file.filename)\[-1\].lower()

if ext not in self.SUPPORTED_EXTENSIONS:

raise AudioValidationError(f\"Unsupported file extension: {ext}\")

file.file.seek(0, os.SEEK_END)

file_size_mb = file.file.tell() / (1024 \* 1024)

file.file.seek(0)

if file_size_mb \> self.max_file_size_mb:

raise AudioValidationError(f\"File size {file_size_mb:.2f}MB exceeds
maximum {self.max_file_size_mb}MB\")

with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:

tmp.write(file.file.read())

tmp_path = tmp.name

try:

audio = AudioSegment.from_file(tmp_path)

except Exception as e:

os.remove(tmp_path)

raise AudioValidationError(f\"Failed to decode audio file: {str(e)}\")

duration_sec = len(audio) / 1000.0

if duration_sec \< self.min_duration_sec:

os.remove(tmp_path)

raise AudioValidationError(f\"Audio duration {duration_sec:.2f}s is
below minimum {self.min_duration_sec}s\")

if duration_sec \> self.max_duration_sec:

os.remove(tmp_path)

raise AudioValidationError(f\"Audio duration {duration_sec:.2f}s exceeds
maximum {self.max_duration_sec}s\")

mime = magic.Magic(mime=True).from_file(tmp_path)

if mime not in self.SUPPORTED_MIME_TYPES:

os.remove(tmp_path)

raise AudioValidationError(f\"Detected MIME type \'{mime}\' is not
supported\")

file_hash = self.\_hash_file(tmp_path)

logger.info(f\"Audio file validated: duration={duration_sec:.2f}s,
mime={mime}, sha256={file_hash}\")

wav_path = self.\_convert_to_standard_format(audio)

os.remove(tmp_path)

return wav_path, duration_sec, file_hash

def \_convert_to_standard_format(self, audio: AudioSegment) -\> str:

output = tempfile.NamedTemporaryFile(delete=False, suffix=\".wav\")

output_path = output.name

output.close()

audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)

audio.export(output_path, format=\"wav\")

logger.debug(f\"Audio auto-converted to 16kHz mono WAV: {output_path}\")

return output_path

def \_hash_file(self, filepath: str) -\> str:

sha256_hash = hashlib.sha256()

with open(filepath, \"rb\") as f:

for byte_block in iter(lambda: f.read(4096), b\"\"):

sha256_hash.update(byte_block)

return sha256_hash.hexdigest()

def get_audio_validator() -\> AudioValidator:

return AudioValidator()

\"\"\"

transcriber_service.py

Transcription service using faster-whisper (OpenAI Whisper variant)

Includes integration with audio validator and optional PII sanitizer

\"\"\"

import os

import hashlib

import logging

from typing import Optional, Dict, Any

from datetime import datetime

from dotenv import load_dotenv

from faster_whisper import WhisperModel

from audio_validator import validate_audio_file, AudioValidationResult

\# Optional: If using a PII sanitizer module

try:

from pii_sanitizer import sanitize_transcript

except ImportError:

sanitize_transcript = lambda text: text \# No-op fallback

\# Load environment variables

load_dotenv()

\# Logging

logger = logging.getLogger(\_\_name\_\_)

logger.setLevel(logging.INFO)

\# Whisper model config from .env

MODEL_SIZE = os.getenv(\"WHISPER_MODEL_SIZE\", \"base\")

COMPUTE_TYPE = os.getenv(\"WHISPER_COMPUTE_TYPE\", \"int8\")

DEVICE = os.getenv(\"WHISPER_DEVICE\", \"cpu\")

BEAM_SIZE = int(os.getenv(\"WHISPER_BEAM_SIZE\", 5))

TEMPERATURE = float(os.getenv(\"WHISPER_TEMPERATURE\", 0.0))

VAD_FILTER = os.getenv(\"WHISPER_VAD_FILTER\", \"true\").lower() ==
\"true\"

\# Load Whisper model

logger.info(f\"Loading Whisper model: {MODEL_SIZE} ({DEVICE})\")

model = WhisperModel(model_size_or_path=MODEL_SIZE, device=DEVICE,
compute_type=COMPUTE_TYPE)

def generate_audio_hash(filepath: str) -\> str:

with open(filepath, \"rb\") as f:

return hashlib.sha256(f.read()).hexdigest()

def transcribe_audio(filepath: str, language: Optional\[str\] = None,
sanitize_pii: bool = True) -\> Dict\[str, Any\]:

logger.info(f\"Starting transcription for {filepath}\")

\# Validate and normalize audio

validation: AudioValidationResult = validate_audio_file(filepath)

if not validation.valid:

raise ValueError(f\"Audio validation failed: {validation.reason}\")

\# Transcribe audio

segments, info = model.transcribe(

audio=validation.normalized_path,

language=language,

beam_size=BEAM_SIZE,

temperature=TEMPERATURE,

vad_filter=VAD_FILTER,

return_segments=True

)

transcript_text = \" \".join(\[seg.text for seg in segments\])

\# Optional PII sanitization

if sanitize_pii:

transcript_text = sanitize_transcript(transcript_text)

\# Build response

return {

\"text\": transcript_text.strip(),

\"segments\": \[

{

\"start\": seg.start,

\"end\": seg.end,

\"text\": seg.text,

\"confidence\": getattr(seg, \"avg_logprob\", -1.0)

} for seg in segments

\],

\"language\": info.language,

\"duration\": info.duration,

\"audio_hash\": generate_audio_hash(validation.normalized_path),

\"trace_id\":
f\"TXN-{hashlib.md5(filepath.encode()).hexdigest()\[:10\].upper()}\",

\"timestamp\": datetime.utcnow().isoformat() + \"Z\",

\"model_version\": f\"faster-whisper-{MODEL_SIZE}\",

\"confidence_score\": getattr(info, \"avg_logprob\", -1.0),

\"sanitize

import re

from typing import Tuple, Dict

class PIISanitizer:

\"\"\"

A utility class for detecting and sanitizing personally identifiable
information (PII)

from transcribed text.

Supports redaction of:

\- Phone numbers

\- Email addresses

\- Social Security Numbers (SSNs)

\- Dates

\- MRNs (if patterns are known)

\"\"\"

def \_\_init\_\_(self):

self.patterns: Dict\[str, str\] = {

\"PHONE\":
r\"\b(?:\\?1\[-.\s\]?)\*\\?\d{3}\\?\[-.\s\]?\d{3}\[-.\s\]?\d{4}\b\",

\"EMAIL\":
r\"\b\[A-Za-z0-9.\_%+-\]+@\[A-Za-z0-9.-\]+\\\[A-Z\|a-z\]{2,}\b\",

\"SSN\": r\"\b\d{3}\[- \]?\d{2}\[- \]?\d{4}\b\",

\"DATE\": r\"\b(?:\d{1,2}\[-/\]){2}\d{2,4}\b\",

\# Add more patterns if needed (e.g., MRN)

}

def sanitize(self, text: str) -\> Tuple\[str, Dict\[str, int\]\]:

\"\"\"

Sanitize PII from a string.

Args:

text (str): The input transcript.

Returns:

Tuple\[str, Dict\[str, int\]\]: Redacted transcript and PII type counts.

\"\"\"

pii_counts: Dict\[str, int\] = {}

sanitized_text = text

for label, pattern in self.patterns.items():

matches = re.findall(pattern, sanitized_text)

pii_counts\[label\] = len(matches)

sanitized_text = re.sub(pattern, f\"\[{label}\]\", sanitized_text)

return sanitized_text, pii_counts

\# Example usage

if \_\_name\_\_ == \"\_\_main\_\_\":

sanitizer = PIISanitizer()

sample = \"Patient email is john.doe@example.com and SSN is 123-45-6789.
Call at (555) 123-4567.\"

redacted, stats = sanitizer.sanitize(sample)

print(\"Redacted:\", redacted)

print(\"Stats:\", stats)

import re

from typing import List, Optional

from uuid import uuid4

from dataclasses import dataclass

import logging

import spacy

\# Load spaCy model

nlp = spacy.load(\"en_core_web_sm\")

logger = logging.getLogger(\_\_name\_\_)

\# \-\-- ENUM-LIKE CLASSES \-\--

class IntentType:

MEDICATION_REFILL = \"medication_refill\"

MEDICATION_SIDE_EFFECT = \"medication_side_effect\"

MEDICATION_QUESTION = \"medication_question\"

APPOINTMENT_SCHEDULE = \"appointment_schedule\"

APPOINTMENT_CANCEL = \"appointment_cancel\"

APPOINTMENT_RESCHEDULE = \"appointment_reschedule\"

APPOINTMENT_CONFIRM = \"appointment_confirm\"

SYMPTOM_REPORT = \"symptom_report\"

TEST_RESULTS = \"test_results\"

BENEFITS_INQUIRY = \"benefits_inquiry\"

BENEFITS_CLAIM = \"benefits_claim\"

CALLBACK_REQUEST = \"callback_request\"

GENERAL_INQUIRY = \"general_inquiry\"

COMPLAINT = \"complaint\"

CRISIS_SUICIDE = \"crisis_suicide\"

CRISIS_SELF_HARM = \"crisis_self_harm\"

CRISIS_VIOLENCE = \"crisis_violence\"

UNKNOWN = \"unknown\"

class UrgencyLevel:

EMERGENT = \"emergent\"

URGENT = \"urgent\"

SEMI_URGENT = \"semi_urgent\"

ROUTINE = \"routine\"

\# \-\-- DATA CLASSES \-\--

@dataclass

class Entity:

text: str

confidence: float = 1.0

negated: bool = False

@dataclass

class TemporalExpression:

text: str

resolved_date: Optional\[str\] = None

@dataclass

class IntentExtractionResult:

primary_intent: str

secondary_intents: List\[str\]

urgency: str

intent_confidence: float

urgency_confidence: float

medications: List\[Entity\]

symptoms: List\[Entity\]

temporal_expressions: List\[TemporalExpression\]

crisis_indicators: List\[str\]

negation_detected: bool

transcript: str

trace_id: str

def to_dict(self):

return self.\_\_dict\_\_

\# \-\-- CORE SERVICE \-\--

class IntentExtractionService:

def \_\_init\_\_(self):

self.intent_patterns = {

IntentType.MEDICATION_REFILL: \[r\"refill.\*prescription\", r\"ran
out.\*medication\"\],

IntentType.APPOINTMENT_SCHEDULE: \[r\"schedule.\*appointment\",
r\"book.\*visit\"\],

IntentType.SYMPTOM_REPORT: \[r\"chest pain\", r\"shortness of breath\",
r\"fever\"\],

IntentType.CRISIS_SUICIDE: \[r\"end my life\", r\"kill myself\"\],

IntentType.CALLBACK_REQUEST: \[r\"call me back\"\]

}

self.urgency_patterns = {

UrgencyLevel.EMERGENT: \[r\"can't breathe\", r\"suicidal\", r\"kill
myself\"\],

UrgencyLevel.URGENT: \[r\"severe pain\", r\"ASAP\"\],

UrgencyLevel.SEMI_URGENT: \[r\"this week\", r\"soon\"\],

}

self.common_meds = {\"lisinopril\", \"atorvastatin\", \"metformin\"}

self.common_symptoms = {\"pain\", \"headache\", \"fever\", \"chest
pain\", \"shortness of breath\"}

def extract(self, transcript: str, trace_id: Optional\[str\] = None) -\>
IntentExtractionResult:

trace_id = trace_id or f\"CLV-{uuid4().hex\[:12\].upper()}\"

doc = nlp(transcript)

primary_intent = IntentType.UNKNOWN

secondary_intents = \[\]

confidence = 0.5

urgency = UrgencyLevel.ROUTINE

urgency_confidence = 0.5

medications = \[\]

symptoms = \[\]

temporal_expressions = \[\]

crisis_indicators = \[\]

negation_detected = False

for intent, patterns in self.intent_patterns.items():

for pattern in patterns:

if re.search(pattern, transcript, re.IGNORECASE):

if primary_intent == IntentType.UNKNOWN:

primary_intent = intent

confidence = 0.9

else:

secondary_intents.append(intent)

for level, patterns in self.urgency_patterns.items():

for pattern in patterns:

if re.search(pattern, transcript, re.IGNORECASE):

urgency = level

urgency_confidence = 0.9

for token in doc:

if token.text.lower() in self.common_meds:

medications.append(Entity(text=token.text, confidence=0.9))

if token.text.lower() in self.common_symptoms:

negated = self.\_check_negation(token)

if negated:

negation_detected = True

symptoms.append(Entity(text=token.text, confidence=0.9,
negated=negated))

if re.search(r\"(suicide\|kill myself\|gun\|knife)\", transcript,
re.IGNORECASE):

crisis_indicators.append(\"potential_crisis\")

return IntentExtractionResult(

primary_intent=primary_intent,

secondary_intents=secondary_intents,

urgency=urgency,

intent_confidence=confidence,

urgency_confidence=urgency_confidence,

medications=medications,

symptoms=symptoms,

temporal_expressions=temporal_expressions,

crisis_indicators=crisis_indicators,

negation_detected=negation_detected,

transcript=transcript,

trace_id=trace_id

)

def \_check_negation(self, token):

for child in token.children:

if child.dep\_ == \"neg\":

return True

for ancestor in token.ancestors:

for child in ancestor.children:

if child.dep\_ == \"neg\":

return True

return False

\# Factory

\_service = None

def get_intent_service():

global \_service

if \_service is None:

\_service = IntentExtractionService()

return \_service

import uuid

from datetime import datetime

from typing import List, Optional

from models import (

IntentType,

UrgencyLevel,

FHIRCommunicationRequest,

FHIRTask,

MedicationRequest,

SymptomObservation

)

class FHIRGenerator:

def \_\_init\_\_(self):

pass

def generate_patient_reference(self, mrn: str) -\> str:

return f\"Patient/{mrn}\"

def create_communication_request(

self,

transcript: str,

intent: IntentType,

urgency: UrgencyLevel,

patient_ref: str,

trace_id: str,

medications: Optional\[List\[str\]\] = None,

symptoms: Optional\[List\[str\]\] = None

) -\> FHIRCommunicationRequest:

return FHIRCommunicationRequest(

id=f\"commreq-{uuid.uuid4()}\",

status=\"active\",

subject=patient_ref,

payload=\[transcript\],

authored_on=datetime.utcnow().isoformat(),

category=intent.value,

priority=urgency.value,

trace_id=trace_id,

medications=medications or \[\],

symptoms=symptoms or \[\]

)

def create_task(

self,

intent: IntentType,

urgency: UrgencyLevel,

patient_ref: str,

trace_id: str

) -\> FHIRTask:

return FHIRTask(

id=f\"task-{uuid.uuid4()}\",

status=\"requested\",

intent=\"order\",

priority=urgency.value,

for_reference=patient_ref,

execution_period={

\"start\": datetime.utcnow().isoformat()

},

trace_id=trace_id,

task_type=intent.value

)

def generate_medication_requests(

self,

medications: List\[str\],

patient_ref: str

) -\> List\[MedicationRequest\]:

return \[

MedicationRequest(

id=f\"medreq-{uuid.uuid4()}\",

subject=patient_ref,

medication_codeable_concept=med,

authored_on=datetime.utcnow().isoformat()

)

for med in medications

\]

def generate_symptom_observations(

self,

symptoms: List\[str\],

patient_ref: str

) -\> List\[SymptomObservation\]:

return \[

SymptomObservation(

id=f\"obs-{uuid.uuid4()}\",

subject=patient_ref,

code=sym,

effective_datetime=datetime.utcnow().isoformat()

)

for sym in symptoms

\]

import uuid

from datetime import datetime

from typing import List, Optional

from models import (

IntentType,

UrgencyLevel,

FHIRCommunicationRequest,

FHIRTask,

MedicationRequest,

SymptomObservation

)

class FHIRGenerator:

def \_\_init\_\_(self):

pass

def generate_patient_reference(self, mrn: str) -\> str:

return f\"Patient/{mrn}\"

def create_communication_request(

self,

transcript: str,

intent: IntentType,

urgency: UrgencyLevel,

patient_ref: str,

trace_id: str,

medications: Optional\[List\[str\]\] = None,

symptoms: Optional\[List\[str\]\] = None

) -\> FHIRCommunicationRequest:

return FHIRCommunicationRequest(

id=f\"commreq-{uuid.uuid4()}\",

status=\"active\",

subject=patient_ref,

payload=\[transcript\],

authored_on=datetime.utcnow().isoformat(),

category=intent.value,

priority=urgency.value,

trace_id=trace_id,

medications=medications or \[\],

symptoms=symptoms or \[\]

)

def create_task(

self,

intent: IntentType,

urgency: UrgencyLevel,

patient_ref: str,

trace_id: str

) -\> FHIRTask:

return FHIRTask(

id=f\"task-{uuid.uuid4()}\",

status=\"requested\",

intent=\"order\",

priority=urgency.value,

for_reference=patient_ref,

execution_period={

\"start\": datetime.utcnow().isoformat()

},

trace_id=trace_id,

task_type=intent.value

)

def generate_medication_requests(

self,

medications: List\[str\],

patient_ref: str

) -\> List\[MedicationRequest\]:

return \[

MedicationRequest(

id=f\"medreq-{uuid.uuid4()}\",

subject=patient_ref,

medication_codeable_concept=med,

authored_on=datetime.utcnow().isoformat()

)

for med in medications

\]

def generate_symptom_observations(

self,

symptoms: List\[str\],

patient_ref: str

) -\> List\[SymptomObservation\]:

return \[

SymptomObservation(

id=f\"obs-{uuid.uuid4()}\",

subject=patient_ref,

code=sym,

effective_datetime=datetime.utcnow().isoformat()

)

for sym in symptoms

\]

import logging

import os

from datetime import datetime

from uuid import uuid4

import hashlib

\# Configuration

LOG_LEVEL = os.getenv(\"TRACE_LOG_LEVEL\", \"INFO\")

LOG_FORMAT = \"%(asctime)s \| %(levelname)s \| %(trace_id)s \|
%(message)s\"

\# Configure root logger

logger = logging.getLogger(\"clarivox_trace\")

logger.setLevel(LOG_LEVEL)

\# Create handler

console_handler = logging.StreamHandler()

formatter = logging.Formatter(LOG_FORMAT)

console_handler.setFormatter(formatter)

logger.addHandler(console_handler)

class TraceContextFilter(logging.Filter):

def \_\_init\_\_(self, trace_id: str):

super().\_\_init\_\_()

self.trace_id = trace_id

def filter(self, record):

record.trace_id = self.trace_id

return True

class TraceLogger:

def \_\_init\_\_(self, trace_id: str = None):

self.trace_id = trace_id or self.\_generate_trace_id()

self.filter = TraceContextFilter(self.trace_id)

self.logger = logger

self.logger.addFilter(self.filter)

def \_generate_trace_id(self):

return f\"CLV-{uuid4().hex\[:12\].upper()}\"

def log_info(self, message: str):

self.logger.info(message)

def log_warning(self, message: str):

self.logger.warning(message)

def log_error(self, message: str):

self.logger.error(message)

def log_debug(self, message: str):

self.logger.debug(message)

def log_stage_timing(self, stage: str, duration_ms: float):

self.logger.info(f\"Stage \'{stage}\' completed in {duration_ms:.2f}
ms\")

def attach_trace_to_response(self, response: dict) -\> dict:

response\[\"trace_id\"\] = self.trace_id

response\[\"timestamp\"\] = datetime.utcnow().isoformat()

return response

\# Utility for hashing audio

def hash_audio_file(file_path: str) -\> str:

\"\"\"Return SHA-256 hash of audio file contents\"\"\"

sha256 = hashlib.sha256()

with open(file_path, \'rb\') as f:

for chunk in iter(lambda: f.read(4096), b\"\"):

sha256.update(chunk)

return sha256.hexdigest()

\# Usage Example:

\# trace_logger = TraceLogger()

\# trace_logger.log_info(\"Transcription started\")

\# hash_val = hash_audio_file(\"sample.wav\")

from fastapi import APIRouter, UploadFile, File, Form, HTTPException

from fastapi.responses import JSONResponse

from typing import Optional

import uuid

import traceback

from audio_validator import validate_audio_file

from transcriber_service import get_transcription_service

from pii_sanitizer import sanitize_transcript

from intent_extractor import get_intent_service

from fhir_generator import generate_fhir_bundle

from router import determine_routing_targets

from trace_logger import log_pipeline_trace

router = APIRouter()

transcriber = get_transcription_service()

intent_service = get_intent_service()

@router.post(\"/process-audio\")

async def process_audio(

audio_file: UploadFile = File(\...),

phone_number: Optional\[str\] = Form(None),

patient_mrn: Optional\[str\] = Form(None),

facility_code: Optional\[str\] = Form(None),

language: Optional\[str\] = Form(\"en\"),

sanitize_pii: bool = Form(True),

):

trace_id = f\"TXN-{uuid.uuid4().hex\[:12\].upper()}\"

try:

\# Step 1: Validate audio input

metadata = await validate_audio_file(audio_file)

\# Step 2: Transcribe

transcription = await transcriber.transcribe(

file=audio_file,

language=language

)

\# Step 3: Sanitize transcript

if sanitize_pii:

transcription\[\"text\"\] =
sanitize_transcript(transcription\[\"text\"\])

transcription\[\"sanitized\"\] = True

else:

transcription\[\"sanitized\"\] = False

\# Step 4: NLP / Intent Extraction

nlp_result = intent_service.extract(

transcript=transcription\[\"text\"\],

trace_id=trace_id

)

\# Step 5: Generate FHIR artifacts

fhir_data = generate_fhir_bundle(

intent=nlp_result.primary_intent,

urgency=nlp_result.urgency,

patient_mrn=patient_mrn,

transcript=transcription\[\"text\"\],

trace_id=trace_id,

medications=\[m.text for m in nlp_result.medications\],

symptoms=\[s.text for s in nlp_result.symptoms if not s.negated\]

)

\# Step 6: Route to target systems

routing_info = determine_routing_targets(nlp_result.primary_intent)

\# Step 7: Log trace

log_pipeline_trace(

trace_id=trace_id,

metadata=metadata,

transcription=transcription,

intent_result=nlp_result,

fhir_bundle=fhir_data,

routing=routing_info

)

\# Step 8: Return full pipeline response

return JSONResponse({

\"trace_id\": trace_id,

\"transcription\": transcription,

\"intent\": nlp_result.primary_intent,

\"urgency\": nlp_result.urgency,

\"medications\": \[m.text for m in nlp_result.medications\],

\"symptoms\": \[s.text for s in nlp_result.symptoms\],

\"fhir_bundle\": fhir_data,

\"routing\": routing_info

})

except Exception as e:

error_msg = f\"Pipeline failed: {str(e)}\"

traceback.print_exc()

raise HTTPException(status_code=500, detail=error_msg)

@router.post(\"/transcribe-only\")

async def transcribe_only(

audio_file: UploadFile = File(\...),

language: Optional\[str\] = Form(\"en\"),

sanitize_pii: bool = Form(True),

):

try:

\# Validate

await validate_audio_file(audio_file)

\# Transcribe

result = await transcriber.transcribe(

file=audio_file,

language=language

)

\# Sanitize

if sanitize_pii:

result\[\"text\"\] = sanitize_transcript(result\[\"text\"\])

result\[\"sanitized\"\] = True

return result

except Exception as e:

error_msg = f\"Transcription failed: {str(e)}\"

traceback.print_exc()

raise HTTPException(status_code=500, detail=error_msg)

@router.get(\"/health/transcriber\")

def transcriber_health():

return {

\"status\": \"health

import logging

import os

from datetime import datetime

from typing import Optional, Dict

\# Setup logging configuration

LOG_DIR = os.getenv(\"LOG_DIR\", \"./logs\")

os.makedirs(LOG_DIR, exist_ok=True)

TRACE_LOG_FILE = os.path.join(LOG_DIR, \"trace.log\")

logging.basicConfig(

level=logging.INFO,

format=\'%(asctime)s \[%(levelname)s\] %(message)s\',

handlers=\[

logging.FileHandler(TRACE_LOG_FILE),

logging.StreamHandler()

\]

)

def log_trace(

trace_id: str,

stage: str,

message: str,

extra: Optional\[Dict\] = None,

level: str = \"info\"\\:

\"\"\"

Log a trace-level message with consistent metadata.

Args:

trace_id (str): Unique trace ID

stage (str): Pipeline stage (e.g. transcription, NLP, FHIR)

message (str): Human-readable message

extra (dict, optional): Additional metadata

level (str): Logging level (info, warning, error)

\"\"\"

payload = {

\"trace_id\": trace_id,

\"stage\": stage,

\"message\": message,

\"timestamp\": datetime.utcnow().isoformat() + \"Z\"

}

if extra:

payload.update(extra)

log_func = getattr(logging, level.lower(), logging.info)

log_func(payload)

def log_pipeline_summary(trace_id: str, summary: Dict):

\"\"\"

Log a full pipeline execution summary for auditing.

Args:

trace_id (str): Unique trace ID

summary (dict): Summary of pipeline execution

\"\"\"

log_trace(

trace_id=trace_id,

stage=\"pipeline_summary\",

message=\"Pipeline execution complete\",

extra=summary,

level=\"info\"

)

def log_error(trace_id: str, stage: str, error: Exception):

\"\"\"

Log an error that occurred in a specific pipeline stage.

Args:

trace_id (str): Trace ID

stage (str): Pipeline stage

error (Exception): Error object

\"\"\"

log_trace(

trace_id=trace

import logging

import os

from datetime import datetime

from typing import Optional, Dict

\# Setup logging configuration

LOG_DIR = os.getenv(\"LOG_DIR\", \"./logs\")

os.makedirs(LOG_DIR, exist_ok=True)

TRACE_LOG_FILE = os.path.join(LOG_DIR, \"trace.log\")

logging.basicConfig(

level=logging.INFO,

format=\'%(asctime)s \[%(levelname)s\] %(message)s\',

handlers=\[

logging.FileHandler(TRACE_LOG_FILE),

logging.StreamHandler()

\]

)

def log_trace(

trace_id: str,

stage: str,

message: str,

extra: Optional\[Dict\] = None,

level: str = \"info\"\\:

\"\"\"

Log a trace-level message with consistent metadata.

Args:

trace_id (str): Unique trace ID

stage (str): Pipeline stage (e.g. transcription, NLP, FHIR)

message (str): Human-readable message

extra (dict, optional): Additional metadata

level (str): Logging level (info, warning, error)

\"\"\"

payload = {

\"trace_id\": trace_id,

\"stage\": stage,

\"message\": message,

\"timestamp\": datetime.utcnow().isoformat() + \"Z\"

}

if extra:

payload.update(extra)

log_func = getattr(logging, level.lower(), logging.info)

log_func(payload)

def log_pipeline_summary(trace_id: str, summary: Dict):

\"\"\"

Log a full pipeline execution summary for auditing.

Args:

trace_id (str): Unique trace ID

summary (dict): Summary of pipeline execution

\"\"\"

log_trace(

trace_id=trace_id,

stage=\"pipeline_summary\",

message=\"Pipeline execution complete\",

extra=summary,

level=\"info\"

)

def log_error(trace_id: str, stage: str, error: Exception):

\"\"\"

Log an error that occurred in a specific pipeline stage.

Args:

trace_id (str): Trace ID

stage (str): Pipeline stage

error (Exception): Error object

\"\"\"

log_trace(

trace_id=trace_id,

stage=stage,

message=f\"Error occurred: {str(error)}\",

extra={\"error_type\": type(error).\_\_name\_\_},

level=\"error\"

)

import logging

from fastapi import Request

from fastapi.responses import JSONResponse

from starlette.exceptions import HTTPException as StarletteHTTPException

from fastapi.exceptions import RequestValidationError

\# Initialize logger

logger = logging.getLogger(\"clarivox.error_handler\")

\# Custom Exception Classes

class ClarivoxException(Exception):

def \_\_init\_\_(self, message: str, status_code: int = 400):

self.message = message

self.status_code = status_code

super().\_\_init\_\_(message)

class AudioValidationError(ClarivoxException):

pass

class TranscriptionError(ClarivoxException):

pass

class IntentExtractionError(ClarivoxException):

pass

class FHIRGenerationError(ClarivoxException):

pass

class RoutingError(ClarivoxException):

pass

\# Global Exception Handlers

async def clarivox_exception_handler(request: Request, exc:
ClarivoxException):

logger.error(f\"{exc.\_\_class\_\_.\_\_name\_\_}: {exc.message}\",
extra={\"path\": request.url.path})

return JSONResponse(

status_code=exc.status_code,

content={\"detail\": exc.message, \"error_type\":
exc.\_\_class\_\_.\_\_name\_\_},

)

async def validation_exception_handler(request: Request, exc:
RequestValidationError):

logger.warning(f\"Validation error: {exc.errors()}\", extra={\"path\":
request.url.path})

return JSONResponse(

status_code=422,

content={\"detail\": exc.errors(), \"error_type\": \"ValidationError\"},

)

async def http_exception_handler(request: Request, exc:
StarletteHTTPException):

logger.warning(f\"HTTP error: {exc.detail}\", extra={\"path\":
request.url.path})

return JSONResponse(

status_code=exc.status_code,

content={\"detail\": exc.detail, \"error_type\": \"HTTPException\"},

)

async def generic_exception_handler(request: Request, exc: Exception):

logger.critical(f\"Unhandled exception: {str(exc)}\", extra={\"path\":
request.url.path})

return JSONResponse(

status_code=500,

content={\"detail\": \"An unexpected error occurred.\", \"error_type\":
\"InternalServerError\"},

)

\# Register these handlers in main.py using:

\#

\# from error_handler import \*

\# app.add_exception_handler(ClarivoxException,
clarivox_exception_handler)

\# app.add_exception_handler(RequestValidation

\# test_audio_pipeline.py

import os

import pytest

from pathlib import Path

from fastapi.testclient import TestClient

from main import app

\# Sample audio test data

TEST_AUDIO_PATH = Path(\"tests/assets/sample_voicemail.mp3\")

client = TestClient(app)

\# Integration test for the full audio processing pipeline

def test_process_audio_pipeline():

if not TEST_AUDIO_PATH.exists():

pytest.skip(\"Test audio file not found.\")

with open(TEST_AUDIO_PATH, \"rb\") as audio_file:

response = client.post(

\"/process-audio\",

files={\"audio_file\": (\"sample_voicemail.mp3\", audio_file,
\"audio/mpeg\")},

data={

\"phone_number\": \"555-1234\",

\"patient_mrn\": \"12345678\",

\"sanitize_pii\": \"true\"

}

)

assert response.status_code == 200

data = response.json()

\# Basic structure checks

assert \"transcription\" in data

assert \"fhir_artifacts\" in data

assert \"processing_time_ms\" in data

\# Transcription checks

transcription = data\[\"transcription\"\]

assert transcription\[\"text\"\]

assert transcription\[\"duration\"\] \> 0

assert transcription\[\"language\"\] == \"en\"

\# FHIR artifacts checks

fhir = data\[\"fhir_artifacts\"\]

assert fhir\[\"trace_id\"\].startswith(\"TXN-\")

assert fhir\[\"intent\"\] in \[\"appointment\", \"medication_refill\",
\"general_inquiry\"\]

assert \"communication_request\" in fhir

assert \"task\" in fhir

\# Health check for transcriber service

def test_transcriber_health():

response = client.get(\"/health/transcriber\")

assert response.status_code == 200

health = response.json()

assert health\[\"status\"\] == \"healthy\"

assert health\[\"model_loaded\"\] is True

\# Transcription-only test

def test_transcribe_only():

if not TEST_AUDIO_PATH.exists():

pytest.skip(\"Test audio file not found.\")

with open(TEST_AUDIO_PATH, \"rb\") as audio_file:

response = client.post(

\"/transcribe-only\",

files={\"audio_file\": (\"sample_voicemail.mp3\", audio_file,
\"audio/mpeg\")},

data={\"language\": \"en\"}

)

assert response.status_code == 200

result = response.json()

assert \"text\" in result

assert result\[\"duration\"\] \> 0

\# mock_services.py

from typing import Dict, Any

import logging

logger = logging.getLogger(\_\_name\_\_)

def mock_cerner_appointment_api(payload: Dict\[str, Any\]) -\>
Dict\[str, Any\]:

logger.info(\"\[Mock\] Routing to Cerner Appointments API with
payload:\", payload)

return {

\"status\": \"success\",

\"system\": \"Cerner\",

\"action\": \"appointment_scheduled\",

\"trace_id\": payload.get(\"trace_id\", \"N/A\")

}

def mock_vista_refill_api(payload: Dict\[str, Any\]) -\> Dict\[str,
Any\]:

logger.info(\"\[Mock\] Routing to VistA Refill API with payload:\",
payload)

return {

\"status\": \"success\",

\"system\": \"VistA\",

\"action\": \"medication_refill_processed\",

\"trace_id\": payload.get(\"trace_id\", \"N/A\")

}

def mock_reach_vet_crisis_flag(payload: Dict\[str, Any\]) -\> Dict\[str,
Any\]:

logger.warning(\"\[Mock\] Crisis flag sent to REACH VET with payload:\",
payload)

return {

\"status\": \"success\",

\"system\": \"REACH_VET\",

\"action\": \"crisis_flagged\",

\"trace_id\": payload.get(\"trace_id\", \"N/A\")

}

def route_to_mock_system(system_code: str, payload: Dict\[str, Any\])
-\> Dict\[str, Any\]:

if system_code == \"CERNER_APPOINTMENTS\":

return mock_cerner_appointment_api(payload)

elif system_code == \"VISTA_REFILL\":

return mock_vista_refill_api(payload)

elif system_code == \"REACH_VET\":

return mock_reach_vet_crisis_flag(payload)

else:

logger.error(f\"\[Mock\] Unknown system code: {system_code}\")

return {

\"status\": \"error\",

\"message\": f\"Unknown routing system: {system_code}\",

\"trace_id\": payload.get(\"trace_id\", \"N/A\")

}

import os

from dotenv import load_dotenv

\# Load environment variables from .env file

load_dotenv()

\# \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--

\# General App Configuration

\# \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--

APP_NAME = \"Clarivox\"

ENV = os.getenv(\"ENV\", \"development\")

DEBUG = ENV != \"production\"

\# \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--

\# Whisper ASR Model Configuration

\# \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--

WHISPER_MODEL_SIZE = os.getenv(\"WHISPER_MODEL_SIZE\", \"base\")

WHISPER_COMPUTE_TYPE = os.getenv(\"WHISPER_COMPUTE_TYPE\", \"int8\")

WHISPER_DEVICE = os.getenv(\"WHISPER_DEVICE\", \"cpu\")

WHISPER_BEAM_SIZE = int(os.getenv(\"WHISPER_BEAM_SIZE\", 5))

WHISPER_TEMPERATURE = float(os.getenv(\"WHISPER_TEMPERATURE\", 0.0))

WHISPER_VAD_FILTER = os.getenv(\"WHISPER_VAD_FILTER\", \"true\").lower()
== \"true\"

\# \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--

\# Audio Processing Limits

\# \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--

MAX_AUDIO_FILE_SIZE_MB = int(os.getenv(\"MAX_AUDIO_FILE_SIZE_MB\", 50))

MIN_AUDIO_DURATION_SEC = float(os.getenv(\"MIN_AUDIO_DURATION_SEC\",
1.0))

MAX_AUDIO_DURATION_SEC = float(os.getenv(\"MAX_AUDIO_DURATION_SEC\",
600.0))

SUPPORTED_AUDIO_FORMATS = \[\".mp3\", \".wav\", \".m4a\", \".ogg\",
\".flac\", \".webm\"\]

STANDARD_SAMPLE_RATE = 16000

STANDARD_CHANNELS = 1

\# \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--

\# NLP and Intent Extraction

\# \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--

INTENT_CONFIDENCE_THRESHOLD =
float(os.getenv(\"INTENT_CONFIDENCE_THRESHOLD\", 0.75))

ENTITY_CONFIDENCE_THRESHOLD =
float(os.getenv(\"ENTITY_CONFIDENCE_THRESHOLD\", 0.70))

ENABLE_PII_SANITIZATION = os.getenv(\"SANITIZE_PII\", \"true\").lower()
== \"true\"

\# \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--

\# Logging and Auditing

\# \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--

ENABLE_TRACE_LOGGING = os.getenv(\"ENABLE_TRACE_LOGGING\",
\"true\").lower() == \"true\"

LOG_LEVEL = os.getenv(\"LOG_LEVEL\", \"INFO\")

\# \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--

\# External Service URLs (mock or real)

\# \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--

MOCK_CERNER_URL = os.getenv(\"MOCK_CERNER_URL\",
\"http://localhost:9001\")

MOCK_VISTA_URL = os.getenv(\"MOCK_VISTA_URL\",
\"http://localhost:9002\")

MOCK_REACH_VET_URL = os.getenv(\"MOCK_REACH_VET_URL\",
\"http://localhost:9003\")

\# \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--

\# Miscellaneous

\# \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--

HASHING_ALGORITHM = \"sha256\"

DEFAULT_LANGUAGE = os.getenv(\"DEFAULT_LANGUAGE\", \"en\")

\# metrics.py

import os

import time

import logging

import boto3

class MetricsLogger:

def \_\_init\_\_(self, service_name: str, use_cloudwatch: bool = True):

self.service_name = service_name

self.use_cloudwatch = use_cloudwatch

self.cloudwatch = None

if use_cloudwatch:

try:

self.cloudwatch = boto3.client(\'cloudwatch\',
region_name=os.getenv(\"AWS_REGION\", \"us-gov-west-1\"))

except Exception as e:

logging.warning(f\"CloudWatch setup failed: {e}\")

def log_metric(self, name: str, value: float, unit: str =
\"Milliseconds\"):

if not self.cloudwatch:

logging.debug(f\"\[METRIC\] {name}: {value} {unit}\")

return

try:

self.cloudwatch.put_metric_data(

Namespace=f\"Clarivox/{self.service_name}\",

MetricData=\[

{

\'MetricName\': name,

\'Value\': value,

\'Unit\': unit

}

\]

)

except Exception as e:

logging.error(f\"Error logging metric {name}: {e}\")

def log_latency(self, start_time: float, label: str):

duration = (time.time() - start_time) \* 1000 \# ms

self.log_metric(f\"Latency\_{label}\", duration)

\# diarization_utils.py (placeholder)

def estimate_number_of_speakers(audio_path: str) -\> int:

\"\"\"Stub for future diarization logic.\"\"\"

\# Placeholder --- real implementation would use pyannote-audio or
similar

return 1

\# language_detector.py (placeholder)

from langdetect import detect

def detect_language(text: str) -\> str:

\"\"\"Detect language of transcript (e.g., English or Spanish).\"\"\"

try:

lang = detect(text)

return \'es\' if lang == \'es\' else \'en\'

except Exception:

return \'en\' \# Default to English if detection fails

\# background_tasks.py

import os

import shutil

import logging

from fastapi import BackgroundTasks

def cleanup_temp_file(file_path: str):

try:

os.remove(file_path)

logging.debug(f\"Deleted temp file: {file_path}\")

except Exception as e:

logging.warning(f\"Failed to delete {file_path}: {e}\")

def move_file_to_archive(file_path: str, archive_dir: str =
\"./archive\"):

try:

os.makedirs(archive_dir, exist_ok=True)

shutil.move(file_path, os.path.join(archive_dir,
os.path.basename(file_path)))

logging.debug(f\"Archived file: {file_path}\")

except Exception as e:

logging.warning(f\"Failed to archive {file_path}: {e}\")

def register_cleanup(background_tasks: BackgroundTasks, file_path: str):

background_tasks.add_task(cleanup)

import time

import logging

import os

from typing import Optional

try:

import boto3

from botocore.exceptions import NoCredentialsError

except ImportError:

boto3 = None \# Graceful fallback if AWS is not being used

\# Logging setup

logger = logging.getLogger(\"metrics\")

logger.setLevel(logging.INFO)

\# Determine metrics backend

USE_CLOUDWATCH = os.getenv(\"USE_CLOUDWATCH\", \"false\").lower() ==
\"true\"

AWS_REGION = os.getenv(\"AWS_REGION\", \"us-gov-west-1\")

if USE_CLOUDWATCH and boto3:

try:

cloudwatch = boto3.client(\"cloudwatch\", region_name=AWS_REGION)

except NoCredentialsError:

logger.warning(\"AWS credentials not found. CloudWatch metrics
disabled.\")

cloudwatch = None

else:

cloudwatch = None

\# Namespace for CloudWatch

METRICS_NAMESPACE = \"Clarivox/ASR\"

def log_metric(name: str, value: float, unit: str = \"None\"):

logger.info(f\"Metric \| {name}: {value} {unit}\")

if cloudwatch:

try:

cloudwatch.put_metric_data(

Namespace=METRICS_NAMESPACE,

MetricData=\[

{

\"MetricName\": name,

\"Value\": value,

\"Unit\": unit,

}

\],

)

except Exception as e:

logger.error(f\"Failed to push metric to CloudWatch: {e}\")

def log_transcription_metrics(duration_ms: float, audio_duration_sec:
float, confidence: Optional\[float\] = None):

log_metric(\"TranscriptionLatency\", duration_ms, unit=\"Milliseconds\")

log_metric(\"AudioDuration\", audio_duration_sec, unit=\"Seconds\")

if confidence is not None:

log_metric(\"TranscriptionConfidence\", confidence, unit=\"None\")

def log_intent_metrics(intent_confidence: float, latency_ms: float,
crisis_detected: bool = False):

log_metric(\"IntentConfidence\", intent_confidence, unit=\"None\")

log_metric(\"IntentLatency\", latency_ms, unit=\"Milliseconds\")

if crisis_detected:

log_metric(\"CrisisDetected\", 1, unit=\"Count\")

def log_end_to_end_latency(start_time: float):

total_time = (time.time() - start_time) \* 1000 \# ms

log_metric(\"TotalPipelineLatency\", total_time, unit=\"Milliseconds\")

\"\"\"

diarization_utils.py

Speaker Diarization Utilities (future use)

Supports future separation of speakers in transcribed audio (e.g.,
patient vs staff).

\"\"\"

import logging

from typing import List, Dict, Optional

logger = logging.getLogger(\_\_name\_\_)

class DiarizationSegment:

def \_\_init\_\_(self, speaker_label: str, start: float, end: float,
text: str):

self.speaker_label = speaker_label

self.start = start

self.end = end

self.text = text

def to_dict(self):

return {

\"speaker\": self.speaker_label,

\"start\": self.start,

\"end\": self.end,

\"text\": self.text

}

def perform_diarization(audio_path: str) -\> List\[DiarizationSegment\]:

\"\"\"

Placeholder for future speaker diarization logic.

Currently returns a single speaker for the full audio.

Args:

audio_path (str): Path to audio file.

Returns:

List\[DiarizationSegment\]: List of segments with speaker labels.

\"\"\"

logger.warning(\"Diarization is not yet implemented. Returning dummy
segment.\")

return \[

DiarizationSegment(

speaker_label=\"Speaker 1\",

start=0.0,

end=0.0, \# Dummy, should be audio duration

text=\"\[Full transcript here\]\"

)

\]

\"\"\"

language_detector.py

Utility to detect audio language (English, Spanish, etc.)

For use when language is not explicitly provided.

\"\"\"

import logging

from typing import Optional

from langdetect import detect, DetectorFactory

logger = logging.getLogger(\_\_name\_\_)

DetectorFactory.seed = 0 \# Make results deterministic

def detect_language(text: str) -\> Optional\[str\]:

\"\"\"

Detects language from transcript text using langdetect.

Args:

text (str): Transcript text

Returns:

Optional\[str\]: ISO language code (e.g., \'en\', \'es\') or None

\"\"\"

try:

if not text or len(text.split()) \< 3:

logger.warning(\"Transcript too short to detect language reliably.\")

return None

language = detect(text)

logger.info(f\"Detected language: {language}\")

return language

except Exception as e:

logger.error(f\"Language detection failed: {e}\")

return None

\# background_tasks.py

import os

import logging

import hashlib

from pathlib import Path

from datetime import datetime

from fastapi import BackgroundTasks

logger = logging.getLogger(\_\_name\_\_)

\# Configuration

AUDIO_TEMP_DIR = os.getenv(\"AUDIO_TEMP_DIR\", \"/tmp/clarivox/audio\")

TRACE_LOG_DIR = os.getenv(\"TRACE_LOG_DIR\", \"/tmp/clarivox/logs\")

Path(AUDIO_TEMP_DIR).mkdir(parents=True, exist_ok=True)

Path(TRACE_LOG_DIR).mkdir(parents=True, exist_ok=True)

def delete_temp_file(file_path: str):

\"\"\"Remove temporary audio file after processing\"\"\"

try:

if os.path.exists(file_path):

os.remove(file_path)

logger.debug(f\"Deleted temporary file: {file_path}\")

except Exception as e:

logger.warning(f\"Failed to delete temp file {file_path}: {e}\")

def save_trace_log(trace_id: str, transcript: str, audio_hash: str,
model_version: str):

\"\"\"Persist audit log for completed transcription\"\"\"

try:

timestamp = datetime.utcnow().isoformat()

log_file = os.path.join(TRACE_LOG_DIR, f\"{trace_id}.log\")

with open(log_file, \"w\") as f:

f.write(f\"Trace ID: {trace_id}\n\")

f.write(f\"Timestamp: {timestamp}\n\")

f.write(f\"Model: {model_version}\n\")

f.write(f\"Audio SHA-256: {audio_hash}\n\")

f.write(f\"Transcript: {transcript}\n\")

logger.debug(f\"Saved trace log: {log_file}\")

except Exception as e:

logger.error(f\"Error saving trace log for {trace_id}: {e}\")

def schedule_cleanup(background_tasks: BackgroundTasks, file_path: str):

background_tasks.add_task(delete_temp_file, file_path)

def schedule_trace_logging(background_tasks: BackgroundTasks, trace_id:
str, transcript: str, audio_hash: str, model_version: str):

background_tasks.add_task(save_trace_log, trace_id, transcript,
audio_hash, model_version)

import logging

from typing import List, Dict

\# Placeholder class structure for future diarization support

class SpeakerSegment:

def \_\_init\_\_(self, start: float, end: float, speaker_label: str):

self.start = start

self.end = end

self.speaker_label = speaker_label

def to_dict(self) -\> Dict:

return {

\"start\": self.start,

\"end\": self.end,

\"speaker\": self.speaker_label

}

class DiarizationService:

def \_\_init\_\_(self, model_name: str =
\"pyannote/speaker-diarization\"):

self.model_name = model_name

self.logger = logging.getLogger(\_\_name\_\_)

self.model = None \# Lazy-load or mocked for now

def initialize_model(self):

\# TODO: Integrate pyannote.audio or other diarization tool

self.logger.info(\"Speaker diarization model initialization is
pending\...\")

self.model = True \# Placeholder to avoid None

def diarize(self, audio_path: str) -\> List\[SpeakerSegment\]:

if self.model is None:

self.initialize_model()

self.logger.warning(\"Diarization is not yet implemented. Returning
dummy segments.\")

\# Mock output for testing structure

dummy_segments = \[

SpeakerSegment(start=0.0, end=3.5, speaker_label=\"Speaker 1\"),

SpeakerSegment(start=3.5, end=7.0, speaker_label=\"Speaker 2\")

\]

return dummy_segments

def attach_speakers_to_transcript(self, segments: List\[Dict\],
speaker_segments: List\[SpeakerSegment\]) -\> List\[Dict\]:

\# Future method: aligns transcript segments with speaker diarization

\# Currently returns unmodified transcript

self.logger.info(\"Attaching speaker labels is not implemented yet.\")

return segments

import logging

from typing import Tuple

from langdetect import detect, DetectorFactory

\# For deterministic results

DetectorFactory.seed = 0

SUPPORTED_LANGUAGES = {

\"en\": \"English\",

\"es\": \"Spanish\",

\"fr\": \"French\",

\"de\": \"German\"

}

class LanguageDetector:

def \_\_init\_\_(self, default_language: str = \"en\"):

self.default_language = default_language

self.supported = SUPPORTED_LANGUAGES

logging.debug(f\"Initialized LanguageDetector with
default={default_language}\")

def detect_language(self, text: str) -\> Tuple\[str, str\]:

\"\"\"

Detects the language of a given transcript.

Returns:

(language_code, language_name)

\"\"\"

try:

detected = detect(text)

logging.debug(f\"Raw detected language: {detected}\")

if detected in self.supported:

return detected, self.supported\[detected\]

else:

logging.warning(f\"Detected unsupported language: {detected}, falling
back to default\")

return self.default_language, self.supported\[self.default_language\]

except Exception as e:

logging.error(f\"Language detection failed: {e}, using default\")

return self.default_language, self.supported\[self.default_language\]

\# For testing / usage

if \_\_name\_\_ == \"\_\_main\_\_\":

detector = LanguageDetector()

sample = \"Necesito una cita para la próxima semana\"

code, name = detector.detect_language(sample)

print(f\"Detected language: {code} ({name})\")

\# background_tasks.py

import os

import shutil

import logging

from pathlib import Path

from datetime import datetime

from fastapi import BackgroundTasks

from transcriber.utils.hashing import compute_sha256

from config import settings

from trace_logger import trace_log

logger = logging.getLogger(\_\_name\_\_)

def cleanup_temp_file(file_path: str):

\"\"\"Remove temporary audio file after processing.\"\"\"

try:

os.remove(file_path)

logger.info(f\"Deleted temporary file: {file_path}\")

except Exception as e:

logger.error(f\"Failed to delete temp file: {file_path} -- {str(e)}\")

def log_transcription_trace(audio_path: str, transcript: str, trace_id:
str):

\"\"\"Log trace info after successful transcription.\"\"\"

try:

audio_hash = compute_sha256(audio_path)

timestamp = datetime.utcnow().isoformat()

trace_data = {

\"trace_id\": trace_id,

\"timestamp\": timestamp,

\"audio_hash\": audio_hash,

\"transcript_preview\": transcript\[:100\] + \"\...\"

}

trace_log(trace_data)

logger.info(f\"Logged trace: {trace_id}\")

except Exception as e:

logger.error(f\"Trace logging failed: {trace_id} -- {str(e)}\")

def move_to_archive(file_path: str):

\"\"\"Move audio file to archive folder (optional audit log).\"\"\"

try:

archive_dir = Path(settings.ARCHIVE_DIR)

archive_dir.mkdir(parents=True, exist_ok=True)

timestamp = datetime.utcnow().strftime(\"%Y%m%dT%H%M%SZ\")

filename = Path(file_path).name

archived_path = archive_dir / f\"{timestamp}\_{filename}\"

shutil.copy(file_path, archived_path)

logger.info(f\"Archived audio file: {archived_path}\")

except Exception as e:

logger.warning(f\"Failed to archive file: {file_path} -- {str(e)}\")

def schedule_background_tasks(

background_tasks: BackgroundTasks,

audio_path: str,

transcript: str,

trace_id: str,

archive: bool = False

):

\"\"\"Schedule common background tasks after processing.\"\"\"

background_tasks.add_task(cleanup_temp_file, audio_path)

background_tasks.add_task(log_transcription_trace, audio_path,
transcript, trace_id)

if archive:

background_tasks.add_task(move_to_archive, audio_path)

\"\"\"

language_detector.py

🔍 Detects the primary spoken language in a given audio file or
transcript.

Supports auto-detection for multilingual voicemails.

\"\"\"

import langdetect

from langdetect import DetectorFactory

import logging

DetectorFactory.seed = 0 \# Make detection deterministic

SUPPORTED_LANGUAGES = {

\'en\': \'English\',

\'es\': \'Spanish\',

\'fr\': \'French\',

\'de\': \'German\'

}

DEFAULT_LANGUAGE = \'en\'

class LanguageDetectionError(Exception):

pass

def detect_language_from_text(text: str) -\> str:

\"\"\"Detect primary language of a transcript string.\"\"\"

try:

lang = langdetect.detect(text)

if lang in SUPPORTED_LANGUAGES:

logging.info(f\"Detected language: {SUPPORTED_LANGUAGES\[lang\]}
({lang})\")

return lang

else:

logging.warning(f\"Detected unsupported language: {lang}. Defaulting to
{DEFAULT_LANGUAGE}.\")

return DEFAULT_LANGUAGE

except langdetect.lang_detect_exception.LangDetectException:

logging.error(\"Language detection failed. Defaulting to English.\")

return DEFAULT_LANGUAGE

def get_language_label(lang_code: str) -\> str:

\"\"\"Return full language name from ISO code.\"\"\"

return SUPPORTED_LANGUAGES.get(lang_code, \'Unknown\')

if \_\_name\_\_ == \'\_\_main\_\_\':

\# Simple test

samples = \[

\"Necesito una cita para la próxima semana\",

\"Je souhaite renouveler mon ordonnance.\",

\"Ich brauche einen neuen Termin.\",

\"I need a refill on my blood pressure medication.\"

\]

for s in samples:

code = detect_language_from_text(s)

print(f\"Text: {s}\nDetected: {get_language_label(code)} ({code})\n\")
