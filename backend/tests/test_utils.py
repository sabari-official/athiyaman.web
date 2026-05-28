"""Test utilities and helpers"""
import jwt
from datetime import datetime, timedelta
from backend.core.config import settings

def create_test_jwt_token(user_id: str, role: str = "MEMBER", must_change_password: bool = False) -> str:
    """Create a test JWT token"""
    payload = {
        "sub": user_id,
        "role": role,
        "must_change_password": must_change_password,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return token

def create_expired_jwt_token(user_id: str) -> str:
    """Create an expired JWT token"""
    payload = {
        "sub": user_id,
        "role": "MEMBER",
        "exp": datetime.utcnow() - timedelta(hours=1)
    }
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return token

class MockWasteRecord:
    """Mock waste record for testing"""
    def __init__(self, user_id, center_id, weight_kg=10.0):
        self.id = "test-waste-id"
        self.user_id = user_id
        self.center_id = center_id
        self.weight_kg = weight_kg
        self.verification_status = "PENDING"
        self.payment_status = "PENDING"
        self.created_at = datetime.utcnow()

class MockUser:
    """Mock user for testing"""
    def __init__(self, username, phone_number, role="MEMBER"):
        self.id = "test-user-id"
        self.username = username
        self.phone_number = phone_number
        self.role = role
        self.is_verified = True
        self.created_at = datetime.utcnow()

class MockTeam:
    """Mock team for testing"""
    def __init__(self, leader_id, name="Test Team"):
        self.id = "test-team-id"
        self.leader_id = leader_id
        self.name = name
        self.status = "ACTIVE"
        self.member_count = 1
        self.created_at = datetime.utcnow()
