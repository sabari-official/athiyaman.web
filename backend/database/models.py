import datetime
import enum
from sqlalchemy import (
    Column,
    String,
    Boolean,
    Integer,
    Text,
    DateTime,
    Date,
    Numeric,
    ForeignKey,
    Index,
    UniqueConstraint,
    JSON,
    UUID,
)
from sqlalchemy.dialects.postgresql import JSONB

# Use JSONB on PostgreSQL for performance, fallback to standard JSON on SQLite/others
JSON_TYPE = JSON().with_variant(JSONB, "postgresql")
from sqlalchemy.orm import relationship

from backend.core.database import Base
from backend.utils.uuid import uuidv7

# ==========================================
# CUSTOM MIXINS
# ==========================================

class TimestampMixin:
    """Mixin for entity creation and modification timestamps."""
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False,
    )

class SoftDeleteMixin:
    """Mixin to enable logical soft delete without physical deletion."""
    deleted_at = Column(DateTime, nullable=True)
    deleted_by = Column(UUID(as_uuid=True), nullable=True)

# ==========================================
# 15 NATIVE POSTGRESQL ENUMS
# ==========================================

class UserRole(str, enum.Enum):
    MEMBER = "MEMBER"
    LEADER = "LEADER"
    ADMIN = "ADMIN"
    DEVELOPER = "DEVELOPER"

class UserStatus(str, enum.Enum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    BLOCKED = "BLOCKED"
    DELETED = "DELETED"

class DocumentType(str, enum.Enum):
    AADHAAR = "AADHAAR"
    BANK_PROOF = "BANK_PROOF"
    PROFILE_PHOTO = "PROFILE_PHOTO"
    NOMINEE_PROOF = "NOMINEE_PROOF"

class VerificationStatus(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

class TeamStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    SUSPENDED = "SUSPENDED"

class ReferralType(str, enum.Enum):
    LEADER = "LEADER"
    TEAM = "TEAM"

class RequirementType(str, enum.Enum):
    MEMBER_COUNT = "MEMBER_COUNT"
    APPROVED_WASTE_KG = "APPROVED_WASTE_KG"

class WastePaymentStatus(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    PROCESSING = "PROCESSING"
    PAID = "PAID"
    FAILED = "FAILED"

class ClaimType(str, enum.Enum):
    TEAM = "TEAM"
    PERSONAL = "PERSONAL"

class ClaimStatus(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    PROCESSING = "PROCESSING"
    PAID = "PAID"

class PaymentBatchStatus(str, enum.Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class PaymentTransactionStatus(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    PROCESSING = "PROCESSING"
    PAID = "PAID"
    FAILED = "FAILED"

class NotificationTarget(str, enum.Enum):
    ALL = "ALL"
    MEMBER = "MEMBER"
    LEADER = "LEADER"
    ADMIN = "ADMIN"
    DEVELOPER = "DEVELOPER"
    USER = "USER"

class LogLevel(str, enum.Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class AnalyticsSnapshotType(str, enum.Enum):
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"

# ==========================================
# 27 SQLALCHEMY MODELS (DOMAIN MODULES)
# ==========================================

# ------------------------------------------
# MODULE 1: AUTHENTICATION & SECURITY
# ------------------------------------------

class User(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuidv7)
    username = Column(String(50), unique=True, nullable=False)
    phone_number = Column(String(15), unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    role = Column(String(20), default=UserRole.MEMBER, nullable=False)
    user_status = Column(String(20), default=UserStatus.PENDING, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    failed_login_attempts = Column(Integer, default=0, nullable=False)
    locked_until = Column(DateTime, nullable=True)
    last_login = Column(DateTime, nullable=True)
    must_change_password = Column(Boolean, default=False, nullable=False)
    password_changed_at = Column(DateTime, nullable=True)

    # Relationships
    profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    sessions = relationship("UserSession", back_populates="user", cascade="all, delete-orphan")
    documents = relationship("UserDocument", foreign_keys="UserDocument.user_id", back_populates="user", cascade="all, delete-orphan")
    rules_acceptances = relationship("RulesAcceptance", back_populates="user", cascade="all, delete-orphan")
    team_memberships = relationship("TeamMember", back_populates="member", uselist=False, cascade="all, delete-orphan")
    led_team = relationship("Team", back_populates="leader", uselist=False)

    __table_args__ = (
        Index("idx_users_username", "username"),
        Index("idx_users_phone_number", "phone_number"),
        Index("idx_users_role", "role"),
        Index("idx_users_user_status", "user_status"),
        Index("idx_users_created_at", "created_at"),
    )

class UserSession(Base, TimestampMixin):
    __tablename__ = "user_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuidv7)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    refresh_token = Column(Text, nullable=False)
    ip_address = Column(String(45), nullable=True)
    device_info = Column(Text, nullable=True)
    login_time = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    logout_time = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="sessions")

    __table_args__ = (
        Index("idx_user_sessions_user_id", "user_id"),
        Index("idx_user_sessions_login_time", "login_time"),
        Index("idx_user_sessions_created_at", "created_at"),
    )

class RulesAcceptance(Base):
    __tablename__ = "rules_acceptance"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuidv7)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    rules_version = Column(String(50), nullable=False)
    accepted_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    ip_address = Column(String(45), nullable=True)

    user = relationship("User", back_populates="rules_acceptances")

    __table_args__ = (
        Index("idx_rules_acceptance_user_id", "user_id"),
        Index("idx_rules_acceptance_accepted_at", "accepted_at"),
    )


# ------------------------------------------
# MODULE 2: PROFILE MANAGEMENT
# ------------------------------------------

class UserProfile(Base, TimestampMixin):
    __tablename__ = "user_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuidv7)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    profile_photo = Column(Text, nullable=True)
    full_name = Column(String(255), nullable=False)
    gender = Column(String(20), nullable=True)
    dob = Column(Date, nullable=True)
    email = Column(String(255), nullable=True)
    masked_aadhaar = Column(String(20), nullable=True)
    aadhaar_hash = Column(String(128), nullable=True)
    aadhaar_verified = Column(Boolean, default=False, nullable=False)
    profession = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    district = Column(String(100), nullable=True)
    pincode = Column(String(10), nullable=True)
    door_no = Column(String(50), nullable=True)
    street_name = Column(String(255), nullable=True)
    landmark = Column(String(255), nullable=True)
    post_office = Column(String(255), nullable=True)
    city = Column(String(100), nullable=True)
    
    bank_name = Column(String(255), nullable=True)
    account_number_encrypted = Column(Text, nullable=True)
    account_number_masked = Column(String(50), nullable=True)
    ifsc_code = Column(String(20), nullable=True)
    bank_verified = Column(Boolean, default=False, nullable=False)
    
    nominee_name = Column(String(255), nullable=True)
    nominee_relationship = Column(String(100), nullable=True)
    nominee_phone = Column(String(20), nullable=True)
    nominee_door_no = Column(String(50), nullable=True)
    nominee_street_name = Column(String(255), nullable=True)
    nominee_landmark = Column(String(255), nullable=True)
    nominee_post_office = Column(String(255), nullable=True)
    nominee_city = Column(String(100), nullable=True)
    nominee_district = Column(String(100), nullable=True)
    nominee_state = Column(String(100), nullable=True)
    nominee_pincode = Column(String(10), nullable=True)
    
    profile_completion = Column(Integer, default=0, nullable=False)

    user = relationship("User", back_populates="profile")

    __table_args__ = (
        Index("idx_user_profiles_full_name", "full_name"),
        Index("idx_user_profiles_district", "district"),
        Index("idx_user_profiles_state", "state"),
        Index("idx_user_profiles_pincode", "pincode"),
        Index("idx_user_profiles_aadhaar_hash", "aadhaar_hash"),
    )

class UserDocument(Base):
    __tablename__ = "user_documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuidv7)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    document_type = Column(String(30), nullable=False)
    file_path = Column(Text, nullable=False)
    verification_status = Column(String(20), default=VerificationStatus.PENDING, nullable=False)
    verified_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    verified_at = Column(DateTime, nullable=True)
    rejection_reason = Column(Text, nullable=True)
    uploaded_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    user = relationship("User", foreign_keys=[user_id], back_populates="documents")
    verifier = relationship("User", foreign_keys=[verified_by])

    __table_args__ = (
        UniqueConstraint("user_id", "document_type", name="uq_user_document_type"),
        Index("idx_user_documents_user_id", "user_id"),
        Index("idx_user_documents_document_type", "document_type"),
        Index("idx_user_documents_verification_status", "verification_status"),
    )


# ------------------------------------------
# MODULE 3: LEADER APPLICATIONS
# ------------------------------------------

class LeaderApplication(Base):
    __tablename__ = "leader_applications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuidv7)
    full_name = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(255), nullable=False)
    masked_aadhaar = Column(String(20), nullable=True)
    aadhaar_hash = Column(String(128), nullable=True)
    state = Column(String(100), nullable=False)
    district = Column(String(100), nullable=False)
    pincode = Column(String(10), nullable=False)
    door_no = Column(String(50), nullable=False)
    street_name = Column(String(255), nullable=False)
    landmark = Column(String(255), nullable=True)
    post_office = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    reason = Column(Text, nullable=True)
    status = Column(String(20), default=VerificationStatus.PENDING, nullable=False)
    reviewed_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    reviewed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    reviewer = relationship("User", foreign_keys=[reviewed_by])

    __table_args__ = (
        Index("idx_leader_applications_status", "status"),
        Index("idx_leader_applications_phone", "phone"),
        Index("idx_leader_applications_email", "email"),
        Index("idx_leader_applications_created_at", "created_at"),
        Index("idx_leader_applications_district", "district"),
        Index("idx_leader_applications_aadhaar_hash", "aadhaar_hash"),
    )


class MemberApplication(Base):
    __tablename__ = "member_applications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuidv7)
    full_name = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(255), nullable=False)
    masked_aadhaar = Column(String(20), nullable=True)
    aadhaar_hash = Column(String(128), nullable=True)
    state = Column(String(100), nullable=False)
    district = Column(String(100), nullable=False)
    pincode = Column(String(10), nullable=False)
    door_no = Column(String(50), nullable=False)
    street_name = Column(String(255), nullable=False)
    landmark = Column(String(255), nullable=True)
    post_office = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    status = Column(String(20), default=VerificationStatus.PENDING, nullable=False)
    assigned_team_id = Column(UUID(as_uuid=True), ForeignKey("teams.id", ondelete="SET NULL"), nullable=True)
    reviewed_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    reviewed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    reviewer = relationship("User", foreign_keys=[reviewed_by])
    assigned_team = relationship("Team", foreign_keys=[assigned_team_id])

    __table_args__ = (
        Index("idx_member_applications_status", "status"),
        Index("idx_member_applications_phone", "phone"),
        Index("idx_member_applications_created_at", "created_at"),
        Index("idx_member_applications_district", "district"),
        Index("idx_member_applications_aadhaar_hash", "aadhaar_hash"),
    )


# ------------------------------------------
# MODULE 4: TEAM MANAGEMENT
# ------------------------------------------

class Team(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "teams"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuidv7)
    team_code = Column(String(50), unique=True, nullable=False)
    team_name = Column(String(100), unique=True, nullable=False)
    leader_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"), unique=True, nullable=False)
    state = Column(String(100), nullable=False)
    district = Column(String(100), nullable=False)
    pincode = Column(String(10), nullable=False)
    door_no = Column(String(50), nullable=True)
    street_name = Column(String(255), nullable=False)
    landmark = Column(String(255), nullable=True)
    post_office = Column(String(255), nullable=False)
    city = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    member_count = Column(Integer, default=0, nullable=False)
    current_level = Column(Integer, default=1, nullable=False)
    status = Column(String(20), default=TeamStatus.ACTIVE, nullable=False)

    leader = relationship("User", back_populates="led_team")
    members = relationship("TeamMember", back_populates="team", cascade="all, delete-orphan")
    referrals = relationship("ReferralCode", back_populates="team", cascade="all, delete-orphan")
    level_progresses = relationship("TeamLevelProgress", back_populates="team", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_teams_current_level", "current_level"),
        Index("idx_teams_status", "status"),
        Index("idx_teams_district", "district"),
        Index("idx_teams_member_count", "member_count"),
        Index("idx_teams_created_at", "created_at"),
    )

class TeamMember(Base):
    __tablename__ = "team_members"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuidv7)
    team_id = Column(UUID(as_uuid=True), ForeignKey("teams.id", ondelete="RESTRICT"), nullable=False)
    member_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"), unique=True, nullable=False)
    joined_level = Column(Integer, default=1, nullable=False)
    joined_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    team = relationship("Team", back_populates="members")
    member = relationship("User", back_populates="team_memberships")

    __table_args__ = (
        Index("idx_team_members_team_id", "team_id"),
        Index("idx_team_members_joined_level", "joined_level"),
        Index("idx_team_members_joined_at", "joined_at"),
    )


# ------------------------------------------
# MODULE 5: REFERRALS
# ------------------------------------------

class ReferralCode(Base):
    __tablename__ = "referral_codes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuidv7)
    code = Column(String(50), unique=True, nullable=False)
    referral_type = Column(String(20), nullable=False)
    team_id = Column(UUID(as_uuid=True), ForeignKey("teams.id", ondelete="RESTRICT"), nullable=True)
    level_number = Column(Integer, nullable=True)
    generated_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    max_usage = Column(Integer, default=1, nullable=False)
    used_count = Column(Integer, default=0, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    team = relationship("Team", back_populates="referrals")
    generator = relationship("User")

    __table_args__ = (
        Index("idx_referral_codes_team_id", "team_id"),
        Index("idx_referral_codes_referral_type", "referral_type"),
        Index("idx_referral_codes_level_number", "level_number"),
        Index("idx_referral_codes_is_active", "is_active"),
        Index("idx_referral_codes_expires_at", "expires_at"),
        Index("idx_referral_codes_created_at", "created_at"),
        Index("idx_referral_codes_team_level", "team_id", "level_number"),
    )


# ------------------------------------------
# MODULE 6: LEVEL SYSTEM
# ------------------------------------------

class Level(Base):
    __tablename__ = "levels"

    id = Column(Integer, primary_key=True, autoincrement=True)
    level_number = Column(Integer, unique=True, nullable=False)
    reward_amount = Column(Numeric(12, 2), nullable=False)
    requirement_type = Column(String(30), nullable=False)
    requirement_value = Column(Integer, nullable=False)

class TeamLevelProgress(Base):
    __tablename__ = "team_level_progress"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuidv7)
    team_id = Column(UUID(as_uuid=True), ForeignKey("teams.id", ondelete="RESTRICT"), nullable=False)
    level_number = Column(Integer, nullable=False)
    current_progress = Column(Integer, default=0, nullable=False)
    completed = Column(Boolean, default=False, nullable=False)
    completed_at = Column(DateTime, nullable=True)

    team = relationship("Team", back_populates="level_progresses")

    __table_args__ = (
        UniqueConstraint("team_id", "level_number", name="uq_team_level"),
        Index("idx_team_level_progress_team_id", "team_id"),
        Index("idx_team_level_progress_level_number", "level_number"),
        Index("idx_team_level_progress_completed", "completed"),
    )

class PersonalLevelProgress(Base):
    __tablename__ = "personal_level_progress"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuidv7)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    level_number = Column(Integer, nullable=False)
    waste_kg = Column(Numeric(12, 3), default=0.000, nullable=False)
    completed = Column(Boolean, default=False, nullable=False)
    completed_at = Column(DateTime, nullable=True)

    user = relationship("User")

    __table_args__ = (
        UniqueConstraint("user_id", "level_number", name="uq_user_level"),
        Index("idx_personal_level_progress_user_id", "user_id"),
        Index("idx_personal_level_progress_level_number", "level_number"),
        Index("idx_personal_level_progress_completed", "completed"),
    )


# ------------------------------------------
# MODULE 7: COLLECTION CENTERS
# ------------------------------------------

class CollectionCenter(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "collection_centers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuidv7)
    center_name = Column(String(255), nullable=False)
    state = Column(String(100), nullable=False)
    district = Column(String(100), nullable=False)
    pincode = Column(String(10), nullable=False)
    door_no = Column(String(50), nullable=False)
    street_name = Column(String(255), nullable=False)
    landmark = Column(String(255), nullable=True)
    post_office = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    latitude = Column(Numeric(10, 8), nullable=True)
    longitude = Column(Numeric(11, 8), nullable=True)
    phone = Column(String(20), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

    __table_args__ = (
        Index("idx_collection_centers_district", "district"),
        Index("idx_collection_centers_pincode", "pincode"),
        Index("idx_collection_centers_is_active", "is_active"),
    )


# ------------------------------------------
# MODULE 8: WASTE MANAGEMENT
# ------------------------------------------

class WasteRecord(Base):
    __tablename__ = "waste_records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuidv7)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    center_id = Column(UUID(as_uuid=True), ForeignKey("collection_centers.id", ondelete="RESTRICT"), nullable=False)
    image_path = Column(Text, nullable=True)
    weight_kg = Column(Numeric(12, 3), nullable=False)
    collection_date = Column(Date, nullable=False)
    location = Column(Text, nullable=True)
    verification_status = Column(String(20), default=VerificationStatus.PENDING, nullable=False)
    verified_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    verified_at = Column(DateTime, nullable=True)
    rejection_reason = Column(Text, nullable=True)
    payment_status = Column(String(20), default=WastePaymentStatus.PENDING, nullable=False)
    amount_paid = Column(Numeric(12, 2), default=0.00, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    user = relationship("User", foreign_keys=[user_id])
    verifier = relationship("User", foreign_keys=[verified_by])
    center = relationship("CollectionCenter")
    status_history = relationship("WasteStatusHistory", back_populates="waste_record", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_waste_records_user_id", "user_id"),
        Index("idx_waste_records_center_id", "center_id"),
        Index("idx_waste_records_collection_date", "collection_date"),
        Index("idx_waste_records_created_at", "created_at"),
        Index("idx_waste_records_verification_status", "verification_status"),
        Index("idx_waste_records_payment_status", "payment_status"),
        Index("idx_waste_records_user_verif", "user_id", "verification_status"),
        Index("idx_waste_records_user_date", "user_id", "collection_date"),
    )

class WasteStatusHistory(Base):
    __tablename__ = "waste_status_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuidv7)
    waste_record_id = Column(UUID(as_uuid=True), ForeignKey("waste_records.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(50), nullable=False)
    comments = Column(Text, nullable=True)
    updated_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    waste_record = relationship("WasteRecord", back_populates="status_history")
    updater = relationship("User")

    __table_args__ = (
        Index("idx_waste_status_history_record_id", "waste_record_id"),
        Index("idx_waste_status_history_updated_by", "updated_by"),
        Index("idx_waste_status_history_updated_at", "updated_at"),
    )


# ------------------------------------------
# MODULE 9: REWARD CLAIMS
# ------------------------------------------

class RewardClaim(Base):
    __tablename__ = "reward_claims"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuidv7)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    claim_type = Column(String(20), nullable=False)
    level_number = Column(Integer, nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    status = Column(String(20), default=ClaimStatus.PENDING, nullable=False)
    is_locked = Column(Boolean, default=False, nullable=False)
    reviewed_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    reviewed_at = Column(DateTime, nullable=True)
    rejection_reason = Column(Text, nullable=True)
    requested_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    user = relationship("User", foreign_keys=[user_id])
    reviewer = relationship("User", foreign_keys=[reviewed_by])
    transaction = relationship("PaymentTransaction", back_populates="claim", uselist=False)

    __table_args__ = (
        UniqueConstraint("user_id", "level_number", "claim_type", name="uq_user_level_claim"),
        Index("idx_reward_claims_user_id", "user_id"),
        Index("idx_reward_claims_status", "status"),
        Index("idx_reward_claims_claim_type", "claim_type"),
        Index("idx_reward_claims_requested_at", "requested_at"),
        Index("idx_reward_claims_user_status", "user_id", "status"),
        Index("idx_reward_claims_type_status", "claim_type", "status"),
    )


# ------------------------------------------
# MODULE 10: PAYMENT PROCESSING
# ------------------------------------------

class PaymentBatch(Base):
    __tablename__ = "payment_batches"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuidv7)
    batch_name = Column(String(255), nullable=False)
    total_transactions = Column(Integer, default=0, nullable=False)
    total_amount = Column(Numeric(15, 2), default=0.00, nullable=False)
    status = Column(String(20), default=PaymentBatchStatus.PENDING, nullable=False)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    creator = relationship("User")
    items = relationship("PaymentBatchItem", back_populates="batch", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_payment_batches_status", "status"),
        Index("idx_payment_batches_created_at", "created_at"),
        Index("idx_payment_batches_created_by", "created_by"),
    )

class PaymentTransaction(Base):
    __tablename__ = "payment_transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuidv7)
    claim_id = Column(UUID(as_uuid=True), ForeignKey("reward_claims.id", ondelete="RESTRICT"), unique=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    transaction_reference = Column(String(255), nullable=True)
    status = Column(String(20), default=PaymentTransactionStatus.PENDING, nullable=False)
    paid_at = Column(DateTime, nullable=True)

    claim = relationship("RewardClaim", back_populates="transaction")
    user = relationship("User")
    batch_item = relationship("PaymentBatchItem", back_populates="transaction", uselist=False, cascade="all, delete-orphan")
    audit_logs = relationship("PaymentAuditLog", back_populates="payment", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_payment_transactions_user_id", "user_id"),
        Index("idx_payment_transactions_status", "status"),
        Index("idx_payment_transactions_paid_at", "paid_at"),
        Index("idx_payment_transactions_user_status", "user_id", "status"),
    )

class PaymentBatchItem(Base):
    __tablename__ = "payment_batch_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuidv7)
    batch_id = Column(UUID(as_uuid=True), ForeignKey("payment_batches.id", ondelete="CASCADE"), nullable=False)
    payment_transaction_id = Column(UUID(as_uuid=True), ForeignKey("payment_transactions.id", ondelete="RESTRICT"), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    batch = relationship("PaymentBatch", back_populates="items")
    transaction = relationship("PaymentTransaction", back_populates="batch_item")

    __table_args__ = (
        Index("idx_payment_batch_items_batch_id", "batch_id"),
        Index("idx_payment_batch_items_transaction_id", "payment_transaction_id"),
    )

class PaymentAuditLog(Base):
    __tablename__ = "payment_audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuidv7)
    payment_id = Column(UUID(as_uuid=True), ForeignKey("payment_transactions.id", ondelete="RESTRICT"), nullable=False)
    action = Column(String(100), nullable=False)
    performed_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    old_status = Column(String(50), nullable=True)
    new_status = Column(String(50), nullable=True)
    remarks = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    payment = relationship("PaymentTransaction", back_populates="audit_logs")
    performer = relationship("User")

    __table_args__ = (
        Index("idx_payment_audit_logs_payment_id", "payment_id"),
        Index("idx_payment_audit_logs_performed_by", "performed_by"),
        Index("idx_payment_audit_logs_created_at", "created_at"),
    )


# ------------------------------------------
# MODULE 11: NOTIFICATIONS & ANNOUNCEMENTS
# ------------------------------------------

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuidv7)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    target_type = Column(String(30), default=NotificationTarget.ALL, nullable=False)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    creator = relationship("User")
    logs = relationship("NotificationLog", back_populates="notification", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_notifications_target_type", "target_type"),
        Index("idx_notifications_created_by", "created_by"),
        Index("idx_notifications_created_at", "created_at"),
    )

class NotificationLog(Base):
    __tablename__ = "notification_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuidv7)
    notification_id = Column(UUID(as_uuid=True), ForeignKey("notifications.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    delivered = Column(Boolean, default=False, nullable=False)
    delivered_at = Column(DateTime, nullable=True)
    is_read = Column(Boolean, default=False, nullable=False)
    read_at = Column(DateTime, nullable=True)

    notification = relationship("Notification", back_populates="logs")
    user = relationship("User")

    __table_args__ = (
        Index("idx_notification_logs_user_id", "user_id"),
        Index("idx_notification_logs_notification_id", "notification_id"),
        Index("idx_notification_logs_is_read", "is_read"),
        Index("idx_notification_logs_delivered", "delivered"),
        Index("idx_notification_logs_user_unread", "user_id", "is_read"),
    )

class Announcement(Base):
    __tablename__ = "announcements"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuidv7)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

    creator = relationship("User")

    __table_args__ = (
        Index("idx_announcements_is_active", "is_active"),
        Index("idx_announcements_start_date", "start_date"),
        Index("idx_announcements_end_date", "end_date"),
    )


# ------------------------------------------
# MODULE 12: SYSTEM AUDIT & LOGGING
# ------------------------------------------

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuidv7)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    role = Column(String(50), nullable=True)
    action = Column(String(100), nullable=False)
    entity_type = Column(String(100), nullable=False)
    entity_id = Column(UUID(as_uuid=True), nullable=True)
    old_values = Column(JSON_TYPE, nullable=True)
    new_values = Column(JSON_TYPE, nullable=True)
    ip_address = Column(String(45), nullable=True)
    device = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    user = relationship("User")

    __table_args__ = (
        Index("idx_audit_logs_user_id", "user_id"),
        Index("idx_audit_logs_role", "role"),
        Index("idx_audit_logs_action", "action"),
        Index("idx_audit_logs_entity_type", "entity_type"),
        Index("idx_audit_logs_created_at", "created_at"),
        Index("idx_audit_logs_user_created", "user_id", "created_at"),
        Index("idx_audit_logs_entity_created", "entity_type", "created_at"),
    )

class SystemLog(Base):
    __tablename__ = "system_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuidv7)
    log_level = Column(String(20), nullable=False)
    source = Column(String(100), nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    __table_args__ = (
        Index("idx_system_logs_log_level", "log_level"),
        Index("idx_system_logs_source", "source"),
        Index("idx_system_logs_created_at", "created_at"),
    )


# ------------------------------------------
# MODULE 13: SYSTEM ANALYTICS
# ------------------------------------------

class AnalyticsSnapshot(Base):
    __tablename__ = "analytics_snapshots"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuidv7)
    metric_name = Column(String(100), nullable=False)
    metric_value = Column(Numeric(15, 3), nullable=False)
    snapshot_date = Column(Date, nullable=False)
    snapshot_type = Column(String(20), nullable=False)

    __table_args__ = (
        Index("idx_analytics_snapshots_metric_name", "metric_name"),
        Index("idx_analytics_snapshots_snapshot_date", "snapshot_date"),
        Index("idx_analytics_snapshots_snapshot_type", "snapshot_type"),
        Index("idx_analytics_snapshots_metric_date", "metric_name", "snapshot_date"),
    )


# ------------------------------------------
# MODULE 14: SYSTEM SETTINGS
# ------------------------------------------

class SystemSetting(Base):
    __tablename__ = "system_settings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuidv7)
    setting_key = Column(String(100), unique=True, nullable=False)
    setting_value = Column(Text, nullable=False)
    updated_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False,
    )

    updater = relationship("User")

    __table_args__ = (
        Index("idx_system_settings_key", "setting_key"),
    )
