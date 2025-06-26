from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from datetime import datetime
import uuid

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
    # Simulated transcription (replace with Whisper/Deepgram call)
    transcript = "Hi, I need to reschedule my cardiology appointment. This is John Smith."

    # Simulated NLP extraction (normally done via spaCy or transformers)
    triage = TranscriptionResult(
        transcript=transcript,
        urgency="low",
        intent="reschedule",
        patient_name="John Smith",
        patient_id="12345"
    )

    # Create FHIR resource
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
