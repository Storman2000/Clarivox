"""
mock_services.py
Mock external service endpoints for development and testing.
Simulates responses from Cerner, VistA, and REACH VET systems.
"""

from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


def mock_cerner_appointment_api(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Mock Cerner Appointments API response."""
    logger.info(f"[Mock] Routing to Cerner Appointments API with payload: {payload.get('trace_id', 'N/A')}")
    return {
        "status": "success",
        "system": "Cerner",
        "action": "appointment_scheduled",
        "trace_id": payload.get("trace_id", "N/A"),
        "message": "Appointment request processed successfully"
    }


def mock_vista_refill_api(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Mock VistA Medication Refill API response."""
    logger.info(f"[Mock] Routing to VistA Refill API with payload: {payload.get('trace_id', 'N/A')}")
    return {
        "status": "success",
        "system": "VistA",
        "action": "medication_refill_processed",
        "trace_id": payload.get("trace_id", "N/A"),
        "message": "Medication refill request queued"
    }


def mock_reach_vet_crisis_flag(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Mock REACH VET Crisis Flag API response."""
    logger.warning(f"[Mock] Crisis flag sent to REACH VET with payload: {payload.get('trace_id', 'N/A')}")
    return {
        "status": "success",
        "system": "REACH_VET",
        "action": "crisis_flagged",
        "trace_id": payload.get("trace_id", "N/A"),
        "message": "Crisis intervention initiated",
        "priority": "EMERGENT"
    }


def mock_nurse_triage_api(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Mock Nurse Triage Queue API response."""
    logger.info(f"[Mock] Routing to Nurse Triage with payload: {payload.get('trace_id', 'N/A')}")
    return {
        "status": "success",
        "system": "NURSE_TRIAGE",
        "action": "triage_queued",
        "trace_id": payload.get("trace_id", "N/A"),
        "message": "Patient added to nurse triage queue"
    }


def mock_general_callback_api(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Mock General Callback Queue API response."""
    logger.info(f"[Mock] Routing to General Callback with payload: {payload.get('trace_id', 'N/A')}")
    return {
        "status": "success",
        "system": "GENERAL_CALLBACK",
        "action": "callback_queued",
        "trace_id": payload.get("trace_id", "N/A"),
        "message": "Callback request added to queue"
    }


def route_to_mock_system(system_code: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Route to the appropriate mock system based on system code.
    
    Args:
        system_code: Target system identifier
        payload: Data to send to the system
        
    Returns:
        Mock response from the target system
    """
    routing_map = {
        "CERNER_APPOINTMENTS": mock_cerner_appointment_api,
        "VISTA_REFILL": mock_vista_refill_api,
        "REACH_VET": mock_reach_vet_crisis_flag,
        "NURSE_TRIAGE": mock_nurse_triage_api,
        "GENERAL_CALLBACK": mock_general_callback_api,
        "LAB_RESULTS": mock_general_callback_api,
        "CRISIS_LINE": mock_reach_vet_crisis_flag,
        "SECURITY": mock_reach_vet_crisis_flag
    }

    handler = routing_map.get(system_code)
    
    if handler:
        return handler(payload)
    else:
        logger.error(f"[Mock] Unknown system code: {system_code}")
        return {
            "status": "error",
            "message": f"Unknown routing system: {system_code}",
            "trace_id": payload.get("trace_id", "N/A")
        }


def process_routing(targets: list, payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process routing to all target systems.
    
    Args:
        targets: List of target system codes
        payload: Data to send to systems
        
    Returns:
        Combined routing results
    """
    results = {}
    for target in targets:
        results[target] = route_to_mock_system(target, payload)
    return results
