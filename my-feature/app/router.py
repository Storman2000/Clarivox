"""
router.py
Routing logic for directing processed voicemails to appropriate backend systems.
Determines routing targets based on intent classification.
"""

import logging
from typing import Dict, Any, List
from app.intent_extractor import IntentType

logger = logging.getLogger(__name__)


# Routing configurations
ROUTING_RULES = {
    IntentType.MEDICATION_REFILL: {
        "primary": "VISTA_REFILL",
        "secondary": [],
        "description": "Route to VistA medication refill system"
    },
    IntentType.APPOINTMENT_SCHEDULE: {
        "primary": "CERNER_APPOINTMENTS",
        "secondary": [],
        "description": "Route to Cerner appointment scheduling"
    },
    IntentType.APPOINTMENT_RESCHEDULE: {
        "primary": "CERNER_APPOINTMENTS",
        "secondary": [],
        "description": "Route to Cerner appointment scheduling"
    },
    IntentType.APPOINTMENT_CANCEL: {
        "primary": "CERNER_APPOINTMENTS",
        "secondary": [],
        "description": "Route to Cerner appointment scheduling"
    },
    IntentType.CRISIS_SUICIDE: {
        "primary": "REACH_VET",
        "secondary": ["CRISIS_LINE"],
        "description": "Route to REACH VET crisis intervention"
    },
    IntentType.CRISIS_SELF_HARM: {
        "primary": "REACH_VET",
        "secondary": ["CRISIS_LINE"],
        "description": "Route to REACH VET crisis intervention"
    },
    IntentType.CRISIS_VIOLENCE: {
        "primary": "REACH_VET",
        "secondary": ["SECURITY"],
        "description": "Route to REACH VET with security alert"
    },
    IntentType.SYMPTOM_REPORT: {
        "primary": "NURSE_TRIAGE",
        "secondary": [],
        "description": "Route to nurse triage queue"
    },
    IntentType.TEST_RESULTS: {
        "primary": "LAB_RESULTS",
        "secondary": [],
        "description": "Route to lab results callback queue"
    },
    IntentType.CALLBACK_REQUEST: {
        "primary": "GENERAL_CALLBACK",
        "secondary": [],
        "description": "Route to general callback queue"
    },
    IntentType.GENERAL_INQUIRY: {
        "primary": "GENERAL_CALLBACK",
        "secondary": [],
        "description": "Route to general callback queue"
    }
}


def determine_routing_targets(intent: str) -> Dict[str, Any]:
    """
    Determine routing targets based on the extracted intent.
    
    Args:
        intent (str): The primary intent classification
        
    Returns:
        Dict containing routing information
    """
    routing_info = ROUTING_RULES.get(intent, {
        "primary": "GENERAL_CALLBACK",
        "secondary": [],
        "description": "Default routing to general callback queue"
    })

    logger.info(f"Routing intent '{intent}' to primary: {routing_info['primary']}")

    return {
        "primary_target": routing_info["primary"],
        "secondary_targets": routing_info["secondary"],
        "description": routing_info["description"],
        "intent": intent
    }


def get_all_routing_targets(intent_result) -> List[str]:
    """
    Get all routing targets (primary + secondary) for an intent result.
    
    Args:
        intent_result: IntentExtractionResult object
        
    Returns:
        List of all target system codes
    """
    routing = determine_routing_targets(intent_result.primary_intent)
    targets = [routing["primary_target"]] + routing["secondary_targets"]
    
    # Add crisis routing if crisis indicators detected
    if intent_result.crisis_indicators:
        if "REACH_VET" not in targets:
            targets.append("REACH_VET")
    
    return targets


def build_routing_payload(
    intent_result,
    trace_id: str,
    transcript: str,
    fhir_bundle: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Build the payload to be sent to routing targets.
    
    Args:
        intent_result: IntentExtractionResult object
        trace_id: Unique trace identifier
        transcript: The sanitized transcript
        fhir_bundle: Generated FHIR bundle
        
    Returns:
        Dict containing the routing payload
    """
    return {
        "trace_id": trace_id,
        "intent": intent_result.primary_intent,
        "urgency": intent_result.urgency,
        "transcript": transcript,
        "medications": [m.text for m in intent_result.medications],
        "symptoms": [s.text for s in intent_result.symptoms if not s.negated],
        "crisis_indicators": intent_result.crisis_indicators,
        "fhir_bundle": fhir_bundle
    }
