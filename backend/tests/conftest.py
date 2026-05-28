import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.main import app
from backend.core.database import Base, get_db
from backend.core.config import settings

# Test database URL (use SQLite for testing)
TEST_DATABASE_URL = "sqlite:///./test.db"

@pytest.fixture(scope="session")
def engine():
    """Create test database engine"""
    engine = create_engine(
        TEST_DATABASE_URL, connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(bind=engine)
    
    # Seed default settings, levels, and admin accounts for testing
    from sqlalchemy.orm import sessionmaker
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    try:
        from backend.database.models import Level, SystemSetting, CollectionCenter, ReferralCode, User, UserProfile
        import datetime
        import uuid
        
        # 1. Seed levels
        if not db.query(Level).first():
            levels = [
                Level(level_number=1, reward_amount=100.00, requirement_type="MEMBER_COUNT", requirement_value=10),
                Level(level_number=2, reward_amount=1000.00, requirement_type="MEMBER_COUNT", requirement_value=90),
                Level(level_number=3, reward_amount=2000.00, requirement_type="MEMBER_COUNT", requirement_value=720),
                Level(level_number=4, reward_amount=3000.00, requirement_type="MEMBER_COUNT", requirement_value=5040),
                Level(level_number=5, reward_amount=4000.00, requirement_type="MEMBER_COUNT", requirement_value=30240),
                Level(level_number=6, reward_amount=5000.00, requirement_type="MEMBER_COUNT", requirement_value=50000),
                Level(level_number=7, reward_amount=10000.00, requirement_type="APPROVED_WASTE_KG", requirement_value=10),
                Level(level_number=8, reward_amount=20000.00, requirement_type="APPROVED_WASTE_KG", requirement_value=10),
                Level(level_number=9, reward_amount=30000.00, requirement_type="APPROVED_WASTE_KG", requirement_value=10),
                Level(level_number=10, reward_amount=40000.00, requirement_type="APPROVED_WASTE_KG", requirement_value=10),
                Level(level_number=11, reward_amount=50000.00, requirement_type="APPROVED_WASTE_KG", requirement_value=10)
            ]
            db.bulk_save_objects(levels)
            
        # 2. Seed settings
        if not db.query(SystemSetting).first():
            settings = [
                SystemSetting(id=uuid.uuid4(), setting_key="OTP_EXPIRY_MINUTES", setting_value="5"),
                SystemSetting(id=uuid.uuid4(), setting_key="MAX_LOGIN_ATTEMPTS", setting_value="5"),
                SystemSetting(id=uuid.uuid4(), setting_key="JWT_ACCESS_TOKEN_MINUTES", setting_value="30"),
                SystemSetting(id=uuid.uuid4(), setting_key="JWT_REFRESH_TOKEN_DAYS", setting_value="30"),
                SystemSetting(id=uuid.uuid4(), setting_key="LEADER_REFERRAL_MAX_USAGE", setting_value="1"),
                SystemSetting(id=uuid.uuid4(), setting_key="CLAIM_LOCK_DAYS", setting_value="30")
            ]
            db.bulk_save_objects(settings)

        # 3. Seed collection centers
        if not db.query(CollectionCenter).first():
            centers = [
                CollectionCenter(id=uuid.UUID("00000000-0000-7000-0000-00000000030a"), center_name="Athiyaman Collection Center - Madurai", state="Tamil Nadu", district="Madurai", pincode="625001", door_no="No 5", street_name="Temple View", post_office="Madurai GPO", city="Madurai", is_active=True)
            ]
            db.bulk_save_objects(centers)

        # 4. Seed system users (admin)
        admin_id = uuid.UUID("00000000-0000-7000-0000-00000000000a")
        if not db.query(User).filter(User.id == admin_id).first():
            from backend.utils.security import get_password_hash
            admin_user = User(
                id=admin_id,
                username="admin",
                phone_number="9999999990",
                password_hash=get_password_hash("admin123"),
                role="ADMIN",
                user_status="ACTIVE",
                is_verified=True
            )
            db.add(admin_user)
            db.flush()
            admin_profile = UserProfile(
                id=uuid.uuid4(),
                user_id=admin_id,
                full_name="System Administrator",
                profile_completion=100
            )
            db.add(admin_profile)

        # 5. Seed default referral code
        if not db.query(ReferralCode).filter(ReferralCode.code == "LEADER-001").first():
            ref_code = ReferralCode(
                id=uuid.uuid4(),
                code="LEADER-001",
                referral_type="LEADER",
                is_active=True,
                max_usage=10,
                used_count=0,
                expires_at=datetime.datetime.utcnow() + datetime.timedelta(days=1)
            )
            db.add(ref_code)
            
        db.commit()
    except Exception as e:
        print(f"Error seeding test DB: {e}")
        db.rollback()
    finally:
        db.close()

    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session(engine):
    """Create test database session"""
    connection = engine.connect()
    transaction = connection.begin()
    session = sessionmaker(autocommit=False, autoflush=False, bind=connection)()
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client(db_session):
    """Create test client with override database dependency"""
    def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app, base_url="http://testserver/api/v1") as test_client:
        yield test_client
    
    app.dependency_overrides.clear()

@pytest.fixture
def test_user_data():
    """Sample user data for testing"""
    return {
        "username": "testuser",
        "phone_number": "9876543210",
        "password": "TestPassword123!",
        "referral_code": "LEADER-001"
    }

@pytest.fixture
def test_admin_data():
    """Sample admin data for testing"""
    return {
        "username": "adminuser",
        "phone_number": "9876543211",
        "password": "AdminPassword123!",
        "role": "ADMIN"
    }

@pytest.fixture
def test_team_data():
    """Sample team data for testing"""
    return {
        "name": "Green Warriors",
        "description": "Community waste collection team",
        "location": "Madurai"
    }

@pytest.fixture
def test_waste_data():
    """Sample waste submission data"""
    return {
        "weight_kg": 25.5,
        "waste_type": "plastic",
        "collection_date": "2026-05-28",
        "location": "Collection Center A"
    }

@pytest.fixture
def authenticated_headers(client, test_user_data):
    """Get authenticated headers with JWT token"""
    # First register user to ensure they exist physically in the test DB
    signup_res = client.post("/auth/signup", json=test_user_data)
    
    # Then login to obtain a real token
    response = client.post("/auth/login", json={
        "username": test_user_data["username"],
        "password": test_user_data["password"]
    })
    
    if response.status_code == 200:
        token = response.json()["access_token"]
    else:
        # Fallback to direct JWT generation with a valid user UUID
        from backend.utils.security import create_access_token
        user_id = None
        if signup_res.status_code in [200, 201]:
            user_id = signup_res.json().get("id")
        
        user_id = user_id or "00000000-0000-0000-0000-000000000099"
        token = create_access_token(user_id=str(user_id), role="MEMBER")
    
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def admin_authenticated_headers(client):
    """Get authenticated headers for administrative user"""
    response = client.post("/auth/login", json={
        "username": "admin",
        "password": "admin123"
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
