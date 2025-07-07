# main.py

import os
import uuid
import shutil
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import whisper

from utils.fhir import build_communication_request
from utils.task import build_task
from utils.intent import detect_intent
from utils.storage import save_transcript, save_fhir_json

app = FastAPI()

# Load whisper model from cache to avoid SSL fetch
model = whisper.load_model("base", download_root=os.path.expanduser("~/.cache/whisper"))

# Setup CORS for Swagger UI (optional but safe for local dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/transcribe/")
async def transcribe_audio(file: UploadFile = File(...)):
    # 1. Save uploaded file temporarily
    file_id = str(uuid.uuid4())
    temp_path = f"temp_{file_id}.m4a"
    with open(temp_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # 2. Transcribe with Whisper
    result = model.transcribe(temp_path)
    transcript = result["text"]

    # 3. Detect intent
    intent = detect_intent(transcript)

    # 4. Build appropriate FHIR resource
    if intent == "general":
        fhir_resource = build_communication_request(transcript).dict()
        output_file = f"{file_id}_fhir.json"
    else:
        fhir_resource = build_task(transcript, intent).dict()
        output_file = f"{file_id}_task.json"

    # 5. Save results
    data_dir = "data"
    os.makedirs(data_dir, exist_ok=True)
    save_transcript(data_dir, file_id, transcript)
    save_fhir_json(data_dir, file_id, fhir_resource)

    # 6. Clean up temp file
    os.remove(temp_path)

    return fhir_resource