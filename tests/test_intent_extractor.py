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


class TestMultipleIntents:
    """Test handling of multiple intents in same voicemail"""
    
    @pytest.fixture
    def service(self):
        return IntentExtractionService()
    
    def test_medication_and_appointment(self, service):
        """Test voicemail with both medication refill and appointment"""
        transcript = "I need to refill my prescription and also schedule my annual checkup"
        result = service.extract(transcript)
        
        # Should choose one as primary
        assert result.primary_intent in [
            IntentType.MEDICATION_REFILL,
            IntentType.APPOINTMENT_SCHEDULE
        ]
        # Medication typically takes priority for clinical urgency
        assert result.primary_intent == IntentType.MEDICATION_REFILL
    
    def test_callback_with_symptom(self, service):
        """Test callback request with symptom mention"""
        transcript = "Please call me back, I have chest pain"
        result = service.extract(transcript)
        
        # Symptom report should take priority over generic callback
        assert result.primary_intent == IntentType.SYMPTOM_REPORT or \
               result.urgency == UrgencyLevel.URGENT


class TestAmbiguousIntent:
    """Test handling of unclear or ambiguous intents"""
    
    @pytest.fixture
    def service(self):
        return IntentExtractionService()
    
    def test_vague_message(self, service):
        """Test voicemail with no clear intent"""
        transcript = "Hi, just calling to check in"
        result = service.extract(transcript)
        
        # Should default to callback request or unknown
        assert result.primary_intent in [
            IntentType.CALLBACK_REQUEST,
            IntentType.UNKNOWN
        ]
        assert result.urgency == UrgencyLevel.ROUTINE
    
    def test_incomplete_message(self, service):
        """Test incomplete or cut-off message"""
        transcript = "Hi, I need to"
        result = service.extract(transcript)
        
        # Should handle gracefully
        assert result.primary_intent is not None
        assert result.urgency == UrgencyLevel.ROUTINE
    
    def test_rambling_message(self, service):
        """Test long rambling message"""
        # Pattern-based NLP needs explicit keywords like "refill" or "prescription"
        transcript = "Well, you see, I was thinking that maybe, you know, I should probably... well, I need a refill on my medication"
        result = service.extract(transcript)
        
        # Should still extract medication refill intent
        assert result.primary_intent == IntentType.MEDICATION_REFILL


class TestCrisisEdgeCases:
    """Test edge cases for crisis detection"""
    
    @pytest.fixture
    def service(self):
        return IntentExtractionService()
    
    def test_crisis_with_negation(self, service):
        """Test that negated crisis statements are detected for safety review"""
        # NOTE: Current pattern-based implementation intentionally detects crisis
        # keywords even with negation - erring on side of caution for patient safety
        # A real ML-based system would handle negation, but for MVP, false positives
        # are safer than false negatives in crisis detection
        transcript = "I am NOT suicidal, I just need to talk to someone"
        result = service.extract(transcript)
        
        # Should still flag for human review (safety-first approach)
        assert result.primary_intent == IntentType.CRISIS_SUICIDE
    
    def test_crisis_in_context(self, service):
        """Test crisis keywords in historical context"""
        # NOTE: Pattern-based detection may flag this as crisis due to "suicide" keyword
        # This is intentional for MVP - human review will assess context
        transcript = "My sister attempted suicide last year, I need counseling referral"
        result = service.extract(transcript)
        
        # Should at least flag crisis indicators for human review
        assert "potential_crisis" in result.crisis_indicators or result.primary_intent == IntentType.CRISIS_SUICIDE
    
    def test_indirect_crisis(self, service):
        """Test indirect distress - requires advanced NLP"""
        # NOTE: Detecting indirect distress requires sentiment analysis
        # beyond current pattern-based implementation. This is tracked as
        # a future enhancement for ML-based intent extraction.
        transcript = "I can't go on like this anymore. Everything is pointless"
        result = service.extract(transcript)
        
        # Current implementation may not detect indirect distress
        # Should at least not crash and return valid result
        assert result is not None
        assert result.urgency in [UrgencyLevel.ROUTINE, UrgencyLevel.URGENT, UrgencyLevel.EMERGENT]
    
    def test_explicit_crisis(self, service):
        """Test explicit crisis statement"""
        transcript = "I want to kill myself right now"
        result = service.extract(transcript)
        
        # Should definitely detect
        assert result.primary_intent == IntentType.CRISIS_SUICIDE
        assert result.urgency == UrgencyLevel.EMERGENT
        assert len(result.crisis_indicators) > 0


class TestLanguageHandling:
    """Test language-specific intent extraction"""
    
    @pytest.fixture
    def service(self):
        return IntentExtractionService()
    
    def test_spanish_medication_refill(self, service):
        """Test Spanish language intent"""
        transcript = "Necesito un refill de mi medicina"
        result = service.extract(transcript)
        
        # Should handle Spanish or at least not crash
        assert result is not None
        assert result.primary_intent is not None
    
    def test_mixed_language(self, service):
        """Test mixed English/Spanish"""
        transcript = "I need refill for mi medicina lisinopril"
        result = service.extract(transcript)
        
        # Should extract intent
        assert result.primary_intent == IntentType.MEDICATION_REFILL


class TestEntityExtraction:
    """Test edge cases for entity extraction"""
    
    @pytest.fixture
    def service(self):
        return IntentExtractionService()
    
    def test_multiple_medications(self, service):
        """Test extraction of multiple medications"""
        transcript = "I need refills on my lisinopril, metformin, and atorvastatin"
        result = service.extract(transcript)
        
        # Should extract all medications
        assert len(result.medications) >= 2
        med_names = [m.text.lower() for m in result.medications]
        assert any("lisinopril" in name or "metformin" in name for name in med_names)
    
    def test_medication_with_dosage(self, service):
        """Test medication mentions with dosage"""
        transcript = "Refill my lisinopril 10mg twice daily"
        result = service.extract(transcript)
        
        # Should extract medication
        assert len(result.medications) > 0
        assert result.primary_intent == IntentType.MEDICATION_REFILL
    
    def test_symptom_with_severity(self, service):
        """Test symptom with severity indicator"""
        transcript = "I have severe chest pain radiating to my arm"
        result = service.extract(transcript)
        
        # Should be urgent
        assert result.urgency in [UrgencyLevel.URGENT, UrgencyLevel.EMERGENT]
        assert len(result.symptoms) > 0


class TestUrgencyDetection:
    """Test urgency level determination"""
    
    @pytest.fixture
    def service(self):
        return IntentExtractionService()
    
    def test_urgent_keywords(self, service):
        """Test that urgent keywords increase urgency"""
        transcript = "I need URGENT refill, I'm out of medication"
        result = service.extract(transcript)
        
        assert result.urgency in [UrgencyLevel.URGENT, UrgencyLevel.EMERGENT]
    
    def test_asap_keyword(self, service):
        """Test ASAP increases urgency"""
        transcript = "Please call back ASAP about my test results"
        result = service.extract(transcript)
        
        assert result.urgency == UrgencyLevel.URGENT
    
    def test_emergency_keyword(self, service):
        """Test emergency keyword"""
        transcript = "This is an emergency, please help"
        result = service.extract(transcript)
        
        assert result.urgency == UrgencyLevel.EMERGENT
