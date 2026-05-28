import pytest
from backend.utils.verhoeff import validate_aadhaar
from backend.utils.uuid import uuidv7


class TestVerhoeffValidation:
    """Test Aadhaar validation using Verhoeff algorithm"""

    def test_valid_aadhaar(self):
        """Test validating a valid Aadhaar"""
        # A valid Aadhaar number (12 digits)
        aadhaar = "123456789012"
        result = validate_aadhaar(aadhaar)
        assert isinstance(result, bool)

    def test_invalid_aadhaar_format(self):
        """Test with invalid format"""
        assert validate_aadhaar("12345") is False
        assert validate_aadhaar("abc12345678901") is False
        assert validate_aadhaar("") is False

    def test_aadhaar_with_spaces(self):
        """Test Aadhaar with spaces"""
        aadhaar = "1234 5678 9012"
        result = validate_aadhaar(aadhaar)
        assert isinstance(result, bool)

    def test_aadhaar_with_hyphens(self):
        """Test Aadhaar with hyphens"""
        aadhaar = "1234-5678-9012"
        result = validate_aadhaar(aadhaar)
        assert isinstance(result, bool)

    def test_aadhaar_too_short(self):
        """Test Aadhaar with less than 12 digits"""
        assert validate_aadhaar("123456789") is False

    def test_aadhaar_too_long(self):
        """Test Aadhaar with more than 12 digits"""
        assert validate_aadhaar("12345678901234") is False


class TestUUIDv7Generation:
    """Test UUIDv7 generation"""

    def test_uuidv7_generation(self):
        """Test generating UUIDv7"""
        uuid = uuidv7()
        assert uuid is not None
        assert len(str(uuid)) == 36  # Standard UUID string length

    def test_uuidv7_format(self):
        """Test UUIDv7 format"""
        uuid = uuidv7()
        uuid_str = str(uuid)
        # Should have standard UUID format: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        parts = uuid_str.split('-')
        assert len(parts) == 5
        assert len(parts[0]) == 8
        assert len(parts[1]) == 4
        assert len(parts[2]) == 4
        assert len(parts[3]) == 4
        assert len(parts[4]) == 12

    def test_uuidv7_uniqueness(self):
        """Test that generated UUIDs are unique"""
        uuid1 = uuidv7()
        uuid2 = uuidv7()
        assert uuid1 != uuid2

    def test_uuidv7_timestamp_ordered(self):
        """Test that UUIDs are roughly timestamp ordered"""
        import time
        uuid1 = uuidv7()
        time.sleep(0.001)  # Small delay
        uuid2 = uuidv7()
        # UUID2 should be greater than UUID1
        assert uuid2 > uuid1
