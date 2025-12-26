"""
pii_sanitizer.py
A utility class for detecting and sanitizing personally identifiable information (PII)
from transcribed text.

Supports redaction of:
- Phone numbers
- Email addresses
- Social Security Numbers (SSNs)
- Dates
- MRNs (if patterns are known)
"""

import re
from typing import Tuple, Dict


class PIISanitizer:
    """
    A utility class for detecting and sanitizing personally identifiable information (PII)
    from transcribed text.
    """

    def __init__(self):
        self.patterns: Dict[str, str] = {
            "PHONE": r"\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b",
            "EMAIL": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
            "SSN": r"\b\d{3}[- ]?\d{2}[- ]?\d{4}\b",
            "DATE": r"\b(?:\d{1,2}[-/]){2}\d{2,4}\b",
            # Add more patterns if needed (e.g., MRN)
        }

    def sanitize(self, text: str) -> Tuple[str, Dict[str, int]]:
        """
        Sanitize PII from a string.

        Args:
            text (str): The input transcript.

        Returns:
            Tuple[str, Dict[str, int]]: Redacted transcript and PII type counts.
        """
        pii_counts: Dict[str, int] = {}
        
        # Handle None or empty input
        if text is None:
            return "", pii_counts
        if not text:
            return text, pii_counts
            
        sanitized_text = text

        for label, pattern in self.patterns.items():
            matches = re.findall(pattern, sanitized_text)
            pii_counts[label] = len(matches)
            sanitized_text = re.sub(pattern, f"[{label}]", sanitized_text)

        return sanitized_text, pii_counts


# Singleton instance
_sanitizer = PIISanitizer()


def sanitize_transcript(text: str) -> str:
    """
    Sanitize PII from a transcript string.
    
    Args:
        text (str): The input transcript.
        
    Returns:
        str: Sanitized transcript with PII redacted.
    """
    sanitized_text, _ = _sanitizer.sanitize(text)
    return sanitized_text


def sanitize_with_stats(text: str) -> Tuple[str, Dict[str, int]]:
    """
    Sanitize PII from a transcript and return statistics.
    
    Args:
        text (str): The input transcript.
        
    Returns:
        Tuple[str, Dict[str, int]]: Sanitized transcript and PII counts.
    """
    return _sanitizer.sanitize(text)


# Example usage
if __name__ == "__main__":
    sanitizer = PIISanitizer()
    sample = "Patient email is john.doe@example.com and SSN is 123-45-6789. Call at (555) 123-4567."
    redacted, stats = sanitizer.sanitize(sample)
    print("Redacted:", redacted)
    print("Stats:", stats)
