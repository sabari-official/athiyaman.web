from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError

from backend.utils.security import decode_token

# Enforce JWT bearer injection controls
bearer_security = HTTPBearer()

class RoleChecker:
    """
    Decoupled FastAPI route guard dependency checker.
    Verifies that the bearer token is valid and the authenticated persona's role
    matches allowed user role scopes.
    """
    def __init__(self, allowed_roles: list):
        self.allowed_roles = allowed_roles

    def __call__(self, credentials: HTTPAuthorizationCredentials = Depends(bearer_security)) -> dict:
        token = credentials.credentials
        try:
            payload = decode_token(token)
            
            # Verify that token type is access token, not refresh token
            if payload.get("type") != "access":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail={
                        "code": "INVALID_TOKEN_TYPE",
                        "message": "Token must be an access token session."
                    }
                )
                
            user_role = payload.get("role")
            
            # Check user role bounds
            if user_role not in self.allowed_roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail={
                        "code": "INSUFFICIENT_PERMISSIONS",
                        "message": f"Your role '{user_role}' is unauthorized to perform this operation."
                    }
                )
                
            # Intercept must_change_password flag
            must_change = payload.get("must_change_password", False)
            if must_change:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail={
                        "code": "MUST_CHANGE_PASSWORD",
                        "message": "You must change your default password before accessing this resource."
                    }
                )

            return payload
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "code": "INVALID_TOKEN",
                    "message": "Authentication signature is invalid or has expired."
                }
            )

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_security)) -> dict:
    """
    Decodes user payload without enforcing the must_change_password flag.
    Used explicitly for endpoints like /auth/change-password.
    """
    token = credentials.credentials
    try:
        payload = decode_token(token)
        if payload.get("type") != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"code": "INVALID_TOKEN_TYPE", "message": "Token must be an access token session."}
            )
        # Rename sub to id to easily use current_user.id
        return type('CurrentUser', (), {'id': payload.get('sub'), 'role': payload.get('role')})()
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "INVALID_TOKEN", "message": "Authentication signature is invalid or has expired."}
        )
