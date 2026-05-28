-- =========================================================
-- ATHIYAMAN PLATFORM — DIGITAL INDIA (PHASE 1)
-- SEED DATA SPECIFICATION (POSTGRESQL INSERT SCRIPT)
-- Version: 1.0.0
-- Status: Production & Development Seeding
-- =========================================================

-- Clear existing seed data (optional, only for fresh setups)
DELETE FROM system_settings;
DELETE FROM levels;
DELETE FROM collection_centers;
DELETE FROM announcements;
DELETE FROM users CASCADE;

-- =========================================================
-- 1. SEED MODULE: SYSTEM SETTINGS
-- =========================================================
INSERT INTO system_settings (id, setting_key, setting_value, updated_at) VALUES 
('00000000-0000-7000-0000-000000000101', 'OTP_EXPIRY_MINUTES', '5', CURRENT_TIMESTAMP),
('00000000-0000-7000-0000-000000000102', 'MAX_LOGIN_ATTEMPTS', '5', CURRENT_TIMESTAMP),
('00000000-0000-7000-0000-000000000103', 'ACCOUNT_LOCK_DURATION_MINUTES', '30', CURRENT_TIMESTAMP),
('00000000-0000-7000-0000-000000000104', 'JWT_ACCESS_TOKEN_MINUTES', '30', CURRENT_TIMESTAMP),
('00000000-0000-7000-0000-000000000105', 'JWT_REFRESH_TOKEN_DAYS', '30', CURRENT_TIMESTAMP),
('00000000-0000-7000-0000-000000000106', 'REFERRAL_EXPIRY_HOURS', '72', CURRENT_TIMESTAMP),
('00000000-0000-7000-0000-000000000107', 'LEADER_REFERRAL_MAX_USAGE', '1', CURRENT_TIMESTAMP),
('00000000-0000-7000-0000-000000000108', 'CLAIM_LOCK_DAYS', '30', CURRENT_TIMESTAMP),
('00000000-0000-7000-0000-000000000109', 'AUTO_CLOSE_FAILED_CLAIMS', 'TRUE', CURRENT_TIMESTAMP),
('00000000-0000-7000-0000-000000000110', 'PAYMENT_BATCH_SIZE', '5000', CURRENT_TIMESTAMP),
('00000000-0000-7000-0000-000000000111', 'PAYMENT_PROVIDER', 'RAZORPAYX', CURRENT_TIMESTAMP),
('00000000-0000-7000-0000-000000000112', 'PAYMENT_APPROVAL_REQUIRED', 'TRUE', CURRENT_TIMESTAMP),
('00000000-0000-7000-0000-000000000113', 'EMAIL_ENABLED', 'TRUE', CURRENT_TIMESTAMP),
('00000000-0000-7000-0000-000000000114', 'INAPP_ENABLED', 'TRUE', CURRENT_TIMESTAMP),
('00000000-0000-7000-0000-000000000115', 'ANNOUNCEMENT_ENABLED', 'TRUE', CURRENT_TIMESTAMP),
('00000000-0000-7000-0000-000000000116', 'AADHAAR_ENCRYPTION_ENABLED', 'TRUE', CURRENT_TIMESTAMP),
('00000000-0000-7000-0000-000000000117', 'BANK_ENCRYPTION_ENABLED', 'TRUE', CURRENT_TIMESTAMP),
('00000000-0000-7000-0000-000000000118', 'RATE_LIMIT_ENABLED', 'TRUE', CURRENT_TIMESTAMP);

-- =========================================================
-- 2. SEED MODULE: LEVEL CONFIGURATIONS
-- =========================================================
INSERT INTO levels (level_number, reward_amount, requirement_type, requirement_value) VALUES 
(1, 100.00, 'MEMBER_COUNT', 10),
(2, 1000.00, 'MEMBER_COUNT', 90),
(3, 2000.00, 'MEMBER_COUNT', 720),
(4, 3000.00, 'MEMBER_COUNT', 5040),
(5, 4000.00, 'MEMBER_COUNT', 30240),
(6, 5000.00, 'MEMBER_COUNT', 50000),
(7, 10000.00, 'APPROVED_WASTE_KG', 10),
(8, 20000.00, 'APPROVED_WASTE_KG', 10),
(9, 30000.00, 'APPROVED_WASTE_KG', 10),
(10, 40000.00, 'APPROVED_WASTE_KG', 10),
(11, 50000.00, 'APPROVED_WASTE_KG', 10);

-- =========================================================
-- 3. SEED MODULE: SYSTEM ROLES & USERS
-- =========================================================

-- Root Administrator (Password: admin123 -> Bcrypt representation)
INSERT INTO users (id, username, phone_number, password_hash, role, user_status, is_verified, must_change_password, created_at, updated_at) VALUES 
('00000000-0000-7000-0000-000000000001', 'admin', '9999999990', '$2b$12$K8M.a8g.J6p64VbW7DEXZ.qU.R78F0T1P8j5e1s2v3t4o5r6q7u8w', 'ADMIN', 'ACTIVE', TRUE, TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT INTO user_profiles (id, user_id, full_name, profile_completion, created_at, updated_at) VALUES 
('00000000-0000-7000-0000-000000000201', '00000000-0000-7000-0000-000000000001', 'System Administrator', 100, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- System Developer (Password: dev123 -> Bcrypt representation)
INSERT INTO users (id, username, phone_number, password_hash, role, user_status, is_verified, must_change_password, created_at, updated_at) VALUES 
('00000000-0000-7000-0000-000000000002', 'developer', '8888888888', '$2b$12$R78F0T1P8j5e1s2v3t4o5r6q7u8w.K8M.a8g.J6p64VbW7DEXZ.qU', 'DEVELOPER', 'ACTIVE', TRUE, TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT INTO user_profiles (id, user_id, full_name, profile_completion, created_at, updated_at) VALUES 
('00000000-0000-7000-0000-000000000202', '00000000-0000-7000-0000-000000000002', 'System Developer', 100, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- =========================================================
-- 4. SEED MODULE: COLLECTION CENTERS (TEST DATA)
-- =========================================================
INSERT INTO collection_centers (id, center_name, state, district, pincode, door_no, street_name, landmark, post_office, city, latitude, longitude, phone, is_active, created_at, updated_at) VALUES 
('00000000-0000-7000-0000-000000000301', 'Athiyaman Collection Center - Chennai', 'Tamil Nadu', 'Chennai', '600001', 'No 1', 'Beach Road', 'Near Fort', 'Chennai GPO', 'Chennai', 13.0827, 80.2707, '9999999991', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('00000000-0000-7000-0000-000000000302', 'Athiyaman Collection Center - Madurai', 'Tamil Nadu', 'Madurai', '625001', 'No 5', 'Temple View', 'Near Meenakshi Amman', 'Madurai GPO', 'Madurai', 9.9252, 78.1198, '9999999992', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('00000000-0000-7000-0000-000000000303', 'Athiyaman Collection Center - Coimbatore', 'Tamil Nadu', 'Coimbatore', '641001', 'No 12', 'Avinashi Road', 'Near Peelamedu', 'Coimbatore GPO', 'Coimbatore', 11.0168, 76.9558, '9999999993', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- =========================================================
-- 5. SEED MODULE: ANNOUNCEMENTS
-- =========================================================
INSERT INTO announcements (id, title, message, start_date, end_date, created_by, is_active) VALUES 
('00000000-0000-7000-0000-000000000401', 'Welcome To Athiyaman Platform', 'Welcome to the digital transformation portal under Digital India Phase 1.', '2026-01-01', '2027-12-31', '00000000-0000-7000-0000-000000000001', TRUE);

-- =========================================================
-- 6. SEED MODULE: INITIAL ANALYTICS SNAPSHOTS
-- =========================================================
INSERT INTO analytics_snapshots (id, metric_name, metric_value, snapshot_date, snapshot_type) VALUES 
('00000000-0000-7000-0000-000000000501', 'TOTAL_USERS', 0.000, '2026-05-26', 'DAILY'),
('00000000-0000-7000-0000-000000000502', 'TOTAL_TEAMS', 0.000, '2026-05-26', 'DAILY'),
('00000000-0000-7000-0000-000000000503', 'TOTAL_MEMBERS', 0.000, '2026-05-26', 'DAILY'),
('00000000-0000-7000-0000-000000000504', 'TOTAL_WASTE_KG', 0.000, '2026-05-26', 'DAILY'),
('00000000-0000-7000-0000-000000000505', 'TOTAL_PAYMENTS', 0.000, '2026-05-26', 'DAILY'),
('00000000-0000-7000-0000-000000000506', 'TOTAL_CLAIMS', 0.000, '2026-05-26', 'DAILY');
