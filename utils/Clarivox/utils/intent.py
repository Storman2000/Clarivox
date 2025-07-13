# utils/intent.py

def extract_intent(transcript: str) -> str:
    t = transcript.lower()
    if "reschedule" in t:
        return "reschedule"
    elif "prescription" in t or "refill" in t:
        return "medication"
    elif "test result" in t or "lab result" in t:
        return "test-results"
    elif "appointment" in t:
        return "appointment"
    elif "cancel" in t:
        return "cancel"
    else:
        return "other"