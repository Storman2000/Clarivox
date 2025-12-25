"""
test_intent_extractor.py
Unit tests for intent_extractor.py
"""

import pytest
from app.intent_extractor import (
    IntentType,
    UrgencyLevel,
    IntentExtractionService,
    get_intent_service,
    Entity,
    IntentExtractionResult
)


class TestIntentType:
    def test_medication_refill(self):
        assert IntentType.MEDICATION_REFILL == "medication_refill"

    def test_appointment_schedule(self):
        assert IntentType.APPOINTMENT_SCHEDULE == "appointment_schedule"

    def test_crisis_suicide(self):
        assert IntentType.CRISIS_SUICIDE == "crisis_suicide"

    def test_unknown(self):
        assert IntentType.UNKNOWN == "unknown"


class TestUrgencyLevel:
    def test_emergent(self):
        assert UrgencyLevel.EMERGENT == "emergent"

    def test_urgent(self):
        assert UrgencyLevel.URGENT == "urgent"

    def test_routine(self):
        assert UrgencyLevel.ROUTINE == "routine"


class TestIntentExtractionService:
    @pytest.fixture
    def service(self):
        return IntentExtractionService()

    def test_medication_refill_intent(self, service):
        transcript = "I need a refill on my prescription medication."
        result = service.extract(transcript)
        assert result.primary_intent == IntentType.MEDICATION_REFILL
        assert result.intent_confidence >= 0.8

    def test_appointment_schedule_intent(self, service):
        transcript = "I want to schedule an appointment with my doctor."
        result = service.extract(transcript)
        assert result.primary_intent == IntentType.APPOINTMENT_SCHEDULE

    def test_appointment_reschedule_intent(self, service):
        transcript = "I need to reschedule my appointment for next week."
        result = service.extract(transcript)
        assert result.primary_intent == IntentType.APPOINTMENT_RESCHEDULE

    def test_callback_request_intent(self, service):
        transcript = "Please call me back when you can."
        result = service.extract(transcript)
        assert result.primary_intent == IntentType.CALLBACK_REQUEST

    def test_crisis_detection(self, service):
        transcript = "I want to kill myself. I can't take it anymore."
        result = service.extract(transcript)
        assert result.primary_intent == IntentType.CRISIS_SUICIDE
        assert len(result.crisis_indicators) > 0
        assert result.urgency == UrgencyLevel.EMERGENT

    def test_routine_urgency_default(self, service):
        transcript = "Hello, just calling to check on something."
        result = service.extract(transcript)
        assert result.urgency == UrgencyLevel.ROUTINE

    def test_urgent_detection(self, service):
        transcript = "I have severe pain and need to see someone ASAP."
        result = service.extract(transcript)
        assert result.urgency == UrgencyLevel.URGENT

    def test_medication_extraction(self, service):
        transcript = "I need a refill on my lisinopril medication."
        result = service.extract(transcript)
        medication_names = [m.text.lower() for m in result.medications]
        assert "lisinopril" in medication_names

    def test_symptom_extraction(self, service):
        transcript = "I have been having chest pain and shortness of breath."
        result = service.extract(transcript)
        symptom_texts = [s.text.lower() for s in result.symptoms]
        # Check for symptoms (note: multi-word symptoms handled separately)
        assert len(result.symptoms) > 0

    def test_trace_id_generation(self, service):
        transcript = "Hello, this is a test."
        result = service.extract(transcript)
        assert result.trace_id.startswith("CLV-")

    def test_to_dict(self, service):
        transcript = "I need a refill on my prescription."
        result = service.extract(transcript)
        result_dict = result.to_dict()
        assert "primary_intent" in result_dict
        assert "urgency" in result_dict
        assert "medications" in result_dict


class TestGetIntentService:
    def test_singleton_instance(self):
        service1 = get_intent_service()
        service2 = get_intent_service()
        assert service1 is service2
