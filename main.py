from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from datetime import datetime
import uuid
import os
import shutil
import whisper

app = FastAPI()

# ------------------- Data Models -------------------
class TranscriptionResult(BaseModel):
    transcript: str
    urgency: str
    intent: str
    patient_name: str
    patient_id: str

class FHIRCommunicationRequest(BaseModel):
    resourceType: str = "CommunicationRequest"
    status: str = "active"
    intent: str = "proposal"
    subject: dict
    requester: dict
    authoredOn: str
    payload: list

class FHIRTask(BaseModel):
    resourceType: str = "Task"
    status: str = "requested"
    intent: str = "order"
    priority: str
    for_: dict
    authoredOn: str
    description: str

# ------------------- Routes -------------------
@app.post("/voicemail/upload")
async def upload_voicemail(file: UploadFile = File(...)):
    temp_path = f"/tmp/{uuid.uuid4().hex}_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Load Whisper model once (assumes 'base' is already downloaded via CLI or cached)
    model = whisper.load_model("base")  # Will load from ~/.cache/whisper automatically
    result = model.transcribe(temp_path)
    transcript = result['text']
    os.remove(temp_path)

    # Simulated NLP
    triage = TranscriptionResult(
        transcript=transcript,
        urgency="low",
        intent="reschedule" if "reschedule" in transcript.lower() else "other",
        patient_name="John Smith",
        patient_id="12345"
    )

    # FHIR output
    if triage.intent == "reschedule":
        fhir_resource = FHIRCommunicationRequest(
            subject={"reference": f"Patient/{triage.patient_id}"},
            requester={"reference": "Practitioner/VA-Agent-001"},
            authoredOn=datetime.utcnow().isoformat(),
            payload=[{"contentString": triage.transcript}]
        )
    else:
        fhir_resource = FHIRTask(
            priority=triage.urgency,
            for_={"reference": f"Patient/{triage.patient_id}"},
            authoredOn=datetime.utcnow().isoformat(),
            description=triage.transcript
        )

    return {"status": "success", "FHIR": fhir_resource.dict()}
