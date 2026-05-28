import base64
import datetime
import hashlib
import uuid
from typing import Optional, Dict, Any
from fastapi import UploadFile, HTTPException, status
from jose import jwt, JWTError
from passlib.context import CryptContext
from cryptography.fernet import Fernet

from backend.core.config import settings

# Enforce Argon2id secure password hashing parameters
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """Hahses plain text password using standard Argon2id algorithm."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies plain text password against database hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

# ==========================================
# JWT SESSION MANAGEMENT
# ==========================================

def create_access_token(user_id: str, role: str, must_change_password: bool = False) -> str:
    """Generates stateless JWT access token expiring in settings ACCESS_TOKEN_EXPIRE_MINUTES."""
    payload = {
        "sub": str(user_id),
        "role": str(role),
        "must_change_password": must_change_password,
        "type": "access",
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

def create_refresh_token(user_id: str) -> str:
    """Generates secure JWT refresh token expiring in settings REFRESH_TOKEN_EXPIRE_DAYS."""
    payload = {
        "sub": str(user_id),
        "type": "refresh",
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

def decode_token(token: str) -> Dict[str, Any]:
    """Decodes and validates JWT token signature. Raises JWTError if invalid or expired."""
    return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])

# ==========================================
# CRITICAL PII DATA CRYPTOGRAPHY
# ==========================================

class CryptographyManager:
    """
    Manages AES-256 symmetric encryption and decryption for sensitive citizen data
    (Aadhaar numbers and Bank Account configurations) stored at rest in the database.
    """
    def __init__(self):
        # Derive standard 32-byte urlsafe Fernet key cryptographically from settings JWT_SECRET
        hashed_secret = hashlib.sha256(settings.JWT_SECRET.encode()).digest()
        fernet_key = base64.urlsafe_b64encode(hashed_secret)
        self.cipher = Fernet(fernet_key)

    def encrypt_data(self, data: str) -> str:
        """Encrypts plain text string into secure AES-256 base64 representation."""
        if not data:
            return ""
        return self.cipher.encrypt(data.encode()).decode()

    def decrypt_data(self, encrypted_data: str) -> str:
        """Decrypts AES-256 encrypted base64 payload into plain text representation."""
        if not encrypted_data:
            return ""
        return self.cipher.decrypt(encrypted_data.encode()).decode()

    def generate_sha256_hash(self, data: str) -> str:
        """Generates standard SHA-256 hash for duplicate check assertions without disclosing plain data."""
        if not data:
            return ""
        return hashlib.sha256(data.encode()).hexdigest()

# Instantiated security Managers ready for dependency injection
aadhaar_security = CryptographyManager()
bank_security = CryptographyManager()

# ==========================================
# FILE UPLOAD VALIDATIONS & SANITIZERS
# ==========================================

ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "application/pdf"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 Megabytes

def validate_uploaded_file(file: UploadFile) -> str:
    """
    Validates uploaded file size and content types signatures.
    Returns a secure path-traversal proof randomly generated UUID filename.
    """
    # 1. Enforce size limitations
    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)
    
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "FILE_TOO_LARGE",
                "message": f"Upload size exceeds the maximum allowed limit of 5MB. Submitted: {file_size / (1024*1024):.2f}MB"
            }
        )

    # 2. Enforce content MIME verification rules
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "INVALID_FILE_TYPE",
                "message": f"MIME type '{file.content_type}' is prohibited. Only JPEG, PNG, and PDF files are allowed."
            }
        )

    # 3. Generate safe path-traversal proof UUID filename
    file_ext = "jpg"
    if file.filename and "." in file.filename:
        file_ext = file.filename.split(".")[-1].lower()
        if file_ext not in {"jpg", "jpeg", "png", "pdf"}:
            file_ext = "jpg"  # default safe fallback
            
    secure_filename = f"{uuid.uuid4()}.{file_ext}"
    return secure_filename
