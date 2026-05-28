-- =========================================================
-- ATHIYAMAN PLATFORM — DIGITAL INDIA (PHASE 1)
-- PHYSICAL DATABASE SCHEMA (POSTGRESQL DDL)
-- Version: 1.0.0
-- Status: Production Ready with Native ENUMs
-- =========================================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =========================================================
-- 1. CLEAN EXISTING ENTITIES (If resetting)
-- =========================================================
DROP VIEW IF EXISTS vw_dashboard_statistics CASCADE;
DROP VIEW IF EXISTS vw_referral_summary CASCADE;
DROP VIEW IF EXISTS vw_collection_center_summary CASCADE;
DROP VIEW IF EXISTS vw_waste_summary CASCADE;
DROP VIEW IF EXISTS vw_claim_summary CASCADE;
DROP VIEW IF EXISTS vw_payment_summary CASCADE;
DROP VIEW IF EXISTS vw_member_summary CASCADE;
DROP VIEW IF EXISTS vw_team_summary CASCADE;

-- Drop Tables (to allow enum drop cascades)
DROP TABLE IF EXISTS system_settings CASCADE;
DROP TABLE IF EXISTS analytics_snapshots CASCADE;
DROP TABLE IF EXISTS system_logs CASCADE;
DROP TABLE IF EXISTS audit_logs CASCADE;
DROP TABLE IF EXISTS announcements CASCADE;
DROP TABLE IF EXISTS notification_logs CASCADE;
DROP TABLE IF EXISTS notifications CASCADE;
DROP TABLE IF EXISTS payment_audit_logs CASCADE;
DROP TABLE IF EXISTS payment_batch_items CASCADE;
DROP TABLE IF EXISTS payment_transactions CASCADE;
DROP TABLE IF EXISTS payment_batches CASCADE;
DROP TABLE IF EXISTS reward_claims CASCADE;
DROP TABLE IF EXISTS waste_status_history CASCADE;
DROP TABLE IF EXISTS waste_records CASCADE;
DROP TABLE IF EXISTS collection_centers CASCADE;
DROP TABLE IF EXISTS personal_level_progress CASCADE;
DROP TABLE IF EXISTS team_level_progress CASCADE;
DROP TABLE IF EXISTS levels CASCADE;
DROP TABLE IF EXISTS referral_codes CASCADE;
DROP TABLE IF EXISTS team_members CASCADE;
DROP TABLE IF EXISTS teams CASCADE;
DROP TABLE IF EXISTS leader_applications CASCADE;
DROP TABLE IF EXISTS member_applications CASCADE;
DROP TABLE IF EXISTS user_documents CASCADE;
DROP TABLE IF EXISTS user_profiles CASCADE;
DROP TABLE IF EXISTS rules_acceptance CASCADE;
DROP TABLE IF EXISTS user_sessions CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Drop Enums
DROP TYPE IF EXISTS user_role_enum CASCADE;
DROP TYPE IF EXISTS user_status_enum CASCADE;
DROP TYPE IF EXISTS document_type_enum CASCADE;
DROP TYPE IF EXISTS verification_status_enum CASCADE;
DROP TYPE IF EXISTS team_status_enum CASCADE;
DROP TYPE IF EXISTS referral_type_enum CASCADE;
DROP TYPE IF EXISTS requirement_type_enum CASCADE;
DROP TYPE IF EXISTS waste_payment_status_enum CASCADE;
DROP TYPE IF EXISTS claim_type_enum CASCADE;
DROP TYPE IF EXISTS claim_status_enum CASCADE;
DROP TYPE IF EXISTS payment_batch_status_enum CASCADE;
DROP TYPE IF EXISTS payment_transaction_status_enum CASCADE;
DROP TYPE IF EXISTS notification_target_enum CASCADE;
DROP TYPE IF EXISTS log_level_enum CASCADE;
DROP TYPE IF EXISTS analytics_snapshot_type_enum CASCADE;

-- =========================================================
-- 2. CREATE NATIVE POSTGRESQL ENUMS
-- =========================================================
CREATE TYPE user_role_enum AS ENUM ('MEMBER', 'LEADER', 'ADMIN', 'DEVELOPER');
CREATE TYPE user_status_enum AS ENUM ('PENDING', 'ACTIVE', 'SUSPENDED', 'BLOCKED', 'DELETED');
CREATE TYPE document_type_enum AS ENUM ('AADHAAR', 'BANK_PROOF', 'PROFILE_PHOTO', 'NOMINEE_PROOF');
CREATE TYPE verification_status_enum AS ENUM ('PENDING', 'APPROVED', 'REJECTED');
CREATE TYPE team_status_enum AS ENUM ('ACTIVE', 'INACTIVE', 'SUSPENDED');
CREATE TYPE referral_type_enum AS ENUM ('LEADER', 'TEAM');
CREATE TYPE requirement_type_enum AS ENUM ('MEMBER_COUNT', 'APPROVED_WASTE_KG');
CREATE TYPE waste_payment_status_enum AS ENUM ('PENDING', 'APPROVED', 'PROCESSING', 'PAID', 'FAILED');
CREATE TYPE claim_type_enum AS ENUM ('TEAM', 'PERSONAL');
CREATE TYPE claim_status_enum AS ENUM ('PENDING', 'APPROVED', 'REJECTED', 'PROCESSING', 'PAID');
CREATE TYPE payment_batch_status_enum AS ENUM ('PENDING', 'PROCESSING', 'COMPLETED', 'FAILED');
CREATE TYPE payment_transaction_status_enum AS ENUM ('PENDING', 'APPROVED', 'PROCESSING', 'PAID', 'FAILED');
CREATE TYPE notification_target_enum AS ENUM ('ALL', 'MEMBER', 'LEADER', 'ADMIN', 'DEVELOPER', 'USER');
CREATE TYPE log_level_enum AS ENUM ('INFO', 'WARNING', 'ERROR', 'CRITICAL');
CREATE TYPE analytics_snapshot_type_enum AS ENUM ('DAILY', 'WEEKLY', 'MONTHLY');

-- =========================================================
-- 3. CREATE TABLES
-- =========================================================

-- users
CREATE TABLE users (
    id UUID PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    phone_number VARCHAR(15) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role user_role_enum NOT NULL DEFAULT 'MEMBER',
    user_status user_status_enum NOT NULL DEFAULT 'PENDING',
    is_verified BOOLEAN NOT NULL DEFAULT FALSE,
    failed_login_attempts INTEGER NOT NULL DEFAULT 0,
    locked_until TIMESTAMP NULL,
    last_login TIMESTAMP NULL,
    must_change_password BOOLEAN NOT NULL DEFAULT FALSE,
    password_changed_at TIMESTAMP NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    deleted_by UUID NULL
);

-- user_sessions
CREATE TABLE user_sessions (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    refresh_token TEXT NOT NULL,
    ip_address VARCHAR(45) NULL,
    device_info TEXT NULL,
    login_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    logout_time TIMESTAMP NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- rules_acceptance
CREATE TABLE rules_acceptance (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    rules_version VARCHAR(50) NOT NULL,
    accepted_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45) NULL
);

-- user_profiles
CREATE TABLE user_profiles (
    id UUID PRIMARY KEY,
    user_id UUID UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    profile_photo TEXT NULL,
    full_name VARCHAR(255) NOT NULL,
    gender VARCHAR(20) NULL,
    dob DATE NULL,
    email VARCHAR(255) NULL,
    masked_aadhaar VARCHAR(20) NULL,
    aadhaar_hash VARCHAR(128) NULL,
    aadhaar_verified BOOLEAN NOT NULL DEFAULT FALSE,
    profession VARCHAR(100) NULL,
    state VARCHAR(100) NULL,
    district VARCHAR(100) NULL,
    pincode VARCHAR(10) NULL,
    door_no VARCHAR(50) NULL,
    street_name VARCHAR(255) NULL,
    landmark VARCHAR(255) NULL,
    post_office VARCHAR(255) NULL,
    city VARCHAR(100) NULL,
    bank_name VARCHAR(255) NULL,
    account_number_encrypted TEXT NULL,
    account_number_masked VARCHAR(50) NULL,
    ifsc_code VARCHAR(20) NULL,
    bank_verified BOOLEAN NOT NULL DEFAULT FALSE,
    nominee_name VARCHAR(255) NULL,
    nominee_relationship VARCHAR(100) NULL,
    nominee_phone VARCHAR(20) NULL,
    nominee_door_no VARCHAR(50) NULL,
    nominee_street_name VARCHAR(255) NULL,
    nominee_landmark VARCHAR(255) NULL,
    nominee_post_office VARCHAR(255) NULL,
    nominee_city VARCHAR(100) NULL,
    nominee_district VARCHAR(100) NULL,
    nominee_state VARCHAR(100) NULL,
    nominee_pincode VARCHAR(10) NULL,
    profile_completion INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- user_documents
CREATE TABLE user_documents (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    document_type document_type_enum NOT NULL,
    file_path TEXT NOT NULL,
    verification_status verification_status_enum NOT NULL DEFAULT 'PENDING',
    verified_by UUID NULL REFERENCES users(id) ON DELETE SET NULL,
    verified_at TIMESTAMP NULL,
    rejection_reason TEXT NULL,
    uploaded_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_user_document_type UNIQUE(user_id, document_type)
);

-- leader_applications
CREATE TABLE leader_applications (
    id UUID PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(255) NOT NULL,
    masked_aadhaar VARCHAR(20) NULL,
    aadhaar_hash VARCHAR(128) NULL,
    state VARCHAR(100) NOT NULL,
    district VARCHAR(100) NOT NULL,
    pincode VARCHAR(10) NOT NULL,
    door_no VARCHAR(50) NOT NULL,
    street_name VARCHAR(255) NOT NULL,
    landmark VARCHAR(255) NULL,
    post_office VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    reason TEXT NULL,
    status verification_status_enum NOT NULL DEFAULT 'PENDING',
    reviewed_by UUID NULL REFERENCES users(id) ON DELETE SET NULL,
    reviewed_at TIMESTAMP NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- member_applications
CREATE TABLE member_applications (
    id UUID PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(255) NOT NULL,
    masked_aadhaar VARCHAR(20) NULL,
    aadhaar_hash VARCHAR(128) NULL,
    state VARCHAR(100) NOT NULL,
    district VARCHAR(100) NOT NULL,
    pincode VARCHAR(10) NOT NULL,
    door_no VARCHAR(50) NOT NULL,
    street_name VARCHAR(255) NOT NULL,
    landmark VARCHAR(255) NULL,
    post_office VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    status verification_status_enum NOT NULL DEFAULT 'PENDING',
    assigned_team_id UUID NULL, -- No foreign key constraint until team table is created below
    reviewed_by UUID NULL REFERENCES users(id) ON DELETE SET NULL,
    reviewed_at TIMESTAMP NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- teams
CREATE TABLE teams (
    id UUID PRIMARY KEY,
    team_code VARCHAR(50) UNIQUE NOT NULL,
    team_name VARCHAR(100) UNIQUE NOT NULL,
    leader_id UUID UNIQUE NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    state VARCHAR(100) NOT NULL,
    district VARCHAR(100) NOT NULL,
    pincode VARCHAR(10) NOT NULL,
    door_no VARCHAR(50) NULL,
    street_name VARCHAR(255) NOT NULL,
    landmark VARCHAR(255) NULL,
    post_office VARCHAR(255) NOT NULL,
    city VARCHAR(100) UNIQUE NOT NULL, -- 1 Team per City constraint
    description TEXT NULL,
    member_count INTEGER NOT NULL DEFAULT 0,
    current_level INTEGER NOT NULL DEFAULT 1,
    status team_status_enum NOT NULL DEFAULT 'ACTIVE',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    deleted_by UUID NULL
);

-- team_members
CREATE TABLE team_members (
    id UUID PRIMARY KEY,
    team_id UUID NOT NULL REFERENCES teams(id) ON DELETE RESTRICT,
    member_id UUID UNIQUE NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    joined_level INTEGER NOT NULL DEFAULT 1,
    joined_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- referral_codes
CREATE TABLE referral_codes (
    id UUID PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    referral_type referral_type_enum NOT NULL,
    team_id UUID NULL REFERENCES teams(id) ON DELETE RESTRICT,
    level_number INTEGER NULL,
    generated_by UUID NULL REFERENCES users(id) ON DELETE SET NULL,
    max_usage INTEGER NOT NULL DEFAULT 1,
    used_count INTEGER NOT NULL DEFAULT 0,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- levels
CREATE TABLE levels (
    id SERIAL PRIMARY KEY,
    level_number INTEGER UNIQUE NOT NULL,
    reward_amount DECIMAL(12, 2) NOT NULL,
    requirement_type requirement_type_enum NOT NULL,
    requirement_value INTEGER NOT NULL
);

-- team_level_progress
CREATE TABLE team_level_progress (
    id UUID PRIMARY KEY,
    team_id UUID NOT NULL REFERENCES teams(id) ON DELETE RESTRICT,
    level_number INTEGER NOT NULL,
    current_progress INTEGER NOT NULL DEFAULT 0,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    completed_at TIMESTAMP NULL,
    CONSTRAINT uq_team_level UNIQUE(team_id, level_number)
);

-- personal_level_progress
CREATE TABLE personal_level_progress (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    level_number INTEGER NOT NULL,
    waste_kg DECIMAL(12, 3) NOT NULL DEFAULT 0.000,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    completed_at TIMESTAMP NULL,
    CONSTRAINT uq_user_level UNIQUE(user_id, level_number)
);

-- collection_centers
CREATE TABLE collection_centers (
    id UUID PRIMARY KEY,
    center_name VARCHAR(255) NOT NULL,
    state VARCHAR(100) NOT NULL,
    district VARCHAR(100) NOT NULL,
    pincode VARCHAR(10) NOT NULL,
    door_no VARCHAR(50) NOT NULL,
    street_name VARCHAR(255) NOT NULL,
    landmark VARCHAR(255) NULL,
    post_office VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    latitude DECIMAL(10, 8) NULL,
    longitude DECIMAL(11, 8) NULL,
    phone VARCHAR(20) NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    deleted_by UUID NULL
);

-- waste_records
CREATE TABLE waste_records (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    center_id UUID NOT NULL REFERENCES collection_centers(id) ON DELETE RESTRICT,
    image_path TEXT NULL,
    weight_kg DECIMAL(12, 3) NOT NULL,
    collection_date DATE NOT NULL,
    location TEXT NULL,
    verification_status verification_status_enum NOT NULL DEFAULT 'PENDING',
    verified_by UUID NULL REFERENCES users(id) ON DELETE SET NULL,
    verified_at TIMESTAMP NULL,
    rejection_reason TEXT NULL,
    payment_status waste_payment_status_enum NOT NULL DEFAULT 'PENDING',
    amount_paid DECIMAL(12, 2) NOT NULL DEFAULT 0.00,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- waste_status_history
CREATE TABLE waste_status_history (
    id UUID PRIMARY KEY,
    waste_record_id UUID NOT NULL REFERENCES waste_records(id) ON DELETE CASCADE,
    status VARCHAR(50) NOT NULL,
    comments TEXT NULL,
    updated_by UUID NULL REFERENCES users(id) ON DELETE SET NULL,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- reward_claims
CREATE TABLE reward_claims (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    claim_type claim_type_enum NOT NULL,
    level_number INTEGER NOT NULL,
    amount DECIMAL(12, 2) NOT NULL,
    status claim_status_enum NOT NULL DEFAULT 'PENDING',
    is_locked BOOLEAN NOT NULL DEFAULT FALSE,
    reviewed_by UUID NULL REFERENCES users(id) ON DELETE SET NULL,
    reviewed_at TIMESTAMP NULL,
    rejection_reason TEXT NULL,
    requested_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_user_level_claim UNIQUE(user_id, level_number, claim_type)
);

-- payment_batches
CREATE TABLE payment_batches (
    id UUID PRIMARY KEY,
    batch_name VARCHAR(255) NOT NULL,
    total_transactions INTEGER NOT NULL DEFAULT 0,
    total_amount DECIMAL(15, 2) NOT NULL DEFAULT 0.00,
    status payment_batch_status_enum NOT NULL DEFAULT 'PENDING',
    created_by UUID NULL REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- payment_transactions
CREATE TABLE payment_transactions (
    id UUID PRIMARY KEY,
    claim_id UUID UNIQUE NOT NULL REFERENCES reward_claims(id) ON DELETE RESTRICT,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    amount DECIMAL(12, 2) NOT NULL,
    transaction_reference VARCHAR(255) NULL,
    status payment_transaction_status_enum NOT NULL DEFAULT 'PENDING',
    paid_at TIMESTAMP NULL
);

-- payment_batch_items
CREATE TABLE payment_batch_items (
    id UUID PRIMARY KEY,
    batch_id UUID NOT NULL REFERENCES payment_batches(id) ON DELETE CASCADE,
    payment_transaction_id UUID UNIQUE NOT NULL REFERENCES payment_transactions(id) ON DELETE RESTRICT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- payment_audit_logs
CREATE TABLE payment_audit_logs (
    id UUID PRIMARY KEY,
    payment_id UUID NOT NULL REFERENCES payment_transactions(id) ON DELETE RESTRICT,
    action VARCHAR(100) NOT NULL,
    performed_by UUID NULL REFERENCES users(id) ON DELETE SET NULL,
    old_status VARCHAR(50) NULL,
    new_status VARCHAR(50) NULL,
    remarks TEXT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- notifications
CREATE TABLE notifications (
    id UUID PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    target_type notification_target_enum NOT NULL DEFAULT 'ALL',
    created_by UUID NULL REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- notification_logs
CREATE TABLE notification_logs (
    id UUID PRIMARY KEY,
    notification_id UUID NOT NULL REFERENCES notifications(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    delivered BOOLEAN NOT NULL DEFAULT FALSE,
    delivered_at TIMESTAMP NULL,
    is_read BOOLEAN NOT NULL DEFAULT FALSE,
    read_at TIMESTAMP NULL
);

-- announcements
CREATE TABLE announcements (
    id UUID PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    created_by UUID NULL REFERENCES users(id) ON DELETE SET NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

-- audit_logs
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY,
    user_id UUID NULL REFERENCES users(id) ON DELETE SET NULL,
    role VARCHAR(50) NULL,
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(100) NOT NULL,
    entity_id UUID NULL,
    old_values JSONB NULL,
    new_values JSONB NULL,
    ip_address VARCHAR(45) NULL,
    device TEXT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- system_logs
CREATE TABLE system_logs (
    id UUID PRIMARY KEY,
    log_level log_level_enum NOT NULL,
    source VARCHAR(100) NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- analytics_snapshots
CREATE TABLE analytics_snapshots (
    id UUID PRIMARY KEY,
    metric_name VARCHAR(100) NOT NULL,
    metric_value DECIMAL(15, 3) NOT NULL,
    snapshot_date DATE NOT NULL,
    snapshot_type analytics_snapshot_type_enum NOT NULL
);

-- system_settings
CREATE TABLE system_settings (
    id UUID PRIMARY KEY,
    setting_key VARCHAR(100) UNIQUE NOT NULL,
    setting_value TEXT NOT NULL,
    updated_by UUID NULL REFERENCES users(id) ON DELETE SET NULL,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- =========================================================
-- 4. CREATE INDEXES
-- =========================================================
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_phone_number ON users(phone_number);
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);
CREATE INDEX IF NOT EXISTS idx_users_user_status ON users(user_status);
CREATE INDEX IF NOT EXISTS idx_users_created_at ON users(created_at);

CREATE INDEX IF NOT EXISTS idx_user_sessions_user_id ON user_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_user_sessions_login_time ON user_sessions(login_time);
CREATE INDEX IF NOT EXISTS idx_user_sessions_created_at ON user_sessions(created_at);

CREATE INDEX IF NOT EXISTS idx_rules_acceptance_user_id ON rules_acceptance(user_id);
CREATE INDEX IF NOT EXISTS idx_rules_acceptance_accepted_at ON rules_acceptance(accepted_at);

CREATE INDEX IF NOT EXISTS idx_user_profiles_full_name ON user_profiles(full_name);
CREATE INDEX IF NOT EXISTS idx_user_profiles_district ON user_profiles(district);
CREATE INDEX IF NOT EXISTS idx_user_profiles_state ON user_profiles(state);
CREATE INDEX IF NOT EXISTS idx_user_profiles_pincode ON user_profiles(pincode);
CREATE INDEX IF NOT EXISTS idx_user_profiles_aadhaar_hash ON user_profiles(aadhaar_hash);

CREATE INDEX IF NOT EXISTS idx_user_documents_user_id ON user_documents(user_id);
CREATE INDEX IF NOT EXISTS idx_user_documents_document_type ON user_documents(document_type);
CREATE INDEX IF NOT EXISTS idx_user_documents_verification_status ON user_documents(verification_status);

CREATE INDEX IF NOT EXISTS idx_leader_applications_status ON leader_applications(status);
CREATE INDEX IF NOT EXISTS idx_leader_applications_phone ON leader_applications(phone);
CREATE INDEX IF NOT EXISTS idx_leader_applications_email ON leader_applications(email);
CREATE INDEX IF NOT EXISTS idx_leader_applications_created_at ON leader_applications(created_at);
CREATE INDEX IF NOT EXISTS idx_leader_applications_district ON leader_applications(district);
CREATE INDEX IF NOT EXISTS idx_leader_applications_aadhaar_hash ON leader_applications(aadhaar_hash);

CREATE INDEX IF NOT EXISTS idx_teams_current_level ON teams(current_level);
CREATE INDEX IF NOT EXISTS idx_teams_status ON teams(status);
CREATE INDEX IF NOT EXISTS idx_teams_district ON teams(district);
CREATE INDEX IF NOT EXISTS idx_teams_member_count ON teams(member_count);
CREATE INDEX IF NOT EXISTS idx_teams_created_at ON teams(created_at);

CREATE INDEX IF NOT EXISTS idx_team_members_team_id ON team_members(team_id);
CREATE INDEX IF NOT EXISTS idx_team_members_joined_level ON team_members(joined_level);
CREATE INDEX IF NOT EXISTS idx_team_members_joined_at ON team_members(joined_at);

CREATE INDEX IF NOT EXISTS idx_referral_codes_team_id ON referral_codes(team_id);
CREATE INDEX IF NOT EXISTS idx_referral_codes_referral_type ON referral_codes(referral_type);
CREATE INDEX IF NOT EXISTS idx_referral_codes_level_number ON referral_codes(level_number);
CREATE INDEX IF NOT EXISTS idx_referral_codes_is_active ON referral_codes(is_active);
CREATE INDEX IF NOT EXISTS idx_referral_codes_expires_at ON referral_codes(expires_at);
CREATE INDEX IF NOT EXISTS idx_referral_codes_created_at ON referral_codes(created_at);
CREATE INDEX IF NOT EXISTS idx_referral_codes_composite ON referral_codes(team_id, level_number);

CREATE INDEX IF NOT EXISTS idx_team_level_progress_team_id ON team_level_progress(team_id);
CREATE INDEX IF NOT EXISTS idx_team_level_progress_level_number ON team_level_progress(level_number);
CREATE INDEX IF NOT EXISTS idx_team_level_progress_completed ON team_level_progress(completed);

CREATE INDEX IF NOT EXISTS idx_personal_level_progress_user_id ON personal_level_progress(user_id);
CREATE INDEX IF NOT EXISTS idx_personal_level_progress_level_number ON personal_level_progress(level_number);
CREATE INDEX IF NOT EXISTS idx_personal_level_progress_completed ON personal_level_progress(completed);

CREATE INDEX IF NOT EXISTS idx_collection_centers_district ON collection_centers(district);
CREATE INDEX IF NOT EXISTS idx_collection_centers_pincode ON collection_centers(pincode);
CREATE INDEX IF NOT EXISTS idx_collection_centers_is_active ON collection_centers(is_active);

CREATE INDEX IF NOT EXISTS idx_waste_records_user_id ON waste_records(user_id);
CREATE INDEX IF NOT EXISTS idx_waste_records_center_id ON waste_records(center_id);
CREATE INDEX IF NOT EXISTS idx_waste_records_collection_date ON waste_records(collection_date);
CREATE INDEX IF NOT EXISTS idx_waste_records_created_at ON waste_records(created_at);
CREATE INDEX IF NOT EXISTS idx_waste_records_verification_status ON waste_records(verification_status);
CREATE INDEX IF NOT EXISTS idx_waste_records_payment_status ON waste_records(payment_status);
CREATE INDEX IF NOT EXISTS idx_waste_records_user_verif ON waste_records(user_id, verification_status);
CREATE INDEX IF NOT EXISTS idx_waste_records_user_date ON waste_records(user_id, collection_date);

CREATE INDEX IF NOT EXISTS idx_waste_status_history_record_id ON waste_status_history(waste_record_id);
CREATE INDEX IF NOT EXISTS idx_waste_status_history_updated_by ON waste_status_history(updated_by);
CREATE INDEX IF NOT EXISTS idx_waste_status_history_updated_at ON waste_status_history(updated_at);

CREATE INDEX IF NOT EXISTS idx_reward_claims_user_id ON reward_claims(user_id);
CREATE INDEX IF NOT EXISTS idx_reward_claims_status ON reward_claims(status);
CREATE INDEX IF NOT EXISTS idx_reward_claims_claim_type ON reward_claims(claim_type);
CREATE INDEX IF NOT EXISTS idx_reward_claims_requested_at ON reward_claims(requested_at);
CREATE INDEX IF NOT EXISTS idx_reward_claims_user_status ON reward_claims(user_id, status);
CREATE INDEX IF NOT EXISTS idx_reward_claims_type_status ON reward_claims(claim_type, status);

CREATE INDEX IF NOT EXISTS idx_payment_batches_status ON payment_batches(status);
CREATE INDEX IF NOT EXISTS idx_payment_batches_created_at ON payment_batches(created_at);
CREATE INDEX IF NOT EXISTS idx_payment_batches_created_by ON payment_batches(created_by);

CREATE INDEX IF NOT EXISTS idx_payment_transactions_user_id ON payment_transactions(user_id);
CREATE INDEX IF NOT EXISTS idx_payment_transactions_status ON payment_transactions(status);
CREATE INDEX IF NOT EXISTS idx_payment_transactions_paid_at ON payment_transactions(paid_at);
CREATE INDEX IF NOT EXISTS idx_payment_transactions_user_status ON payment_transactions(user_id, status);

CREATE INDEX IF NOT EXISTS idx_payment_batch_items_batch_id ON payment_batch_items(batch_id);
CREATE INDEX IF NOT EXISTS idx_payment_batch_items_transaction_id ON payment_batch_items(payment_transaction_id);

CREATE INDEX IF NOT EXISTS idx_payment_audit_logs_payment_id ON payment_audit_logs(payment_id);
CREATE INDEX IF NOT EXISTS idx_payment_audit_logs_performed_by ON payment_audit_logs(performed_by);
CREATE INDEX IF NOT EXISTS idx_payment_audit_logs_created_at ON payment_audit_logs(created_at);

CREATE INDEX IF NOT EXISTS idx_notifications_target_type ON notifications(target_type);
CREATE INDEX IF NOT EXISTS idx_notifications_created_by ON notifications(created_by);
CREATE INDEX IF NOT EXISTS idx_notifications_created_at ON notifications(created_at);

CREATE INDEX IF NOT EXISTS idx_notification_logs_user_id ON notification_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_notification_logs_notification_id ON notification_logs(notification_id);
CREATE INDEX IF NOT EXISTS idx_notification_logs_is_read ON notification_logs(is_read);
CREATE INDEX IF NOT EXISTS idx_notification_logs_delivered ON notification_logs(delivered);
CREATE INDEX IF NOT EXISTS idx_notification_logs_user_unread ON notification_logs(user_id, is_read);

CREATE INDEX IF NOT EXISTS idx_announcements_is_active ON announcements(is_active);
CREATE INDEX IF NOT EXISTS idx_announcements_start_date ON announcements(start_date);
CREATE INDEX IF NOT EXISTS idx_announcements_end_date ON announcements(end_date);

CREATE INDEX IF NOT EXISTS idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_role ON audit_logs(role);
CREATE INDEX IF NOT EXISTS idx_audit_logs_action ON audit_logs(action);
CREATE INDEX IF NOT EXISTS idx_audit_logs_entity_type ON audit_logs(entity_type);
CREATE INDEX IF NOT EXISTS idx_audit_logs_created_at ON audit_logs(created_at);
CREATE INDEX IF NOT EXISTS idx_audit_logs_user_created ON audit_logs(user_id, created_at);
CREATE INDEX IF NOT EXISTS idx_audit_logs_entity_created ON audit_logs(entity_type, created_at);

CREATE INDEX IF NOT EXISTS idx_system_logs_log_level ON system_logs(log_level);
CREATE INDEX IF NOT EXISTS idx_system_logs_source ON system_logs(source);
CREATE INDEX IF NOT EXISTS idx_system_logs_created_at ON system_logs(created_at);

CREATE INDEX IF NOT EXISTS idx_analytics_snapshots_metric_name ON analytics_snapshots(metric_name);
CREATE INDEX IF NOT EXISTS idx_analytics_snapshots_snapshot_date ON analytics_snapshots(snapshot_date);
CREATE INDEX IF NOT EXISTS idx_analytics_snapshots_snapshot_type ON analytics_snapshots(snapshot_type);
CREATE INDEX IF NOT EXISTS idx_analytics_snapshots_composite ON analytics_snapshots(metric_name, snapshot_date);

CREATE INDEX IF NOT EXISTS idx_system_settings_key ON system_settings(setting_key);


-- =========================================================
-- 5. CREATE DATABASE TRIGGERS
-- =========================================================

-- Trigger 1: Team Member Counter Function
CREATE OR REPLACE FUNCTION fn_team_member_counter()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        UPDATE teams SET member_count = member_count + 1 WHERE id = NEW.team_id;
    ELSIF TG_OP = 'DELETE' THEN
        UPDATE teams SET member_count = member_count - 1 WHERE id = OLD.team_id;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_team_member_counter
AFTER INSERT OR DELETE ON team_members
FOR EACH ROW EXECUTE FUNCTION fn_team_member_counter();


-- Trigger 2: Referral Usage Counter Function
CREATE OR REPLACE FUNCTION fn_referral_usage_counter()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE referral_codes
    SET used_count = used_count + 1
    WHERE team_id = NEW.team_id AND is_active = TRUE;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_referral_usage_counter
AFTER INSERT ON team_members
FOR EACH ROW EXECUTE FUNCTION fn_referral_usage_counter();


-- Trigger 3: Referral Auto Expiration Function
CREATE OR REPLACE FUNCTION fn_referral_auto_expiration()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.used_count >= NEW.max_usage THEN
        NEW.is_active := FALSE;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_referral_auto_expiration
BEFORE UPDATE OF used_count ON referral_codes
FOR EACH ROW EXECUTE FUNCTION fn_referral_auto_expiration();


-- Trigger 4: Team Level Completion Function
CREATE OR REPLACE FUNCTION fn_team_level_completion()
RETURNS TRIGGER AS $$
DECLARE
    req_val INT;
    lvl INT;
BEGIN
    FOR lvl IN 1..6 LOOP
        CASE lvl
            WHEN 1 THEN req_val := 10;
            WHEN 2 THEN req_val := 90;
            WHEN 3 THEN req_val := 720;
            WHEN 4 THEN req_val := 5040;
            WHEN 5 THEN req_val := 30240;
            WHEN 6 THEN req_val := 50000;
        END CASE;

        IF NEW.member_count >= req_val THEN
            INSERT INTO team_level_progress (id, team_id, level_number, current_progress, completed, completed_at)
            VALUES (gen_random_uuid(), NEW.id, lvl, NEW.member_count, TRUE, CURRENT_TIMESTAMP)
            ON CONFLICT (team_id, level_number) DO UPDATE
            SET current_progress = NEW.member_count,
                completed = TRUE,
                completed_at = COALESCE(team_level_progress.completed_at, CURRENT_TIMESTAMP);

            IF lvl > NEW.current_level THEN
                NEW.current_level := lvl;
            END IF;
        END IF;
    END LOOP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_team_level_completion
BEFORE UPDATE OF member_count ON teams
FOR EACH ROW EXECUTE FUNCTION fn_team_level_completion();


-- Trigger 5: Personal Level Completion Function
CREATE OR REPLACE FUNCTION fn_personal_level_completion()
RETURNS TRIGGER AS $$
DECLARE
    total_waste NUMERIC(12,3);
    lvl RECORD;
BEGIN
    SELECT COALESCE(SUM(weight_kg), 0) INTO total_waste
    FROM waste_records
    WHERE user_id = NEW.user_id AND verification_status = 'APPROVED';

    FOR lvl IN SELECT level_number, requirement_value FROM levels WHERE level_number >= 7 AND level_number <= 11 ORDER BY level_number LOOP
        IF total_waste >= (lvl.requirement_value * (lvl.level_number - 6)) THEN
            INSERT INTO personal_level_progress (id, user_id, level_number, waste_kg, completed, completed_at)
            VALUES (gen_random_uuid(), NEW.user_id, lvl.level_number, total_waste, TRUE, CURRENT_TIMESTAMP)
            ON CONFLICT (user_id, level_number) DO UPDATE
            SET waste_kg = total_waste,
                completed = TRUE,
                completed_at = COALESCE(personal_level_progress.completed_at, CURRENT_TIMESTAMP);
        ELSE
            INSERT INTO personal_level_progress (id, user_id, level_number, waste_kg, completed, completed_at)
            VALUES (gen_random_uuid(), NEW.user_id, lvl.level_number, total_waste, FALSE, NULL)
            ON CONFLICT (user_id, level_number) DO UPDATE
            SET waste_kg = total_waste;
        END IF;
    END LOOP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_personal_level_completion
AFTER UPDATE OF verification_status ON waste_records
FOR EACH ROW
WHEN (NEW.verification_status = 'APPROVED')
EXECUTE FUNCTION fn_personal_level_completion();


-- Trigger 6: Payment Audit Function
CREATE OR REPLACE FUNCTION fn_payment_audit()
RETURNS TRIGGER AS $$
BEGIN
    IF OLD.status IS DISTINCT FROM NEW.status THEN
        INSERT INTO payment_audit_logs (id, payment_id, action, performed_by, old_status, new_status, remarks, created_at)
        VALUES (
            gen_random_uuid(),
            NEW.id,
            'STATUS_CHANGE',
            NEW.user_id,
            OLD.status,
            NEW.status,
            'Status updated successfully.',
            CURRENT_TIMESTAMP
        );
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_payment_audit
AFTER UPDATE OF status ON payment_transactions
FOR EACH ROW EXECUTE FUNCTION fn_payment_audit();


-- Trigger 7: Immutable Audit Log Function
CREATE OR REPLACE FUNCTION fn_immutable_audit()
RETURNS TRIGGER AS $$
BEGIN
    RAISE EXCEPTION 'Audit logs are immutable. Updates and Deletions are forbidden on this table.';
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_immutable_audit
BEFORE UPDATE OR DELETE ON audit_logs
FOR EACH ROW EXECUTE FUNCTION fn_immutable_audit();


-- =========================================================
-- 6. CREATE REPORTING VIEWS
-- =========================================================

-- View 1: Team Summary
CREATE OR REPLACE VIEW vw_team_summary AS
SELECT
    t.team_name,
    p.full_name AS leader,
    t.current_level,
    t.member_count,
    t.status
FROM teams t
JOIN users u ON t.leader_id = u.id
LEFT JOIN user_profiles p ON u.id = p.user_id;

-- View 2: Member Summary
CREATE OR REPLACE VIEW vw_member_summary AS
SELECT
    u.username,
    t.team_name AS team,
    COALESCE((SELECT MAX(level_number) FROM personal_level_progress WHERE user_id = u.id AND completed = TRUE), 0) AS personal_level,
    COALESCE((SELECT SUM(weight_kg) FROM waste_records WHERE user_id = u.id AND verification_status = 'APPROVED'), 0) AS approved_waste_kg
FROM users u
LEFT JOIN team_members tm ON u.id = tm.member_id
LEFT JOIN teams t ON tm.team_id = t.id;

-- View 3: Payment Summary
CREATE OR REPLACE VIEW vw_payment_summary AS
SELECT
    COUNT(pt.id) AS total_claims,
    COALESCE(SUM(CASE WHEN pt.status = 'APPROVED' THEN pt.amount ELSE 0 END), 0) AS total_approved,
    COALESCE(SUM(CASE WHEN pt.status = 'PAID' THEN pt.amount ELSE 0 END), 0) AS total_paid,
    COALESCE(SUM(CASE WHEN pt.status = 'FAILED' THEN pt.amount ELSE 0 END), 0) AS total_failed
FROM payment_transactions pt;

-- View 4: Claim Summary
CREATE OR REPLACE VIEW vw_claim_summary AS
SELECT
    COALESCE(SUM(CASE WHEN status = 'PENDING' THEN 1 ELSE 0 END), 0) AS pending_claims,
    COALESCE(SUM(CASE WHEN status = 'APPROVED' THEN 1 ELSE 0 END), 0) AS approved_claims,
    COALESCE(SUM(CASE WHEN status = 'REJECTED' THEN 1 ELSE 0 END), 0) AS rejected_claims
FROM reward_claims;

-- View 5: Waste Summary
CREATE OR REPLACE VIEW vw_waste_summary AS
SELECT
    p.district,
    COALESCE(SUM(w.weight_kg), 0) AS total_waste,
    COALESCE(SUM(CASE WHEN w.verification_status = 'APPROVED' THEN w.weight_kg ELSE 0 END), 0) AS approved_waste,
    COALESCE(SUM(CASE WHEN w.verification_status = 'REJECTED' THEN w.weight_kg ELSE 0 END), 0) AS rejected_waste
FROM waste_records w
JOIN user_profiles p ON w.user_id = p.user_id
GROUP BY p.district;

-- View 6: Collection Center Summary
CREATE OR REPLACE VIEW vw_collection_center_summary AS
SELECT
    cc.center_name,
    COUNT(w.id) AS waste_count,
    COALESCE(SUM(w.weight_kg), 0) AS total_weight
FROM collection_centers cc
LEFT JOIN waste_records w ON cc.id = w.center_id
GROUP BY cc.id, cc.center_name;

-- View 7: Referral Summary
CREATE OR REPLACE VIEW vw_referral_summary AS
SELECT
    t.team_name AS team,
    r.code AS current_referral,
    r.used_count,
    (r.max_usage - r.used_count) AS remaining_slots
FROM referral_codes r
JOIN teams t ON r.team_id = t.id
WHERE r.is_active = TRUE;

-- View 8: Dashboard Statistics
CREATE OR REPLACE VIEW vw_dashboard_statistics AS
SELECT
    (SELECT COUNT(*) FROM users) AS total_users,
    (SELECT COUNT(*) FROM teams) AS total_teams,
    (SELECT COUNT(*) FROM team_members) AS total_members,
    (SELECT COALESCE(SUM(weight_kg), 0) FROM waste_records WHERE verification_status = 'APPROVED') AS total_waste,
    (SELECT COUNT(*) FROM reward_claims) AS total_claims,
    (SELECT COALESCE(SUM(amount), 0) FROM payment_transactions WHERE status = 'PAID') AS total_payments;
