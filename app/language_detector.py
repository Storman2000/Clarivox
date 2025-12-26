"""
language_detector.py
Utility to detect audio language (English, Spanish, etc.)
For use when language is not explicitly provided.
"""

import logging
from typing import Optional, Tuple
from langdetect import detect, DetectorFactory

logger = logging.getLogger(__name__)

DetectorFactory.seed = 0  # Make results deterministic

SUPPORTED_LANGUAGES = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German"
}

DEFAULT_LANGUAGE = "en"


class LanguageDetectionError(Exception):
    pass


class LanguageDetector:
    def __init__(self, default_language: str = "en"):
        self.default_language = default_language
        self.supported = SUPPORTED_LANGUAGES
        logging.debug(f"Initialized LanguageDetector with default={default_language}")

    def detect_language(self, text: str) -> Tuple[str, str]:
        """
        Detects the language of a given transcript.

        Returns:
            (language_code, language_name)
        """
        try:
            detected = detect(text)
            logging.debug(f"Raw detected language: {detected}")

            if detected in self.supported:
                return detected, self.supported[detected]
            else:
                logging.warning(f"Detected unsupported language: {detected}, falling back to default")
                return self.default_language, self.supported[self.default_language]

        except Exception as e:
            logging.error(f"Language detection failed: {e}, using default")
            return self.default_language, self.supported[self.default_language]


def detect_language(text: str) -> Optional[str]:
    """Detect language of transcript (e.g., English or Spanish)."""
    try:
        lang = detect(text)
        return 'es' if lang == 'es' else 'en'
    except Exception:
        return 'en'  # Default to English if detection fails


def detect_language_from_text(text: str) -> str:
    """Detect primary language of a transcript string."""
    try:
        lang = detect(text)
        if lang in SUPPORTED_LANGUAGES:
            logging.info(f"Detected language: {SUPPORTED_LANGUAGES[lang]} ({lang})")
            return lang
        else:
            logging.warning(f"Detected unsupported language: {lang}. Defaulting to {DEFAULT_LANGUAGE}.")
            return DEFAULT_LANGUAGE
    except Exception:
        logging.error("Language detection failed. Defaulting to English.")
        return DEFAULT_LANGUAGE


def get_language_label(lang_code: str) -> str:
    """Return full language name from ISO code."""
    return SUPPORTED_LANGUAGES.get(lang_code, 'Unknown')


# For testing / usage
if __name__ == '__main__':
    detector = LanguageDetector()
    samples = [
        "Necesito una cita para la próxima semana",
        "Je souhaite renouveler mon ordonnance.",
        "Ich brauche einen neuen Termin.",
        "I need a refill on my blood pressure medication."
    ]
    for s in samples:
        code, name = detector.detect_language(s)
        print(f"Text: {s}\nDetected: {name} ({code})\n")
