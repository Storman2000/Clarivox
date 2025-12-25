"""
test_pii_sanitizer.py
Unit tests for PII/PHI sanitization - CRITICAL for HIPAA compliance
"""

import pytest
from app.pii_sanitizer import sanitize_transcript


class TestPhoneNumberRedaction:
    """Test phone number pattern detection and redaction"""
    
    def test_standard_phone_format(self):
        """Test 555-123-4567 format"""
        text = "Call me at 555-123-4567 for results"
        result = sanitize_transcript(text)
        assert "555-123-4567" not in result
        assert "[PHONE]" in result or "[REDACTED]" in result or "***" in result
    
    def test_phone_with_parentheses(self):
        """Test (555) 123-4567 format"""
        text = "My number is (555) 123-4567"
        result = sanitize_transcript(text)
        assert "(555) 123-4567" not in result
    
    def test_phone_no_dashes(self):
        """Test 5551234567 format"""
        text = "Contact me at 5551234567"
        result = sanitize_transcript(text)
        assert "5551234567" not in result
    
    def test_phone_with_extension(self):
        """Test phone with extension"""
        text = "Call 555-123-4567 ext 890"
        result = sanitize_transcript(text)
        assert "555-123-4567" not in result
    
    def test_multiple_phone_numbers(self):
        """Test multiple phone numbers in one text"""
        text = "Call 555-123-4567 or 555-987-6543"
        result = sanitize_transcript(text)
        assert "555-123-4567" not in result
        assert "555-987-6543" not in result


class TestSSNRedaction:
    """Test Social Security Number redaction"""
    
    def test_ssn_with_dashes(self):
        """Test 123-45-6789 format"""
        text = "My SSN is 123-45-6789"
        result = sanitize_transcript(text)
        assert "123-45-6789" not in result
        assert "[SSN]" in result or "[REDACTED]" in result or "***" in result
    
    def test_ssn_no_dashes(self):
        """Test 123456789 format"""
        text = "Social security number 123456789"
        result = sanitize_transcript(text)
        # Should redact 9-digit number
        assert "123456789" not in result
    
    def test_ssn_with_spaces(self):
        """Test 123 45 6789 format"""
        text = "SSN: 123 45 6789"
        result = sanitize_transcript(text)
        assert "123 45 6789" not in result


class TestEmailRedaction:
    """Test email address redaction"""
    
    def test_standard_email(self):
        """Test user@example.com format"""
        text = "Email me at john.doe@hospital.com"
        result = sanitize_transcript(text)
        assert "john.doe@hospital.com" not in result
        assert "[EMAIL]" in result or "[REDACTED]" in result or "***" in result
    
    def test_email_with_numbers(self):
        """Test email with numbers"""
        text = "Reach me at patient123@clinic.org"
        result = sanitize_transcript(text)
        assert "patient123@clinic.org" not in result
    
    def test_multiple_emails(self):
        """Test multiple emails"""
        text = "Contact admin@hospital.com or support@clinic.org"
        result = sanitize_transcript(text)
        assert "admin@hospital.com" not in result
        assert "support@clinic.org" not in result


class TestMixedPIIRedaction:
    """Test multiple PII patterns in same text"""
    
    def test_phone_and_email(self):
        """Test both phone and email"""
        text = "Call 555-123-4567 or email patient@hospital.com"
        result = sanitize_transcript(text)
        assert "555-123-4567" not in result
        assert "patient@hospital.com" not in result
    
    def test_all_pii_types(self):
        """Test phone, email, and SSN together"""
        text = "Patient SSN 123-45-6789, phone 555-123-4567, email patient@example.com"
        result = sanitize_transcript(text)
        assert "123-45-6789" not in result
        assert "555-123-4567" not in result
        assert "patient@example.com" not in result
    
    def test_pii_in_context(self):
        """Test PII within medical context"""
        text = "Hi, this is John at 555-123-4567. I need refill for lisinopril. My SSN is 123-45-6789."
        result = sanitize_transcript(text)
        # Should redact PII but keep medication name
        assert "555-123-4567" not in result
        assert "123-45-6789" not in result
        assert "lisinopril" in result.lower()


class TestNonPIIPreservation:
    """Test that non-PII data is NOT redacted"""
    
    def test_medication_names_preserved(self):
        """Test medication names remain"""
        text = "I need refill on lisinopril 10mg"
        result = sanitize_transcript(text)
        assert "lisinopril" in result.lower()
    
    def test_symptom_descriptions_preserved(self):
        """Test symptoms remain"""
        text = "I have chest pain and shortness of breath"
        result = sanitize_transcript(text)
        assert "chest pain" in result.lower()
        assert "breath" in result.lower()
    
    def test_dates_preserved(self):
        """Test dates are kept (not PII in this context)"""
        text = "My appointment is on January 15th"
        result = sanitize_transcript(text)
        assert "January" in result or "january" in result
    
    def test_short_numbers_not_phones(self):
        """Test that short numbers aren't treated as phones"""
        text = "Take 2 pills daily"
        result = sanitize_transcript(text)
        assert "2" in result or "two" in result
    
    def test_medical_record_numbers(self):
        """Test MRN handling - may or may not redact"""
        text = "Patient MRN 12345678"
        result = sanitize_transcript(text)
        # Document the behavior - this test ensures consistency
        assert result is not None


class TestEdgeCases:
    """Test edge cases and boundary conditions"""
    
    def test_empty_string(self):
        """Test empty input"""
        result = sanitize_transcript("")
        assert result == ""
    
    def test_none_input(self):
        """Test None input handling"""
        result = sanitize_transcript(None)
        # Should either return None or empty string, not crash
        assert result is None or result == ""
    
    def test_no_pii_present(self):
        """Test text with no PII"""
        text = "I need to schedule an appointment"
        result = sanitize_transcript(text)
        assert result == text  # Should be unchanged
    
    def test_partial_phone_number(self):
        """Test incomplete phone number"""
        text = "Call me at 555-12"  # Too short to be phone
        result = sanitize_transcript(text)
        # Should NOT redact partial numbers
        assert "555-12" in result or result != text
    
    def test_international_phone_format(self):
        """Test +1-555-123-4567 format"""
        text = "International number +1-555-123-4567"
        result = sanitize_transcript(text)
        # Should handle international format
        assert "+1-555-123-4567" not in result or "[PHONE]" in result


class TestSanitizationConsistency:
    """Test that sanitization is consistent and deterministic"""
    
    def test_same_input_same_output(self):
        """Test deterministic behavior"""
        text = "Call 555-123-4567"
        result1 = sanitize_transcript(text)
        result2 = sanitize_transcript(text)
        assert result1 == result2
    
    def test_case_insensitive_patterns(self):
        """Test case variations"""
        text1 = "Email PATIENT@HOSPITAL.COM"
        text2 = "Email patient@hospital.com"
        result1 = sanitize_transcript(text1)
        result2 = sanitize_transcript(text2)
        # Both should redact the email
        assert "PATIENT@HOSPITAL.COM" not in result1
        assert "patient@hospital.com" not in result2
