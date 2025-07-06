from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from datetime import datetime
import uuid
import os
import whisper
import json

app = FastAPI()

# ------------------- Data Models -------------------

class TranscriptionResult(BaseModel):
transcript: str
urgency: str
intent: str
patient\_name: str
patient\_id: str

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
for\_: dict
authoredOn: str
description: str

# ------------------- Routes -------------------

@app.post("/voicemail/upload")
async def upload\_voicemail(file: UploadFile = File(...)):
contents = await file.read()
temp\_path = f"temp\_{uuid.uuid4().hex}.m4a"
with open(temp\_path, "wb") as f:
f.write(contents)

```
# --- Actual Transcription using local Whisper model ---
model = whisper.load_model("base", download_root=os.path.expanduser("~/.cache/whisper"))
result = model.transcribe(temp_path)
transcript = result["text"]
os.remove(temp_path)

# Simulated NLP extraction
triage = TranscriptionResult(
    transcript=transcript,
    urgency="low",
    intent="reschedule" if "reschedule" in transcript.lower() else "other",
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