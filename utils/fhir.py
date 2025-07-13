# utils/fhir.py

from datetime import datetime

def build_communication_request(transcript: str, uuid, patient_info: dict) -> dict:
    return {
        "resourceType": "CommunicationRequest",
        "status": "active",
        "intent": "order",
        "authoredOn": datetime.utcnow().isoformat(),
        "subject": {
            "reference": f"Patient/{patient_info.get('identifier', 'unknown')}",
            "display": patient_info.get("full_name", "Unknown")
        },
        "payload": [
            {
                "contentString": transcript
            }
        ],
        "identifier": [
            {
                "system": "urn:clarivox",
                "value": str(uuid)
            }
        ]
    }