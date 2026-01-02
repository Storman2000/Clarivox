"""
test_fhir_generator.py
Unit tests for fhir_generator.py
"""

import pytest
from app.fhir_generator import (
    FHIRGenerator,
    get_fhir_generator,
    generate_fhir_bundle,
    FHIRCommunicationRequest,
    FHIRTask,
    MedicationRequest,
    SymptomObservation
)


class TestFHIRGenerator:
    @pytest.fixture
    def generator(self):
        return FHIRGenerator()

    def test_generate_patient_reference(self, generator):
        result = generator.generate_patient_reference("12345")
        assert result == "Patient/12345"

    def test_create_communication_request(self, generator):
        result = generator.create_communication_request(
            transcript="Test transcript",
            intent="medication_refill",
            urgency="routine",
            patient_ref="Patient/12345",
            trace_id="CLV-TEST123",
            medications=["lisinopril"],
            symptoms=["headache"]
        )
        assert isinstance(result, FHIRCommunicationRequest)
        assert result.status == "active"
        assert result.subject == "Patient/12345"
        assert "lisinopril" in result.medications

    def test_create_task(self, generator):
        result = generator.create_task(
            intent="appointment_schedule",
            urgency="routine",
            patient_ref="Patient/12345",
            trace_id="CLV-TEST123"
        )
        assert isinstance(result, FHIRTask)
        assert result.status == "requested"
        assert result.intent == "order"

    def test_generate_medication_requests(self, generator):
        result = generator.generate_medication_requests(
            medications=["lisinopril", "metformin"],
            patient_ref="Patient/12345"
        )
        assert len(result) == 2
        assert all(isinstance(r, MedicationRequest) for r in result)

    def test_generate_symptom_observations(self, generator):
        result = generator.generate_symptom_observations(
            symptoms=["headache", "fever"],
            patient_ref="Patient/12345"
        )
        assert len(result) == 2
        assert all(isinstance(r, SymptomObservation) for r in result)


class TestFHIRCommunicationRequest:
    def test_to_dict(self):
        comm_request = FHIRCommunicationRequest(
            id="test-id",
            status="active",
            subject="Patient/123",
            payload=["Test transcript"],
            authored_on="2024-01-01T00:00:00",
            category="medication_refill",
            priority="routine",
            trace_id="CLV-TEST",
            medications=["lisinopril"],
            symptoms=["headache"]
        )
        result = comm_request.to_dict()
        assert result["resourceType"] == "CommunicationRequest"
        assert result["status"] == "active"


class TestFHIRTask:
    def test_to_dict(self):
        task = FHIRTask(
            id="test-task-id",
            status="requested",
            intent="order",
            priority="routine",
            for_reference="Patient/123",
            execution_period={"start": "2024-01-01T00:00:00"},
            trace_id="CLV-TEST",
            task_type="medication_refill"
        )
        result = task.to_dict()
        assert result["resourceType"] == "Task"
        assert result["status"] == "requested"


class TestGenerateFhirBundle:
    def test_bundle_creation(self):
        result = generate_fhir_bundle(
            intent="medication_refill",
            urgency="routine",
            patient_mrn="12345",
            transcript="Test transcript",
            trace_id="CLV-TEST123",
            medications=["lisinopril"],
            symptoms=["headache"]
        )
        assert "trace_id" in result
        assert "communication_request" in result
        assert "task" in result
        assert "medication_requests" in result
        assert "observations" in result

    def test_bundle_with_no_medications(self):
        result = generate_fhir_bundle(
            intent="appointment_schedule",
            urgency="routine",
            patient_mrn=None,
            transcript="Test transcript",
            trace_id="CLV-TEST123"
        )
        assert result["medication_requests"] == []

    def test_bundle_unknown_patient(self):
        result = generate_fhir_bundle(
            intent="general_inquiry",
            urgency="routine",
            patient_mrn=None,
            transcript="Test",
            trace_id="CLV-TEST"
        )
        assert "unknown" in result["communication_request"]["subject"]["reference"]


class TestGetFhirGenerator:
    def test_singleton_instance(self):
        gen1 = get_fhir_generator()
        gen2 = get_fhir_generator()
        assert gen1 is gen2
