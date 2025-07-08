from fastapi import FastAPI, UploadFile, File
from uuid import uuid4
from pathlib import Path
import whisper
from utils.fhir import build_communication_request
from utils.task import build_task
from utils.storage import save_outputs
import os

app = FastAPI()
model = whisper.load_model("base", download_root=os.path.expanduser("~/.cache/whisper"))

@app.post("/transcribe/")
async def transcribe_audio(file: UploadFile = File(...)):
    file_bytes = await file.read()
    uid = uuid4()
    temp_file_path = f"temp_{uid}.m4a"
    with open(temp_file_path, "wb") as f:
        f.write(file_bytes)

    result = model.transcribe(temp_file_path)
    transcription = result["text"]

    # Simple intent logic
    if "reschedule" in transcription.lower():
        fhir_resource = build_communication_request(transcription, uid)
    else:
        fhir_resource = build_task(transcription, uid)

    save_outputs(uid, transcription, fhir_resource)
    Path(temp_file_path).unlink(missing_ok=True)

    return fhir_resource