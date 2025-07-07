# utils/intent.py

def detect_intent(transcript: str) -> str:
    transcript = transcript.lower()

    if "cancel" in transcript or "reschedule" in transcript:
        return "appointment-change"
    if "refill" in transcript or "prescription" in transcript:
        return "medication-refill"
    if "pain" in transcript or "suicide" in transcript or "kill myself" in transcript:
        return "urgent-behavioral-health"
    
    return "general"