from fastapi import FastAPI, UploadFile, File
from uuid import uuid4
import os
import shutil
from whisper import load_model
from utils.fhir import build_communication_request
from utils.task import build_task
from utils.storage import save_outputs

app = FastAPI()
model = load_model("base")  # Assumes model is cached locally in ~/.cache/whisper

@app.post("/voicemail/upload")
async def upload_voicemail(file: UploadFile = File(...)):
    # Generate unique UUID for this session
    uuid = uuid4()

    # Save uploaded file to temp .m4a
    temp_path = f"temp_{uuid}.m4a"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Run transcription
    result = model.transcribe(temp_path)
    transcript = result["text"]

    # Determine intent (stub for now)
    intent = None
    if "reschedule" in transcript.lower():
        intent = "reschedule"
        fhir_data = build_communication_request(transcript, uuid)
    else:
        intent = "other"
        fhir_data = build_task(transcript, uuid, intent)

    # Save transcript + FHIR JSON to disk
    save_outputs(uuid, transcript, fhir_data)

    # Clean up temp file
    os.remove(temp_path)

    return {
        "uuid": str(uuid),
        "intent": intent,
        "transcript": transcript,
        "fhir": fhir_data
    }