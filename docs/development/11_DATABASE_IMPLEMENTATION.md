# Athiyaman Platform - Database Implementation Document
## Phase 1 – Digital India PostgreSQL Implementation Instructions & SQL Blueprints

---

## 1. PostgreSQL Installation Strategy

*   **Production Database Engine:** Enforces PostgreSQL v15+ installed on standard Linux servers.
*   **Installation Command:** Use standard packages to install PostgreSQL:
    ```bash
    sudo apt update
    sudo apt install -y postgresql-15 postgresql-client-15
    ```
*   **Service Operations:** Set the PostgreSQL service to start automatically on system boot:
    ```bash
    sudo systemctl enable postgresql
    sudo systemctl start postgresql
    ```
*   **System Resource Optimizations:** Modify `/etc/postgresql/15/main/postgresql.conf` configurations:
    *   `shared_buffers`: Allocate $25\%$ of total system RAM.
    *   `work_mem`: Set to `64MB` to optimize transactional sorting.
    *   `maintenance_work_mem`: Set to `256MB` to optimize index build operations.
    *   `effective_cache_size`: Allocate $50\%$ of system memory for database caching.
*   **Connection Pool Strategy:** Deploy **PgBouncer** locally as a connection pool manager, configuring PgBouncer to handle active pool distributions under port $6432$.

---

## 2. Database Creation Strategy

*   **User Provisioning:** Create a dedicated, unprivileged database owner user account (`athiyaman_db_user`), avoiding standard administrative accounts:
    ```sql
    CREATE USER athiyaman_db_user WITH PASSWORD 'SecureDatabasePassword123!';
    ```
*   **Database Initializations:** Create the primary production database instance (`athiyaman_digital_india`), assigning the new user as owner:
    ```sql
    CREATE DATABASE athiyaman_digital_india OWNER athiyaman_db_user ENCODING 'UTF8';
    ```
*   **Access Privileges configuration:** Revoke public schema creation rights:
    ```sql
    REVOKE ALL ON SCHEMA public FROM PUBLIC;
    GRANT ALL ON SCHEMA public TO athiyaman_db_user;
    ```
*   **Local Connection Configurations:** Edit `/etc/postgresql/15/main/pg_hba.conf` to restrict connections, denying external IP lookups:
    ```ini
    # IPv4 local connections only
    host    athiyaman_digital_india    athiyaman_db_user    127.0.0.1/32    scram-sha-256
    host    athiyaman_digital_india    athiyaman_db_user    ::1/128         scram-sha-256
    ```

---

## 3. Schema Creation Order

To maintain data integrity, database schemas and components must be deployed in a strict sequential order:

```
┌────────────────────────────────────────────────────────┐
│             Step 1: SQL Extension Installs             │
├────────────────────────────────────────────────────────┤
│             Step 2: Database ENUM Assemblies           │
├────────────────────────────────────────────────────────┤
│          Step 3: Reference Lookup Tables (Levels)      │
├────────────────────────────────────────────────────────┤
│           Step 4: Primary Entities (Users, Teams)      │
├────────────────────────────────────────────────────────┤
│          Step 5: Secondary Workflow Ledgers            │
├────────────────────────────────────────────────────────┤
│            Step 6: Indexes & Triggers setup            │
└────────────────────────────────────────────────────────┘
```

1.  **SQL Extension Installs:** Install extensions (such as `pgcrypto` for encryption, `uuid-ossp` for legacy keys) in the public database schema.
2.  **Database ENUM Assemblies:** Register custom status types before creating tables.
3.  **Reference Lookup Tables:** Deploy tables that do not have foreign key dependencies (e.g., `levels`, `collection_centers`).
4.  **Primary Entities:** Deploy core tables (`users`, `user_profiles`, `teams`).
5.  **Secondary Workflow Ledgers:** Deploy child tables (`team_members`, `waste_records`, `reward_claims`).
6.  **Indexes & Triggers Setup:** Define indexes, write triggers to enforce immutable audit trails, and configure backup scripts.

---

## 4. Enum Creation Order

Register the following custom status types in the database public schema:

```sql
-- 1. User Status Enum
CREATE TYPE user_status_enum AS ENUM ('REGISTERED', 'ACTIVE', 'SUSPENDED');

-- 2. Application Status Enum
CREATE TYPE application_status_enum AS ENUM ('SUBMITTED', 'PENDING', 'APPROVED', 'REJECTED');

-- 3. Referral Status Enum
CREATE TYPE referral_status_enum AS ENUM ('ACTIVE', 'EXPIRED', 'DISABLED');

-- 4. Waste Verification Status Enum
CREATE TYPE waste_status_enum AS ENUM ('SUBMITTED', 'PENDING_VERIFICATION', 'APPROVED', 'REJECTED');

-- 5. Payout Claim Status Enum
CREATE TYPE claim_status_enum AS ENUM ('INITIATED', 'PENDING_AUDIT', 'APPROVED', 'REJECTED');

-- 6. Payment Transaction Status Enum
CREATE TYPE payment_status_enum AS ENUM ('PENDING_PAYMENT', 'PROCESSING', 'PAID', 'FAILED');

-- 7. Document Type Enum
CREATE TYPE document_type_enum AS ENUM ('AADHAAR', 'BANK_PROOF', 'PROFILE_PHOTO', 'NOMINEE_DOCUMENT');
```

---

## 5. Table Creation Order

Deploy database tables sequentially to prevent dependency conflicts during creation:

### 5.1 Step 1: Base Configuration & Reference Tables

```sql
-- 1. Levels Configuration Table
CREATE TABLE levels (
    id SERIAL PRIMARY KEY,
    level_number INTEGER UNIQUE NOT NULL,
    requirement_type VARCHAR(20) NOT NULL,
    requirement_value INTEGER NOT NULL,
    reward_amount DECIMAL(12, 2) NOT NULL
);

-- 2. Collection Centers Table
CREATE TABLE collection_centers (
    id UUID PRIMARY KEY,
    center_name VARCHAR(100) NOT NULL,
    district VARCHAR(50) NOT NULL,
    pincode VARCHAR(6) NOT NULL,
    address TEXT NOT NULL,
    latitude DECIMAL(9, 6) NOT NULL,
    longitude DECIMAL(9, 6) NOT NULL,
    phone VARCHAR(15) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);
```

### 5.2 Step 2: Primary Account & Profile Tables

```sql
-- 3. Users Table
CREATE TABLE users (
    id UUID PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    phone_number VARCHAR(15) UNIQUE NOT NULL,
    role VARCHAR(20) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- 4. User Profiles Table
CREATE TABLE user_profiles (
    id UUID PRIMARY KEY,
    user_id UUID UNIQUE NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    gender VARCHAR(10) NOT NULL,
    dob DATE NOT NULL,
    email VARCHAR(100) NOT NULL,
    aadhaar_encrypted TEXT NOT NULL,
    aadhaar_hash VARCHAR(64) UNIQUE NOT NULL,
    state VARCHAR(50) NOT NULL,
    district VARCHAR(50) NOT NULL,
    pincode VARCHAR(6) NOT NULL,
    address TEXT NOT NULL,
    bank_account_encrypted TEXT NOT NULL,
    profile_completion INTEGER DEFAULT 0 NOT NULL
);

-- 5. User Documents Table
CREATE TABLE user_documents (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    document_type document_type_enum NOT NULL,
    file_url TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'PENDING' NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- 6. Teams Table
CREATE TABLE teams (
    id UUID PRIMARY KEY,
    team_code VARCHAR(20) UNIQUE NOT NULL,
    team_name VARCHAR(100) UNIQUE NOT NULL,
    leader_id UUID UNIQUE NOT NULL,
    district VARCHAR(50) NOT NULL,
    area VARCHAR(100) NOT NULL,
    pincode VARCHAR(6) NOT NULL,
    current_level INTEGER DEFAULT 1 NOT NULL,
    member_count INTEGER DEFAULT 0 NOT NULL,
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);
```

### 5.3 Step 3: Referral & Progress Tables

```sql
-- 7. Team Members Table
CREATE TABLE team_members (
    id UUID PRIMARY KEY,
    team_id UUID NOT NULL,
    member_id UUID UNIQUE NOT NULL,
    joined_level INTEGER NOT NULL,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- 8. Referral Codes Table
CREATE TABLE referral_codes (
    id UUID PRIMARY KEY,
    code VARCHAR(30) UNIQUE NOT NULL,
    type VARCHAR(20) NOT NULL,
    team_id UUID,
    generated_by UUID NOT NULL,
    usage_count INTEGER DEFAULT 0 NOT NULL,
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- 9. Team Level Progress Table
CREATE TABLE team_level_progress (
    id UUID PRIMARY KEY,
    team_id UUID NOT NULL,
    level_number INTEGER NOT NULL,
    current_progress INTEGER DEFAULT 0 NOT NULL,
    completed BOOLEAN DEFAULT FALSE NOT NULL,
    completed_at TIMESTAMP
);

-- 10. Personal Level Progress Table
CREATE TABLE personal_level_progress (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    level_number INTEGER NOT NULL,
    waste_kg DECIMAL(8, 2) DEFAULT 0.00 NOT NULL,
    completed BOOLEAN DEFAULT FALSE NOT NULL,
    completed_at TIMESTAMP
);
```

### 5.4 Step 4: Waste, Claims, and Payments Tables

```sql
-- 11. Waste Records Table
CREATE TABLE waste_records (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    center_id UUID NOT NULL,
    weight_kg DECIMAL(6, 2) NOT NULL,
    image_url TEXT NOT NULL,
    verification_status waste_status_enum DEFAULT 'SUBMITTED' NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- 12. Reward Claims Table
CREATE TABLE reward_claims (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    claim_type VARCHAR(20) NOT NULL,
    level_number INTEGER NOT NULL,
    amount DECIMAL(12, 2) NOT NULL,
    status claim_status_enum DEFAULT 'INITIATED' NOT NULL,
    requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- 13. Payment Transactions Table
CREATE TABLE payment_transactions (
    id UUID PRIMARY KEY,
    claim_id UUID UNIQUE NOT NULL,
    user_id UUID NOT NULL,
    amount DECIMAL(12, 2) NOT NULL,
    transaction_reference VARCHAR(100),
    status payment_status_enum DEFAULT 'PENDING_PAYMENT' NOT NULL,
    paid_at TIMESTAMP
);
```

### 5.5 Step 5: Audits, Notifications, and Analytics Tables

```sql
-- 14. Audit Logs Table
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    role VARCHAR(30) NOT NULL,
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(50) NOT NULL,
    entity_id UUID,
    ip_address VARCHAR(45) NOT NULL,
    device TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- 15. User Sessions Table
CREATE TABLE user_sessions (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    logout_time TIMESTAMP,
    ip_address VARCHAR(45) NOT NULL
);

-- 16. Waste Status History Table
CREATE TABLE waste_status_history (
    id UUID PRIMARY KEY,
    waste_record_id UUID NOT NULL,
    status waste_status_enum NOT NULL,
    comments TEXT,
    updated_by UUID NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);
```

---

## 6. Foreign Key Creation Order

Add foreign key constraints to relational tables to ensure database integrity:

```sql
-- 1. Profiles to Users Link
ALTER TABLE user_profiles ADD CONSTRAINT fk_user_profiles_user_id FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE RESTRICT;

-- 2. Teams to Users (Leader) Link
ALTER TABLE teams ADD CONSTRAINT fk_teams_leader_id FOREIGN KEY (leader_id) REFERENCES users(id) ON DELETE RESTRICT;

-- 3. Team Members Linkages
ALTER TABLE team_members ADD CONSTRAINT fk_team_members_team_id FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE RESTRICT;
ALTER TABLE team_members ADD CONSTRAINT fk_team_members_member_id FOREIGN KEY (member_id) REFERENCES users(id) ON DELETE RESTRICT;

-- 4. Waste Records Linkages
ALTER TABLE waste_records ADD CONSTRAINT fk_waste_records_user_id FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE RESTRICT;
ALTER TABLE waste_records ADD CONSTRAINT fk_waste_records_center_id FOREIGN KEY (center_id) REFERENCES collection_centers(id) ON DELETE RESTRICT;

-- 5. Reward Claims Linkages
ALTER TABLE reward_claims ADD CONSTRAINT fk_reward_claims_user_id FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE RESTRICT;

-- 6. Payment Transactions Linkages
ALTER TABLE payment_transactions ADD CONSTRAINT fk_payment_transactions_claim_id FOREIGN KEY (claim_id) REFERENCES reward_claims(id) ON DELETE RESTRICT;
```

---

## 7. Index Creation Strategy

Create explicit database indexes on columns frequently searched or joined to optimize query performance:

```sql
-- 1. Username and Phone Search indexes
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_phone ON users(phone_number);

-- 2. Team Code and Name search indexes
CREATE INDEX idx_teams_code ON teams(team_code);
CREATE INDEX idx_teams_name ON teams(team_name);

-- 3. Referral code validation index
CREATE INDEX idx_referrals_code ON referral_codes(code);

-- 4. Waste Verification Queue index
CREATE INDEX idx_waste_verification ON waste_records(verification_status, created_at);

-- 5. Audit Log timestamps and users search indexes
CREATE INDEX idx_audit_created ON audit_logs(created_at DESC);
CREATE INDEX idx_audit_user ON audit_logs(user_id);
```

---

## 8. UUIDv7 Implementation Strategy

UUIDv7 identifiers combine timestamps with random numbers, ensuring database keys are sequential and time-ordered to optimize indexing speeds.

*   **UUIDv7 Generator SQL Function:** Create the following SQL function to generate UUIDv7 keys natively in PostgreSQL:
    ```sql
    CREATE OR REPLACE FUNCTION generate_uuid_v7()
    RETURNS uuid AS $$
    DECLARE
        unix_time_ms bigint;
        uuid_bytes bytea;
        rand_bytes bytea;
    BEGIN
        -- 1. Get current epoch timestamp in milliseconds
        unix_time_ms := (EXTRACT(EPOCH FROM clock_timestamp()) * 1000)::bigint;
        
        -- 2. Construct UUIDv7 timestamp bytes
        uuid_bytes := decode(lpad(to_hex(unix_time_ms), 12, '0'), 'hex');
        
        -- 3. Append random bytes
        rand_bytes := gen_random_bytes(10);
        uuid_bytes := uuid_bytes || rand_bytes;
        
        -- 4. Set UUIDv7 version and variant bits
        uuid_bytes := set_byte(uuid_bytes, 6, (get_byte(uuid_bytes, 6) & 15) | 112); -- Version 7
        uuid_bytes := set_byte(uuid_bytes, 8, (get_byte(uuid_bytes, 8) & 63) | 128); -- Variant 1
        
        RETURN encode(uuid_bytes, 'hex')::uuid;
    END;
    $$ LANGUAGE plpgsql VOLATILE;
    ```
*   **Enforcing Default Keys:** Set `generate_uuid_v7()` as the default value for primary keys in transactional tables:
    ```sql
    ALTER TABLE users ALTER COLUMN id SET DEFAULT generate_uuid_v7();
    ALTER TABLE teams ALTER COLUMN id SET DEFAULT generate_uuid_v7();
    ```

---

## 9. Audit Log Implementation Strategy

*   **Immutable Trigger Function:** Create a PL/pgSQL database trigger function to block `UPDATE` and `DELETE` queries targeting audit tables:
    ```sql
    CREATE OR REPLACE FUNCTION prevent_audit_log_mutation()
    RETURNS TRIGGER AS $$
    BEGIN
        -- Block update or delete queries
        RAISE EXCEPTION 'Audit logs are immutable. Mutations or deletions are prohibited.';
        RETURN NULL;
    END;
    $$ LANGUAGE plpgsql;
    ```
*   **Enforcing Trigger Constraints:** Configure database triggers on audit tables to block mutations:
    ```sql
    CREATE TRIGGER trg_immutable_audit_logs
    BEFORE UPDATE OR DELETE ON audit_logs
    FOR EACH ROW EXECUTE FUNCTION prevent_audit_log_mutation();
    ```

---

## 10. Aadhaar Encryption Strategy

*   **Encryption at Rest:** Plain text Aadhaar entries are encrypted before database writes using AES-256 algorithms.
*   **Aadhaar Duplicate Check:** Cryptographic hashes of Aadhaar numbers are saved in `aadhaar_hash` to detect duplicate profiles without storing plain text credentials.
*   **Implementation Steps:**
    ```sql
    -- 1. Enable pgcrypto extension
    CREATE EXTENSION IF NOT EXISTS pgcrypto;
    
    -- 2. Encrypt and save Aadhaar values
    INSERT INTO user_profiles (aadhaar_encrypted, aadhaar_hash)
    VALUES (
        pgp_sym_encrypt('123456789012', 'SystemSecretKey_32_bytes_min'),
        encode(digest('123456789012', 'sha256'), 'hex')
    );
    ```

---

## 11. Bank Data Encryption Strategy

*   **Banking details protection:** Bank account numbers and passbook scans are encrypted at rest using AES-256 algorithms, mapping details to `bank_account_encrypted` columns.
*   **Display Masking:** Dashboards display masked account numbers (e.g., `XXXXXX4589`), decrypting unmasked values only when authorized admins verify profiles.
*   **Access Audits:** Reading unmasked banking details is restricted to verified administrators and logs access events in the audit trail.

---

## 12. Soft Delete Strategy

*   **Relational Integrity Rules:** Transactional tables block physical database row deletions to protect audit histories.
*   **Anonymization Protocols:** Profiles marked for deletion undergo anonymization, removing contact details and PII while preserving historical records for audit compliance.
*   **Anonymization Trigger:**
    ```sql
    CREATE OR REPLACE FUNCTION anonymize_user_profile(user_uuid UUID)
    RETURNS void AS $$
    BEGIN
        UPDATE user_profiles
        SET 
            full_name = 'DEACTIVATED_CITIZEN',
            email = 'deleted_' || user_uuid || '@athiyaman.in',
            aadhaar_encrypted = 'MASKED_VALUE',
            aadhaar_hash = 'MASKED_HASH_' || user_uuid,
            bank_account_encrypted = 'MASKED_VALUE',
            address = 'DEACTIVATED'
        WHERE user_id = user_uuid;
        
        UPDATE users
        SET 
            password_hash = 'LOCKED',
            is_active = FALSE
        WHERE id = user_uuid;
    END;
    $$ LANGUAGE plpgsql;
    ```

---

## 13. Migration Strategy

*   **Alembic Schema migrations:** Schema modifications must use versioned Alembic scripts, keeping databases synchronized.
*   **Revision Standards:** Every migration script must include a rollback path (`down_revision`) to support system recoveries.
*   **Deployments Verification:** Run migration test suites on staging databases before pushing updates to production.

---

## 14. Alembic Structure

Configure Alembic environments to manage database schema evolutions:

```
alembic/
├── env.py              # Loads configurations and configures connection engines
├── README              # Documentation files
├── script.py.mako      # Code templates for new migration scripts
└── versions/           # Versioned migration script history (.py files)
    ├── 20260523_120000_create_base_tables.py
    └── 20260523_130000_add_waste_history.py
```

---

## 15. Backup Strategy

*   **Daily Full Backups:** Automated pg_dump scripts run daily during off-peak hours ($2\text{:00 AM}$).
*   **Hourly Incremental Backups:** Hourly write-ahead log (WAL) archiving ensures minimal data loss in case of hardware failures.
*   **Backup Verification:** Backups are encrypted and stored in independent, secure cloud storage buckets, running restore validation tests weekly to ensure backup integrity.

---

## 16. Recovery Strategy

*   **Point-in-Time Recovery (PITR):** Utilizes PostgreSQL WAL logs to restore database states to the exact second before a crash occurred.
*   **Recovery Steps:**
    1. Stop the active database service.
    2. Restore the latest daily full backup.
    3. Configure `recovery.signal` settings.
    4. Play back the write-ahead logs (WAL) to restore the state to the target timestamp.
    5. Restart the database service and verify keys and relational constraints.

---

## 17. Query Optimization Strategy

*   **Dashboard aggregates:** Precalculated snapshots avoid real-time query bottlenecks, ensuring fast dashboard load times.
*   **Relational Query Optimizations:** Avoid wildcards (`SELECT *`), specify required columns explicitly, and optimize joins using indexes.
*   **Payload Pagination:** Queries returning list rosters use pagination bounds to keep database query loads light.

---

## 18. Scaling Strategy

*   **PgBouncer Pool Managers:** Manage database connections using PgBouncer, preventing backend processes from exhausting connection pools.
*   **Read-Write Separation:** Route read-heavy analytical queries to secondary replica instances, reducing traffic loads on the primary database engine.
*   **Database Partitioning:** Prepare long-term audit tables for time-based partitioning to optimize search performance.

---

## 19. Future Expansion Strategy

*   **Skill India Integration (Phase 2):** Deploy new course, assignment, and certification tables under the public schema, linking to the `users` table via foreign keys.
*   **Clean India Integration (Phase 3):** Extend collection center registries and add processing logs without modifying existing relational keys.

---

## 20. Database Readiness Checklist

Before launching the database in production, ensure all items on this readiness checklist are completed:

*   [ ] **PostgreSQL Installation:** Confirm PostgreSQL v15+ is installed and pgBouncer is configured under port 6432.
*   [ ] **Relational Schemas:** Verify all tables are created sequentially and foreign key constraints are active.
*   [ ] **UUIDv7 Implementation:** Verify `generate_uuid_v7()` functions are active and configured as primary key defaults.
*   [ ] **PII Protections:** Confirm Aadhaar and bank details are encrypted at rest using AES-256.
*   [ ] **Audit Immutability:** Verify trigger functions block UPDATE and DELETE queries on audit logs.
*   [ ] **Backup Operations:** Verify cron backup scripts run daily, encrypting and storing backups off-site.
*   [ ] **Recovery Testing:** Confirm point-in-time recovery validations verify database restores successfully.

---

## 21. Conclusion

This Database Implementation Document (`11_DATABASE_IMPLEMENTATION.md`) establishes the absolute database schemas, UUIDv7 default key engines, constraint strategies, ENUM types, and backup recovery standards for the Athiyaman Platform – Digital India Phase 1. By detailing tables sequentially and providing complete SQL code templates, it serves as a complete implementation guide for database engineers. All SQL scripts, database migrations, and operational audits must adhere strictly to these principles, ensuring a highly secure, traceable, and scalable database.
