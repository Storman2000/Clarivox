"""
intent_extractor.py
NLP logic for extracting clinical intents, urgency levels, medications, and symptoms
from transcribed voicemail text.
"""

import re
from typing import List, Optional
from uuid import uuid4
from dataclasses import dataclass
import logging
import spacy

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    # If model not found, download it
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

logger = logging.getLogger(__name__)


# --- ENUM-LIKE CLASSES ---
class IntentType:
    MEDICATION_REFILL = "medication_refill"
    MEDICATION_SIDE_EFFECT = "medication_side_effect"
    MEDICATION_QUESTION = "medication_question"
    APPOINTMENT_SCHEDULE = "appointment_schedule"
    APPOINTMENT_CANCEL = "appointment_cancel"
    APPOINTMENT_RESCHEDULE = "appointment_reschedule"
    APPOINTMENT_CONFIRM = "appointment_confirm"
    SYMPTOM_REPORT = "symptom_report"
    TEST_RESULTS = "test_results"
    BENEFITS_INQUIRY = "benefits_inquiry"
    BENEFITS_CLAIM = "benefits_claim"
    CALLBACK_REQUEST = "callback_request"
    GENERAL_INQUIRY = "general_inquiry"
    COMPLAINT = "complaint"
    CRISIS_SUICIDE = "crisis_suicide"
    CRISIS_SELF_HARM = "crisis_self_harm"
    CRISIS_VIOLENCE = "crisis_violence"
    UNKNOWN = "unknown"


class UrgencyLevel:
    EMERGENT = "emergent"
    URGENT = "urgent"
    SEMI_URGENT = "semi_urgent"
    ROUTINE = "routine"


# --- DATA CLASSES ---
@dataclass
class Entity:
    text: str
    confidence: float = 1.0
    negated: bool = False


@dataclass
class TemporalExpression:
    text: str
    resolved_date: Optional[str] = None


@dataclass
class IntentExtractionResult:
    primary_intent: str
    secondary_intents: List[str]
    urgency: str
    intent_confidence: float
    urgency_confidence: float
    medications: List[Entity]
    symptoms: List[Entity]
    temporal_expressions: List[TemporalExpression]
    crisis_indicators: List[str]
    negation_detected: bool
    transcript: str
    trace_id: str

    def to_dict(self):
        return {
            "primary_intent": self.primary_intent,
            "secondary_intents": self.secondary_intents,
            "urgency": self.urgency,
            "intent_confidence": self.intent_confidence,
            "urgency_confidence": self.urgency_confidence,
            "medications": [{"text": m.text, "confidence": m.confidence, "negated": m.negated} for m in self.medications],
            "symptoms": [{"text": s.text, "confidence": s.confidence, "negated": s.negated} for s in self.symptoms],
            "temporal_expressions": [{"text": t.text, "resolved_date": t.resolved_date} for t in self.temporal_expressions],
            "crisis_indicators": self.crisis_indicators,
            "negation_detected": self.negation_detected,
            "transcript": self.transcript,
            "trace_id": self.trace_id
        }


# --- CORE SERVICE ---
class IntentExtractionService:
    def __init__(self):
        self.intent_patterns = {
            IntentType.MEDICATION_REFILL: [r"refill.*prescription", r"ran out.*medication", r"need.*refill", r"prescription.*refill"],
            IntentType.APPOINTMENT_SCHEDULE: [r"schedule.*appointment", r"book.*visit", r"make.*appointment", r"set up.*appointment"],
            IntentType.APPOINTMENT_RESCHEDULE: [r"reschedule.*appointment", r"change.*appointment", r"move.*appointment"],
            IntentType.APPOINTMENT_CANCEL: [r"cancel.*appointment", r"cancel.*visit"],
            IntentType.SYMPTOM_REPORT: [r"chest pain", r"shortness of breath", r"fever", r"feeling.*sick", r"not feeling well"],
            IntentType.TEST_RESULTS: [r"test results", r"lab results", r"blood work", r"results.*back"],
            IntentType.CRISIS_SUICIDE: [r"end my life", r"kill myself", r"suicidal", r"want to die"],
            IntentType.CRISIS_SELF_HARM: [r"hurt myself", r"self harm", r"cutting"],
            IntentType.CALLBACK_REQUEST: [r"call me back", r"give me a call", r"return.*call", r"callback"]
        }

        self.urgency_patterns = {
            UrgencyLevel.EMERGENT: [r"can't breathe", r"suicidal", r"kill myself", r"chest pain", r"emergency"],
            UrgencyLevel.URGENT: [r"severe pain", r"ASAP", r"urgent", r"as soon as possible", r"right away"],
            UrgencyLevel.SEMI_URGENT: [r"this week", r"soon", r"when possible"],
        }

        self.common_meds = {"lisinopril", "atorvastatin", "metformin", "amlodipine", "omeprazole",
                          "losartan", "gabapentin", "hydrochlorothiazide", "levothyroxine", "simvastatin"}
        
        self.common_symptoms = {"pain", "headache", "fever", "chest pain", "shortness of breath",
                               "nausea", "dizziness", "fatigue", "cough", "sore throat"}

    def extract(self, transcript: str, trace_id: Optional[str] = None) -> IntentExtractionResult:
        trace_id = trace_id or f"CLV-{uuid4().hex[:12].upper()}"
        doc = nlp(transcript)

        primary_intent = IntentType.UNKNOWN
        secondary_intents = []
        confidence = 0.5
        urgency = UrgencyLevel.ROUTINE
        urgency_confidence = 0.5
        medications = []
        symptoms = []
        temporal_expressions = []
        crisis_indicators = []
        negation_detected = False

        # Check intent patterns
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, transcript, re.IGNORECASE):
                    if primary_intent == IntentType.UNKNOWN:
                        primary_intent = intent
                        confidence = 0.9
                    else:
                        secondary_intents.append(intent)

        # Check urgency patterns
        for level, patterns in self.urgency_patterns.items():
            for pattern in patterns:
                if re.search(pattern, transcript, re.IGNORECASE):
                    urgency = level
                    urgency_confidence = 0.9
                    break

        # Extract medications and symptoms from tokens
        for token in doc:
            if token.text.lower() in self.common_meds:
                medications.append(Entity(text=token.text, confidence=0.9))
            if token.text.lower() in self.common_symptoms:
                negated = self._check_negation(token)
                if negated:
                    negation_detected = True
                symptoms.append(Entity(text=token.text, confidence=0.9, negated=negated))

        # Check for multi-word symptoms
        transcript_lower = transcript.lower()
        for symptom in self.common_symptoms:
            if " " in symptom and symptom in transcript_lower:
                symptoms.append(Entity(text=symptom, confidence=0.9, negated=False))

        # Crisis detection
        if re.search(r"(suicide|kill myself|gun|knife|end my life)", transcript, re.IGNORECASE):
            crisis_indicators.append("potential_crisis")

        # Temporal expressions (basic)
        date_patterns = [r"\b(tomorrow|today|next week|this week|monday|tuesday|wednesday|thursday|friday)\b"]
        for pattern in date_patterns:
            matches = re.findall(pattern, transcript, re.IGNORECASE)
            for match in matches:
                temporal_expressions.append(TemporalExpression(text=match))

        return IntentExtractionResult(
            primary_intent=primary_intent,
            secondary_intents=secondary_intents,
            urgency=urgency,
            intent_confidence=confidence,
            urgency_confidence=urgency_confidence,
            medications=medications,
            symptoms=symptoms,
            temporal_expressions=temporal_expressions,
            crisis_indicators=crisis_indicators,
            negation_detected=negation_detected,
            transcript=transcript,
            trace_id=trace_id
        )

    def _check_negation(self, token):
        for child in token.children:
            if child.dep_ == "neg":
                return True
        for ancestor in token.ancestors:
            for child in ancestor.children:
                if child.dep_ == "neg":
                    return True
        return False


# Factory
_service = None


def get_intent_service():
    global _service
    if _service is None:
        _service = IntentExtractionService()
    return _service
