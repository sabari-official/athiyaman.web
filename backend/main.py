import logging
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from backend.core.config import settings

# Configure basic logging standard
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("backend")

app = FastAPI(
    title="Athiyaman Platform - Digital India",
    description="Decentralized Resource Collection & Level Progression Portal (Phase 1)",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS configurations loaded dynamically from environment setting class
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",  # Vite default port
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# UNIFIED ERROR HANDLERS (05_IMPLEMENTATION.md Standards)
# ==========================================

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request, exc: HTTPException):
    """
    Returns API Errors in the standard formats required by frontend interceptors:
    {
      "detail": {
        "code": "ERROR_CODE",
        "message": "Detailed description of error state."
      }
    }
    """
    # If detail is already a dict with code, pass it through directly
    if isinstance(exc.detail, dict) and "code" in exc.detail:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
        )
    
    # Otherwise format it standardly
    code = "API_ERROR"
    if exc.status_code == status.HTTP_401_UNAUTHORIZED:
        code = "UNAUTHORIZED"
    elif exc.status_code == status.HTTP_403_FORBIDDEN:
        code = "FORBIDDEN"
    elif exc.status_code == status.HTTP_404_NOT_FOUND:
        code = "RESOURCE_NOT_FOUND"
        
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": {
                "code": code,
                "message": str(exc.detail)
            }
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    """
    Formats standard pydantic parameters validation violations into standardized API errors.
    """
    errors = exc.errors()
    message = "Request validation failed."
    if errors:
        loc = " -> ".join(str(x) for x in errors[0].get("loc", []))
        msg = errors[0].get("msg", "invalid input value")
        message = f"Validation failed at '{loc}': {msg}"

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": {
                "code": "VALIDATION_ERROR",
                "message": message
            }
        }
    )

@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "Athiyaman Digital India Platform (Phase 1) Backend API",
        "version": "1.0.0"
    }

# Mount API Routers
from backend.api.v1.api import api_router
app.include_router(api_router, prefix="/api/v1")

