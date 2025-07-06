from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from datetime import datetime
import uuid
import os
import whisper
import json
import traceback

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
    try:
        contents = await file.read()
        temp_path = f"temp_{uuid.uuid4().hex}.m4a"
        with open(temp_path, "wb") as f:
            f.write(contents)

        # Load model from local disk (bypass SSL/download issues)
        model = whisper.load_model(os.path.expanduser("~/.cache/whisper/whisper-base.pt"))

        result = model.transcribe(temp_path)
        transcript = result["text"]
        os.remove(temp_path)

        triage = TranscriptionResult(
            transcript=transcript,
            urgency="low",
            intent="reschedule" if "reschedule" in transcript.lower() else "other",
            patient_name="John Smith",
            patient_id="12345"
        )

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

        os.makedirs("data", exist_ok=True)
        base_filename = f"data/{uuid.uuid4().hex}"

        with open(f"{base_filename}_transcript.txt", "w") as tf:
            tf.write(triage.transcript)

        with open(f"{base_filename}_fhir.json", "w") as jf:
            json.dump(fhir_resource.dict(), jf, indent=2)

        return {"status": "success", "FHIR": fhir_resource.dict()}

    except Exception as e:
        traceback.print_exc()
        return {"status": "error", "detail": str(e)}