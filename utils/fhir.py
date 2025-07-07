from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CommunicationRequest(BaseModel):
    resourceType: str = "CommunicationRequest"
    status: str = "active"
    intent: str = "order"
    subject: dict = {"reference": "Patient/example"}  # Placeholder
    authoredOn: str = datetime.utcnow().isoformat()
    payload: list

def build_communication_request(transcript: str) -> CommunicationRequest:
    return CommunicationRequest(
        payload=[{"contentString": transcript}]
    )