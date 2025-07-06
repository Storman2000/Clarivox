from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import whisper
import os
import shutil
import uuid
import json

app = FastAPI()

# Load Whisper model
model = whisper.load_model("base", download_root=os.path.expanduser("~/.cache/whisper"))

# Directories for saving files
TRANSCRIPT_DIR = "transcripts"
AUDIO_DIR = "audio"
FHIR_DIR = "fhir_outputs"
os.makedirs(TRANSCRIPT_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(FHIR_DIR, exist_ok=True)

class TranscriptionResponse(BaseModel):
    resourceType: str
    status: str
    payload: list
    reasonCode: list

@app.post("/transcribe/", response_model=TranscriptionResponse)
async def transcribe_audio(file: UploadFile = File(...)):
    # Save audio file locally
    audio_id = str(uuid.uuid4())
    audio_path = os.path.join(AUDIO_DIR, f"{audio_id}_{file.filename}")
    with open(audio_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Transcribe audio
    result = model.transcribe(audio_path)
    transcription = result["text"].strip()

    # Save transcription to file
    transcript_path = os.path.join(TRANSCRIPT_DIR, f"{audio_id}.txt")
    with open(transcript_path, "w") as f:
        f.write(transcription)

    # Generate FHIR CommunicationRequest
    communication_request = {
        "resourceType": "CommunicationRequest",
        "status": "active",
        "payload": [{"contentString": transcription}],
        "reasonCode": [{"text": "Voicemail transcription"}]
    }

    # Save FHIR output to file
    fhir_path = os.path.join(FHIR_DIR, f"{audio_id}.json")
    with open(fhir_path, "w") as f:
        json.dump(communication_request, f, indent=2)

    return communication_request