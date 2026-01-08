"""
fhir_generator.py
FHIR R4 resource generation for healthcare interoperability.
Converts extracted intents and data into FHIR-compliant resources.
"""

import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any
from dataclasses import dataclass

from app.intent_extractor import IntentType, UrgencyLevel


@dataclass
class FHIRCommunicationRequest:
    id: str
    status: str
    subject: str
    payload: List[str]
    authored_on: str
    category: str
    priority: str
    trace_id: str
    medications: List[str]
    symptoms: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "resourceType": "CommunicationRequest",
            "id": self.id,
            "status": self.status,
            "subject": {"reference": self.subject},
            "payload": [{"contentString": p} for p in self.payload],
            "authoredOn": self.authored_on,
            "category": [{"coding": [{"code": self.category}]}],
            "priority": self.priority,
            "identifier": [{"system": "urn:clarivox", "value": self.trace_id}],
            "extension": [
                {"url": "medications", "valueString": ",".join(self.medications)},
                {"url": "symptoms", "valueString": ",".join(self.symptoms)}
            ]
        }


@dataclass
class FHIRTask:
    id: str
    status: str
    intent: str
    priority: str
    for_reference: str
    execution_period: Dict[str, str]
    trace_id: str
    task_type: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "resourceType": "Task",
            "id": self.id,
            "status": self.status,
            "intent": self.intent,
            "priority": self.priority,
            "for": {"reference": self.for_reference},
            "executionPeriod": self.execution_period,
            "identifier": [{"system": "urn:clarivox", "value": self.trace_id}],
            "code": {"text": f"Follow-up for voicemail intent: {self.task_type}"}
        }


@dataclass
class MedicationRequest:
    id: str
    subject: str
    medication_codeable_concept: str
    authored_on: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "resourceType": "MedicationRequest",
            "id": self.id,
            "status": "active",
            "intent": "order",
            "subject": {"reference": self.subject},
            "medicationCodeableConcept": {"text": self.medication_codeable_concept},
            "authoredOn": self.authored_on
        }


@dataclass
class SymptomObservation:
    id: str
    subject: str
    code: str
    effective_datetime: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "resourceType": "Observation",
            "id": self.id,
            "status": "preliminary",
            "category": [{"coding": [{"code": "symptom"}]}],
            "code": {"text": self.code},
            "subject": {"reference": self.subject},
            "effectiveDateTime": self.effective_datetime
        }


class FHIRGenerator:
    def __init__(self):
        pass

    def generate_patient_reference(self, mrn: str) -> str:
        return f"Patient/{mrn}"

    def create_communication_request(
        self,
        transcript: str,
        intent: str,
        urgency: str,
        patient_ref: str,
        trace_id: str,
        medications: Optional[List[str]] = None,
        symptoms: Optional[List[str]] = None
    ) -> FHIRCommunicationRequest:
        return FHIRCommunicationRequest(
            id=f"commreq-{uuid.uuid4()}",
            status="active",
            subject=patient_ref,
            payload=[transcript],
            authored_on=datetime.utcnow().isoformat(),
            category=intent,
            priority=urgency,
            trace_id=trace_id,
            medications=medications or [],
            symptoms=symptoms or []
        )

    def create_task(
        self,
        intent: str,
        urgency: str,
        patient_ref: str,
        trace_id: str
    ) -> FHIRTask:
        return FHIRTask(
            id=f"task-{uuid.uuid4()}",
            status="requested",
            intent="order",
            priority=urgency,
            for_reference=patient_ref,
            execution_period={
                "start": datetime.utcnow().isoformat()
            },
            trace_id=trace_id,
            task_type=intent
        )

    def generate_medication_requests(
        self,
        medications: List[str],
        patient_ref: str
    ) -> List[MedicationRequest]:
        return [
            MedicationRequest(
                id=f"medreq-{uuid.uuid4()}",
                subject=patient_ref,
                medication_codeable_concept=med,
                authored_on=datetime.utcnow().isoformat()
            )
            for med in medications
        ]

    def generate_symptom_observations(
        self,
        symptoms: List[str],
        patient_ref: str
    ) -> List[SymptomObservation]:
        return [
            SymptomObservation(
                id=f"obs-{uuid.uuid4()}",
                subject=patient_ref,
                code=sym,
                effective_datetime=datetime.utcnow().isoformat()
            )
            for sym in symptoms
        ]


# Singleton instance
_generator = None


def get_fhir_generator() -> FHIRGenerator:
    global _generator
    if _generator is None:
        _generator = FHIRGenerator()
    return _generator


def generate_fhir_bundle(
    intent: str,
    urgency: str,
    patient_mrn: Optional[str],
    transcript: str,
    trace_id: str,
    medications: Optional[List[str]] = None,
    symptoms: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Generate a complete FHIR bundle with all relevant resources.
    
    Args:
        intent: The extracted intent classification
        urgency: Urgency level (emergent, urgent, semi_urgent, routine)
        patient_mrn: Patient Medical Record Number (can be None)
        transcript: The sanitized transcript text
        trace_id: Unique transaction trace ID
        medications: List of medication names (optional)
        symptoms: List of symptom descriptions (optional)
        
    Returns:
        Dict containing FHIR resources (CommunicationRequest, Task, etc.)
    """
    generator = get_fhir_generator()
    
    # Null-safe patient reference generation
    safe_mrn = patient_mrn if patient_mrn else "unknown"
    patient_ref = generator.generate_patient_reference(safe_mrn)
    
    # Ensure lists are never None
    safe_medications = medications if medications is not None else []
    safe_symptoms = symptoms if symptoms is not None else []
    safe_transcript = transcript if transcript else ""
    safe_intent = intent if intent else "unknown"
    safe_urgency = urgency if urgency else "routine"
    safe_trace_id = trace_id if trace_id else f"CLV-{uuid.uuid4().hex[:12].upper()}"

    # Create main communication request
    comm_request = generator.create_communication_request(
        transcript=safe_transcript,
        intent=safe_intent,
        urgency=safe_urgency,
        patient_ref=patient_ref,
        trace_id=safe_trace_id,
        medications=safe_medications,
        symptoms=safe_symptoms
    )

    # Create task for follow-up
    task = generator.create_task(
        intent=safe_intent,
        urgency=safe_urgency,
        patient_ref=patient_ref,
        trace_id=safe_trace_id
    )

    # Create medication requests if applicable
    med_requests = []
    if safe_medications:
        med_requests = generator.generate_medication_requests(safe_medications, patient_ref)

    # Create symptom observations if applicable
    observations = []
    if safe_symptoms:
        observations = generator.generate_symptom_observations(safe_symptoms, patient_ref)

    return {
        "trace_id": safe_trace_id,
        "intent": safe_intent,
        "urgency": safe_urgency,
        "communication_request": comm_request.to_dict(),
        "task": task.to_dict(),
        "medication_requests": [m.to_dict() for m in med_requests],
        "observations": [o.to_dict() for o in observations]
    }
