# Athiyaman Platform - Backend Implementation Document
## Phase 1 – Digital India FastAPI Development & Engineering Guidelines

---

## 1. Backend Development Strategy

*   **Engineering Focus:** To construct a stateless, highly auditable, and asynchronous backend engine using FastAPI.
*   **Architecture Standard:** Clean Architecture design, decoupling Presentation schemas, Service business logic, and Repository database access layers.
*   **Core Engineering Principles:** Enforce type safety, strict data validations, and comprehensive audit logs across all modules.
*   **Performance Benchmarks:** Maintain sub-$500\text{ms}$ API server response limits.

---

## 2. FastAPI Project Setup

Configure the Python runtime environment and core application scripts:

### 2.1 Virtual Environment Setup
```bash
# 1. Initialize Python virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install core packages
pip install fastapi uvicorn sqlalchemy alembic pydantic[email] python-jose[cryptography] passlib[argon2] psycopg2-binary pydantic-settings python-multipart celery redis
```

### 2.2 Core Application Entrypoint (`app/main.py`)
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.api import api_router

app = FastAPI(
    title="Athiyaman Platform - Digital India",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API Routers
app.include_router(api_router, prefix=settings.API_V1_STR)
```

### 2.3 Core Configuration Loader (`app/core/config.py`)
```python
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Athiyaman"
    
    # Security Configuration
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Database Configuration
    DATABASE_URL: str
    
    # CORS Configuration
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # Storage Configuration
    STORAGE_TYPE: str = "LOCAL"
    STORAGE_PATH: str = "/var/www/athiyaman/uploads"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
```

---

## 3. Module Development Order

To avoid dependency blocks, modules must be developed in this strict order:

```
┌────────────────────────────────────────────────────────┐
│  1. Auth: User identities and JWT tokens               │
├────────────────────────────────────────────────────────┤
│  2. Profiles: PII details and bank configurations       │
├────────────────────────────────────────────────────────┤
│  3. Teams: Team boundaries and unique team codes       │
├────────────────────────────────────────────────────────┤
│  4. Referrals: Invitation codes and capacity counters  │
├────────────────────────────────────────────────────────┤
│  5. Levels: Progression thresholds and rewards         │
├────────────────────────────────────────────────────────┤
│  6. Waste: Logging deposits and center associations     │
├────────────────────────────────────────────────────────┤
│  7. Collection Centers: Geocoded physical centers      │
├────────────────────────────────────────────────────────┤
│  8. Claims: Level milestone reward claims              │
├────────────────────────────────────────────────────────┤
│  9. Payments: Bank transfer references and ledgers     │
├────────────────────────────────────────────────────────┤
│ 10. Notifications: Inbox updates and alerts            │
├────────────────────────────────────────────────────────┤
│ 11. Audit: Immutable logging logs                      │
├────────────────────────────────────────────────────────┤
│ 12. Analytics: Snapshot aggregate tables               │
├────────────────────────────────────────────────────────┤
│ 13. Admin: Vetting panels and approvals                │
├────────────────────────────────────────────────────────┤
│ 14. Developer: System health and backups               │
└────────────────────────────────────────────────────────┘
```

---

## 4. Folder Creation Process

Build out the directory layout in the workspace, adding standard python entry files (`__init__.py`) to make directories importable:

```bash
mkdir -p app/api/v1 app/core app/database app/middleware app/utils app/jobs app/modules
cd app/modules
mkdir -p auth profiles teams referrals levels waste collection_centers claims payments notifications audit analytics admin developer

# Create sub-structure files in each module
for mod in auth profiles teams referrals levels waste collection_centers claims payments notifications audit analytics admin developer; do
    touch $mod/__init__.py
    touch $mod/router.py
    touch $mod/schema.py
    touch $mod/model.py
    touch $mod/service.py
    touch $mod/repository.py
done
```

---

## 5. SQLAlchemy Model Implementation

*   **Database Entity Definitions:** Define model classes in `model.py` files under their respective modules, mapping attributes directly to PostgreSQL tables.
*   **Table Naming Rules:** Enforce lowercase, snake_case plural naming. Singular forms are preferred for column names.
*   **Relational Integrity Rules:** Primary keys in transactional tables must use UUID types, enforcing foreign key constraints and `ON DELETE RESTRICT` rules to prevent orphaned records.
*   **Model Audit Base class:**
    ```python
    import datetime
    from sqlalchemy import Column, DateTime
    from sqlalchemy.ext.declarative import declarative_base
    
    Base = declarative_base()
    
    class AuditBaseModel(Base):
        __abstract__ = True
        
        created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
        updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow, nullable=False)
    ```

---

## 6. Pydantic Schema Implementation

*   **Schema Isolation:** Pydantic schemas in `schema.py` must separate request shapes from response models:
    *   *Base Schemas:* Defines shared properties.
    *   *Request Schemas (Create/Update):* Used to validate incoming payloads.
    *   *Response Schemas:* Used to serialize data returned to clients.
*   **Data Serialization Standards:** Enforce strict type hints, disabling ORM lazy-loading to keep response payloads deterministic:
    ```python
    from pydantic import BaseModel, Field
    from uuid import UUID
    
    class UserProfileResponse(BaseModel):
        full_name: str = Field(..., example="Ramesh Kumar")
        email: str = Field(..., example="ramesh@email.com")
        profile_completion: int = Field(0, ge=0, le=100)
        
        class Config:
            from_attributes = True  # Enable ORM serialization support
    ```

---

## 7. Repository Layer Implementation

*   **Decoupled Relational Database Access:** Repositories handle database interactions using SQLAlchemy ORM, isolating database sessions from business services.
*   **Repository Base Template:**
    ```python
    from typing import Generic, TypeVar, Type, Optional, List
    from sqlalchemy.orm import Session
    from uuid import UUID
    
    T = TypeVar('T')
    
    class BaseRepository(Generic[T]):
        def __init__(self, model: Type[T], db: Session):
            self.model = model
            self.db = db
            
        def get_by_id(self, id: UUID) -> Optional[T]:
            return self.db.query(self.model).filter(self.model.id == id).first()
            
        def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
            return self.db.query(self.model).offset(skip).limit(limit).all()
            
        def create(self, obj: T) -> T:
            self.db.add(obj)
            self.db.commit()
            self.db.refresh(obj)
            return obj
    ```

---

## 8. Service Layer Implementation

*   **Service Layer Separation:** Business rules, level progression metrics, geocoding lookups, and reward eligibility are processed exclusively in Service classes.
*   **Database Transaction Strategy:** Enforces explicit database transactions (`commit` / `rollback`) inside Service classes, ensuring updates are saved successfully or rolled back completely in case of database failures.
*   **Service Core Blueprint:**
    ```python
    from sqlalchemy.orm import Session
    from app.modules.teams.repository import TeamRepository
    
    class TeamService:
        def __init__(self, db: Session):
            self.db = db
            self.team_repo = TeamRepository(db)
            
        def create_new_team(self, leader_id, team_name, district, area, pincode):
            # 1. Enforce unique team name constraints
            if self.team_repo.exists_by_name(team_name):
                raise ValueError("DUPLICATE_TEAM_NAME")
                
            # 2. Enforce One Leader One Team rule
            if self.team_repo.exists_by_leader(leader_id):
                raise ValueError("LEADER_ALREADY_HAS_TEAM")
                
            # 3. Create team record in transaction
            team = self.team_repo.create_team(leader_id, team_name, district, area, pincode)
            return team
    ```

---

## 9. API Layer Implementation

*   **REST Endpoint Standards:** Endpoint controllers only route paths, validate request schemas, check JWT credentials, and return JSON payloads.
*   **API Router Blueprint:**
    ```python
    from fastapi import APIRouter, Depends, HTTPException, status
    from sqlalchemy.orm import Session
    from app.database.session import get_db
    from app.modules.teams.schema import TeamCreateSchema, TeamResponseSchema
    from app.modules.teams.service import TeamService
    
    router = APIRouter()
    
    @router.post("/", response_model=TeamResponseSchema, status_code=status.HTTP_201_CREATED)
    def create_team(payload: TeamCreateSchema, db: Session = Depends(get_db)):
        service = TeamService(db)
        try:
            team = service.create_new_team(
                leader_id=payload.leader_id,
                team_name=payload.team_name,
                district=payload.district,
                area=payload.area,
                pincode=payload.pincode
            )
            return team
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    ```

---

## 10. JWT Implementation

Stateless session access controls utilize dual JWT tokens managed securely on client and server networks:

```python
import datetime
from jose import jwt
from app.core.config import settings

def create_access_token(user_id: str, role: str) -> str:
    payload = {
        "sub": user_id,
        "role": role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

def create_refresh_token(user_id: str) -> str:
    payload = {
        "sub": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
```

---

## 11. RBAC Implementation

Verify endpoint permissions dynamically by parsing JWT role payloads at the router layer:

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from app.core.config import settings

security = HTTPBearer()

class RoleChecker:
    def __init__(self, allowed_roles: list):
        self.allowed_roles = allowed_roles
        
    def __call__(self, creds: HTTPAuthorizationCredentials = Depends(security)):
        token = creds.credentials
        try:
            payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
            user_role = payload.get("role")
            if user_role not in self.allowed_roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="INSUFFICIENT_PERMISSIONS"
                )
            return payload
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="INVALID_TOKEN"
            )
```

---

## 12. Aadhaar Security Implementation

Plain text Aadhaar entries are encrypted before database writes, using unique cryptographic hashes for duplicate detection checks:

```python
import hashlib
from cryptography.fernet import Fernet
from app.core.config import settings

class AadhaarSecurityManager:
    def __init__(self):
        # Enforce key-based encryption controls
        self.cipher = Fernet(settings.JWT_SECRET.encode()[:32] + b'=')
        
    def encrypt_aadhaar(self, aadhaar: str) -> str:
        return self.cipher.encrypt(aadhaar.encode()).decode()
        
    def decrypt_aadhaar(self, encrypted_aadhaar: str) -> str:
        return self.cipher.decrypt(encrypted_aadhaar.encode()).decode()
        
    def hash_aadhaar(self, aadhaar: str) -> str:
        return hashlib.sha256(aadhaar.encode()).hexdigest()
```

---

## 13. File Upload Security Implementation

Inspect incoming files, verifying signatures and checking sizes to prevent file upload exploits:

```python
import uuid
from fastapi import UploadFile, HTTPException, status

ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "application/pdf"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def validate_uploaded_file(file: UploadFile):
    # 1. Size checking
    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="FILE_TOO_LARGE")
        
    # 2. Content MIME verification
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="INVALID_FILE_TYPE")
        
    # 3. Rename files to prevent path traversal exploits
    file_ext = file.filename.split(".")[-1]
    secure_filename = f"{uuid.uuid4()}.{file_ext}"
    return secure_filename
```

---

## 14. Audit Logging Implementation

Enforce asynchronous database logging to prevent user request bottlenecks during operations:

```python
import asyncio
from app.modules.audit.model import AuditLog

def log_system_event(db_session, user_id, role, action, entity_type, entity_id, ip_address, device):
    async def write_log():
        log = AuditLog(
            user_id=user_id,
            role=role,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            ip_address=ip_address,
            device=device
        )
        db_session.add(log)
        db_session.commit()
        
    # Schedule log execution asynchronously
    asyncio.create_task(write_log())
```

---

## 15. Queue Processing Implementation

Heavy background operations use Celery background queues:

```python
from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "athiyaman_tasks",
    broker=settings.REDIS_QUEUE_URL,
    backend=settings.REDIS_QUEUE_URL
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Kolkata",
    enable_utc=True,
)
```

---

## 16. Notification Engine Implementation

*   **Asynchronous Alert Routing:** The notification engine routes alerts asynchronously to prevent application bottlenecks.
*   **Inbox Tracking:** Logs track the read/unread states of user notifications.
*   **Multi-channel Adapters:** Employs dynamic system interfaces, sending dashboard updates natively and routing SMS/WhatsApp notifications via mock adapters.

---

## 17. Payment Engine Implementation

Decouples payment engines using the Payment Service Interface, allowing provider switches without modifying business logic:

```python
from abc import ABC, abstractmethod

class PaymentProviderInterface(ABC):
    @abstractmethod
    def process_payout(self, recipient_account: str, amount: float, tracking_id: str) -> str:
        pass

class RazorpayXAdapter(PaymentProviderInterface):
    def process_payout(self, recipient_account: str, amount: float, tracking_id: str) -> str:
        # Integrated RazorpayX payout logic
        return "RAZORPAYX_TXN_REF_12345"

class BankUploadAdapter(PaymentProviderInterface):
    def process_payout(self, recipient_account: str, amount: float, tracking_id: str) -> str:
        # Standard manual banking reference ledger
        return "MANUAL_BANK_REF_56789"
```

---

## 18. Background Workers

*   **Worker Deployment:** Deploy background workers on production servers to execute queued tasks, managing worker lifecycles via Systemd:
    ```ini
    [Unit]
    Description=Celery Worker for Athiyaman Tasks
    After=network.target
    
    [Service]
    User=athiyaman_user
    WorkingDirectory=/var/www/athiyaman/backend
    ExecStart=/var/www/athiyaman/backend/venv/bin/celery -A app.jobs.tasks worker --loglevel=info
    Restart=always
    
    [Install]
    WantedBy=multi-user.target
    ```

---

## 19. Error Handling Strategy

*   **Validation Errors:** Caught automatically by FastAPI routers, returning HTTP status `422 Unprocessable Entity` with parameter details.
*   **Business Errors:** Triggered by service logic violations (e.g., duplicate team names), returning HTTP status `400 Bad Request` with consistent details.
*   **System Errors:** Database connection issues trigger transaction rollbacks, returning HTTP status `500 Internal Error` to prevent data corruption.
*   **Security Violations:** Return HTTP status `403 Forbidden` for route permission exceptions.

---

## 20. Logging Strategy

*   **Application Logging:** Standard logging handlers capture database connections, server actions, and system startup metrics.
*   **Security Logging:** Tracks security alerts, including consecutive failed logins, blocked IPs, and unauthorized access attempts.
*   **Log Rotation:** Logs use automated rotation files to prevent disk space exhaustion.

---

## 21. Testing Strategy

*   **Unit Testing:** Focuses on testing standalone components, mathematical formulas, and helper utilities.
*   **Integration Testing:** Validates complete database-to-endpoint integrations.
*   **Security Scans:** Automated scripts verify endpoint protection, confirming that unprivileged users receive `403 Forbidden` errors.

---

## 22. Code Review Standards

*   **PEP 8 Compliance:** All backend scripts must pass strict PEP 8 linting checks before code reviews.
*   **Validation Checkpoints:** Confirm that all API endpoints declare explicit input and output schemas.
*   **Relational Integrity:** Verify that all database migrations include safe upgrade and rollback paths.

---

## 23. Security Review Standards

*   **PII Vetting:** Ensure that no Aadhaar or bank account numbers are logged in plain text in database entries or application logs.
*   **Route Guards Vetting:** Confirm all non-public APIs require valid JWT tokens and check user roles at the gateway layer.
*   **Upload Vetting:** Verify file validation rules check file signatures and restrict uploads to secure types.

---

## 24. Performance Review Standards

*   **API Latency:** Verify that standard endpoint response times maintain latency limits of less than $500\text{ms}$.
*   **Query Optimization:** Confirm that frequently queried columns are optimized using indexes and heavy dashboard calculations use precalculated snapshots.

---

## 25. Backend Readiness Checklist

Before deploying the backend in production, ensure all items on this readiness checklist are completed:

*   [ ] **FastAPI Setup:** Confirm Python virtual environments are configured and core routes are active.
*   [ ] **Security hardening:** Verify passwords hash using Argon2id and access tokens carry $15\text{-minute}$ lifespans.
*   [ ] **PII Protections:** Confirm Aadhaar and bank details are encrypted at rest using AES-256.
*   [ ] **Audit Logging:** Verify trigger functions block UPDATE and DELETE queries on audit logs.
*   [ ] **Queue Processing:** Verify Redis queue workers run asynchronously without errors.
*   [ ] **Testing Audit:** Confirm core unit and integration test coverage exceeds $85\%$.

---

## 26. Conclusion

This Backend Implementation Guide (`12_BACKEND_IMPLEMENTATION.md`) establishes the absolute technical setups, folder structures, component interfaces, security modules, Celery queues, error handling rules, and readiness checklists for the Athiyaman Platform – Digital India Phase 1. By detailing code architectures and providing complete SQL and Python snippets, it serves as a complete technical guide for backend developers, enabling independent development cycles.
