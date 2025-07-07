import os
import uuid
import json
import whisper
from fastapi import FastAPI, UploadFile, File, HTTPException
from utils.fhir import build_communication_request
from utils.storage import save_transcript, save_fhir_json

# Ensure data directory
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)

app = FastAPI(
    title="Clarivox MVP",
    description="Voicemail → Transcription → FHIR pipeline",
    version="0.1.0"
)

# Load Whisper model once, using local cache only
try:
    model = whisper.load_model(
        "base",
        download_root=os.path.expanduser("~/.cache/whisper")
    )
except Exception as e:
    raise RuntimeError("Failed to load Whisper model from cache: " + str(e))


@app.post("/transcribe/")
async def transcribe_voicemail(file: UploadFile = File(...)):
    # 1. Load audio into temp file
    audio_path = os.path.join(DATA_DIR, f"{uuid.uuid4()}.{file.filename.split('.')[-1]}")
    with open(audio_path, "wb") as out:
        out.write(await file.read())

    # 2. Transcribe
    result = model.transcribe(audio_path)
    transcript = result["text"].strip()
    if not transcript:
        raise HTTPException(status_code=500, detail="Transcription returned empty text")

    # 3. Build FHIR resource
    communication = build_communication_request(transcript)

    # 4. Save outputs
    file_id = os.path.splitext(os.path.basename(audio_path))[0]
    save_transcript(DATA_DIR, file_id, transcript)
    save_fhir_json(DATA_DIR, file_id, communication.dict())

    return communication