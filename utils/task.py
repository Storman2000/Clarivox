from uuid import UUID
from typing import Optional
from datetime import datetime

def build_task(transcription: str, uuid: UUID, intent: Optional[str] = None) -> dict:
    return {
        "resourceType": "Task",
        "status": "requested",
        "intent": "order",
        "priority": "routine",
        "authoredOn": datetime.utcnow().isoformat(),
        "description": transcription,
        "identifier": [{"system": "urn:clarivox", "value": str(uuid)}],
        "code": {
            "text": f"Follow-up for voicemail intent: {intent or 'unspecified'}"
        }
    }