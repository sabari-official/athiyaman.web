from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.modules.auth.schema import (
    UserSignupRequest, UserLoginRequest, TokenResponse, UserResponse,
    ChangePasswordRequest, VerifyAadhaarRequest, VerifyAadhaarResponse
)
from backend.modules.auth.service import AuthService
from backend.middleware.rbac import get_current_user
from backend.utils.verhoeff import validate_aadhaar

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup(payload: UserSignupRequest, db: Session = Depends(get_db)):
    """
    Onboard a new Citizen or Team Leader.
    Signups are closed-loop, requiring a valid inviter referral code.
    """
    service = AuthService(db)
    try:
        user = service.signup(
            username=payload.username,
            phone_number=payload.phone_number,
            plain_password=payload.password,
            referral_code_str=payload.referral_code
        )
        return user
    except ValueError as e:
        error_msg = str(e)
        
        # Map specific business errors to appropriate HTTP status codes
        if error_msg in {"USERNAME_TAKEN", "PHONE_REGISTERED"}:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "code": error_msg,
                    "message": "The username or phone number is already registered."
                }
            )
        elif error_msg in {"INVALID_REFERRAL_CODE", "REFERRAL_CODE_EXPIRED"}:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "code": error_msg,
                    "message": "The referral code is either invalid, expired, or fully utilized."
                }
            )
        elif error_msg == "TEAM_INACTIVE":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "code": "TEAM_INACTIVE",
                    "message": "The inviter's team is currently suspended or inactive."
                }
            )
            
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "SIGNUP_FAILED",
                "message": error_msg
            }
        )

@router.post("/login", response_model=TokenResponse)
def login(payload: UserLoginRequest, db: Session = Depends(get_db)):
    """
    Authenticate user credentials and issue stateless JWT session tokens.
    """
    service = AuthService(db)
    try:
        token_data = service.login(
            username_or_phone=payload.username,
            plain_password=payload.password
        )
        return token_data
    except ValueError as e:
        error_msg = str(e)
        
        if "ACCOUNT_LOCKED" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "code": "ACCOUNT_LOCKED",
                    "message": f"Too many failed attempts. Account locked. {error_msg.replace('ACCOUNT_LOCKED_', '').replace('_MINUTES', ' minutes remaining.')}"
                }
            )
            
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "code": "INVALID_CREDENTIALS",
                "message": "Incorrect username, phone number, or password."
            }
        )

@router.post("/change-password", status_code=status.HTTP_200_OK)
def change_password(payload: ChangePasswordRequest, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Allows a user to change their password. If forced (must_change_password), this clears the flag.
    """
    service = AuthService(db)
    try:
        service.change_password(
            user_id=str(current_user.id),
            current_password=payload.current_password,
            new_password=payload.new_password,
            new_username=payload.new_username
        )
        return {"status": "success", "message": "Password changed successfully"}
    except ValueError as e:
        error_msg = str(e)
        if error_msg == "USERNAME_TAKEN":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"code": "USERNAME_TAKEN", "message": "This username is already taken by another account."}
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "PASSWORD_CHANGE_FAILED", "message": error_msg}
        )

@router.post("/verify-aadhaar", response_model=VerifyAadhaarResponse, status_code=status.HTTP_200_OK)
def verify_aadhaar(payload: VerifyAadhaarRequest):
    """
    Validates Aadhaar format using local Verhoeff checksum.
    """
    is_valid = validate_aadhaar(payload.aadhaar)
    return VerifyAadhaarResponse(valid=is_valid)

@router.get("/check-username", status_code=status.HTTP_200_OK)
def check_username(username: str, db: Session = Depends(get_db)):
    """
    Checks if a username is already taken.
    """
    service = AuthService(db)
    exists = service.user_repo.get_by_username(username) is not None
    return {"available": not exists}
