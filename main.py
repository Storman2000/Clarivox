from fastapi import FastAPI, UploadFile, File
from uuid import uuid4
import os
import shutil
from whisper import load_model
from utils.fhir import build_communication_request
from utils.task import build_task
from utils.storage import save_outputs
from utils.intent import extract_intent
from utils.identity import extract_patient_info

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

    # Extract patient identity
    patient_info = extract_patient_info(transcript)

    # Determine intent
    intent = extract_intent(transcript)

    # Build FHIR resource
    if intent == "reschedule":
        fhir_data = build_communication_request(transcript, uuid, patient_info)
    else:
        fhir_data = build_task(transcript, uuid, intent, patient_info)

    # Save outputs
    save_outputs(uuid, transcript, fhir_data)

    # Clean up temp file
    os.remove(temp_path)

    return {
        "uuid": str(uuid),
        "intent": intent,
        "transcript": transcript,
        "patient_info": patient_info,
        "fhir": fhir_data
    }