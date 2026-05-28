# Athiyaman Platform - Database Design Document
## Phase 1 – Digital India Logical Data Architecture Blueprint

---

## 1. Database Overview

This Database Design Document defines the logical data architecture of the Athiyaman Platform - Digital India Phase 1. It details the entity relationships, constraint policies, database indexes, and security controls required to build a highly secure, reliable, and auditable relational data ecosystem.

*   **Purpose:** To establish a central, relational database structure that ensures complete data traceability for citizens, teams, waste weights, and payouts.
*   **Objectives:**
    *   *Relational Integrity:* Enforce zero-orphan constraints across all tables.
    *   *Audit Traceability:* Capture and log every system-mutating transaction asynchronously.
    *   *Zero Security Vulnerabilities:* Native protection against SQL injection and unauthorized data access.
*   **Design Principles:** Normalization (3NF), separation of concerns, explicit validation boundaries, clean key strategies, and column isolation.
*   **Scalability Goals:** Relational optimizations supporting $500,000$ active users, $10\text{ million}$ audit entries, and concurrent requests.
*   **Security Goals:** Robust OAuth2 JWT session guards, Argon2 hashing, AES-256 rest-encryption of PII, and sanitization parameters.
*   **Auditability Goals:** Maintain a permanent, read-only audit ledger (`audit_logs`) that blocks updates or deletions.

---

## 2. Database Technology

The platform utilizes **PostgreSQL** as its core relational database engine, selected for its enterprise-grade dependability, ACID compliance, and low resource overhead.

*   **Why PostgreSQL:** It combines robust relational constraints with strong performance, index flexibility, and native JSONB support.
*   **Key Advantages:**
    *   *ACID Compliance:* Guarantees safe transactions, protecting database state from corruption during hardware or network failures.
    *   *JSONB Support:* Allows storing semi-structured metadata alongside strictly normalized tables, facilitating clean system configurations.
    *   *Asynchronous Snapshots Strategy:* Provides solid performance under heavy query loads.
*   **Scalability Benefits:** Supports high concurrency and connection pooling, keeping database query latencies low under operational loads.
*   **Future Expansion Support:** Relational tables and columns can be modified easily via Alembic migrations, enabling seamless integration of Phase 2 and 3 modules.

---

## 3. Database Architecture

The backend isolates database operations using a Clean Architecture design, keeping SQL queries separate from business rules.

```
[ FastAPI App ] <───(Schema DTOs)───> [ Service Logic ] <───(Repositories)───> [ PostgreSQL Engine ]
```

*   **Data Flow:** Endpoint routers receive JSON payloads, validate inputs against Pydantic schemas, and call pure business services. Services apply calculations and delegate database writes to Repositories via SQLAlchemy.
*   **Data Ownership:** Each module (e.g., Waste) is the sole owner of its database tables, accessing other tables via strict foreign keys.
*   **Data Integrity:** Enforces database constraints and transaction boundaries to prevent incomplete data states or record orphans during operations.

---

## 4. Entity Relationship Strategy

To maintain a clean, performant data footprint, the database organizes entities into five distinct operational tiers:

*   **Primary Entities:** Core system entities managing accounts, teams, and profiles (`users`, `teams`, `user_profiles`).
*   **Secondary Entities:** Entities linked to primary records to manage activity workflows (`waste_records`, `reward_claims`, `user_documents`).
*   **Reference Entities:** Static dictionaries detailing configuration parameters (`levels`, `collection_centers`).
*   **Audit Entities:** Immutable ledgers tracking security and operational transactions (`audit_logs`, `user_sessions`, `waste_status_history`).
*   **Analytics Entities:** Asynchronously compiled tables storing precalculated performance metrics (`analytics_snapshots`).

---

## 5. Entity Catalog

### 5.1 primary_entities

#### 5.1.1 users
*   *Purpose:* Stores account credentials, roles, and status states.
*   *Key Columns:* `id` (UUID, PK), `username` (VARCHAR, UNIQUE), `password_hash` (TEXT), `phone_number` (VARCHAR, UNIQUE), `role` (ENUM), `is_active` (BOOLEAN), `created_at` (TIMESTAMP).
*   *Relationships:* One-to-One with `user_profiles`, One-to-Many with `user_documents`, `user_sessions`, `waste_records`, `reward_claims`.

#### 5.1.2 user_profiles
*   *Purpose:* Stores personal biographical details and bank accounts.
*   *Key Columns:* `id` (UUID, PK), `user_id` (UUID, FK), `full_name` (VARCHAR), `dob` (DATE), `email` (VARCHAR), `aadhaar_number` (VARCHAR, Encrypted), `state` (VARCHAR), `district` (VARCHAR), `pincode` (VARCHAR), `profile_completion` (INTEGER).
*   *Relationships:* Many-to-One with `users`.

#### 5.1.3 teams
*   *Purpose:* Registers unique teams geocoded by local borders.
*   *Key Columns:* `id` (UUID, PK), `team_code` (VARCHAR, UNIQUE), `team_name` (VARCHAR, UNIQUE), `leader_id` (UUID, FK), `district` (VARCHAR), `pincode` (VARCHAR), `current_level` (INTEGER).
*   *Relationships:* One-to-Many with `team_members`, `team_level_progress`, `referral_codes`.

### 5.2 secondary_entities

#### 5.2.1 team_members
*   *Purpose:* Links Member accounts to their respective teams.
*   *Key Columns:* `id` (UUID, PK), `team_id` (UUID, FK), `member_id` (UUID, FK), `joined_level` (INTEGER), `joined_at` (TIMESTAMP).
*   *Relationships:* Many-to-One with `teams`, Many-to-One with `users`.

#### 5.2.2 referral_codes
*   *Purpose:* Manages single-use leader codes and multi-use team codes.
*   *Key Columns:* `id` (UUID, PK), `code` (VARCHAR, UNIQUE), `type` (ENUM), `team_id` (UUID, FK), `generated_by` (UUID, FK), `usage_count` (INTEGER), `is_active` (BOOLEAN).
*   *Relationships:* Many-to-One with `teams`, Many-to-One with `users`.

#### 5.2.3 waste_records
*   *Purpose:* Logs individual waste submissions, geocodes, and photos.
*   *Key Columns:* `id` (UUID, PK), `user_id` (UUID, FK), `center_id` (UUID, FK), `weight_kg` (DECIMAL), `image_url` (TEXT), `verification_status` (ENUM), `created_at` (TIMESTAMP).
*   *Relationships:* Many-to-One with `users`, Many-to-One with `collection_centers`.

#### 5.2.4 reward_claims
*   *Purpose:* Manages manual payout claims submitted by users.
*   *Key Columns:* `id` (UUID, PK), `user_id` (UUID, FK), `claim_type` (ENUM), `level_number` (INTEGER), `amount` (DECIMAL), `status` (ENUM), `requested_at` (TIMESTAMP).
*   *Relationships:* Many-to-One with `users`.

#### 5.2.5 user_documents
*   *Purpose:* Stores uploaded identity scans (Aadhaar cards, bank books).
*   *Key Columns:* `id` (UUID, PK), `user_id` (UUID, FK), `document_type` (ENUM), `file_url` (TEXT), `status` (ENUM), `uploaded_at` (TIMESTAMP).
*   *Relationships:* Many-to-One with `users`.

### 5.3 reference_entities

#### 5.3.1 levels
*   *Purpose:* Static configuration catalog defining progression milestones.
*   *Key Columns:* `id` (INTEGER, PK), `level_number` (INTEGER), `requirement_type` (ENUM), `requirement_value` (INTEGER), `reward_amount` (DECIMAL).
*   *Relationships:* Static lookup mappings.

#### 5.3.2 collection_centers
*   *Purpose:* Lists authorized centers geocoded by latitude/longitude.
*   *Key Columns:* `id` (UUID, PK), `center_name` (VARCHAR), `district` (VARCHAR), `pincode` (VARCHAR), `latitude` (DECIMAL), `longitude` (DECIMAL), `is_active` (BOOLEAN).
*   *Relationships:* One-to-Many with `waste_records`.

### 5.4 audit_entities

#### 5.4.1 user_sessions
*   *Purpose:* Tracks active sessions and device footprints.
*   *Key Columns:* `id` (UUID, PK), `user_id` (UUID, FK), `login_time` (TIMESTAMP), `logout_time` (TIMESTAMP), `ip_address` (VARCHAR).
*   *Relationships:* Many-to-One with `users`.

#### 5.4.2 waste_status_history
*   *Purpose:* Tracks every verification state transition.
*   *Key Columns:* `id` (UUID, PK), `waste_record_id` (UUID, FK), `status` (ENUM), `comments` (TEXT), `updated_by` (UUID, FK), `updated_at` (TIMESTAMP).
*   *Relationships:* Many-to-One with `waste_records`, Many-to-One with `users`.

#### 5.4.3 audit_logs
*   *Purpose:* Permanent, read-only system transaction log.
*   *Key Columns:* `id` (UUID, PK), `user_id` (UUID, FK), `role` (VARCHAR), `action` (VARCHAR), `entity_type` (VARCHAR), `entity_id` (UUID), `ip_address` (VARCHAR), `created_at` (TIMESTAMP).
*   *Relationships:* Many-to-One with `users`.

### 5.5 analytics_entities

#### 5.5.1 analytics_snapshots
*   *Purpose:* Stores precalculated performance metrics.
*   *Key Columns:* `id` (UUID, PK), `metric_name` (VARCHAR), `metric_value` (DECIMAL), `snapshot_date` (DATE).
*   *Relationships:* Static lookup aggregates.

---

## 6. User Domain

The user domain maps user credentials, roles, profiles, and active sessions.

```
┌────────────────────────────────────────────────────────┐
│                        users                           │
└───────────────────────────┬────────────────────────────┘
                            │ (One-to-One)
                            ▼
┌────────────────────────────────────────────────────────┐
│                     user_profiles                      │
└────────────────────────────────────────────────────────┘
```

*   **Relational Maps:** One-to-One between `users` and `user_profiles`. One-to-Many between `users` and `user_documents`, `user_sessions`, and `audit_logs`.
*   **Ownership Rules:** User Profiles inherit database context directly from the main User identity via foreign key linkages.
*   **User Lifecycle Lifecycle:**
    ```
    [REGISTERED] -> [ACTIVE] <-> [SUSPENDED]
    ```

---

## 7. Team Domain

The team domain maps team metadata, member linkages, and level progress logs.

```
┌────────────────────────────────────────────────────────┐
│                        teams                           │
└───────────────────────────┬────────────────────────────┘
                            │ (One-to-Many)
                            ▼
┌────────────────────────────────────────────────────────┐
│                     team_members                       │
└────────────────────────────────────────────────────────┘
```

*   **Relational Maps:** One-to-Many between `teams` and `team_members`. Many-to-One between `team_members` and the primary `users` table.
*   **Ownership Rules:** Leaders own their teams. Deleting or suspending a team leader account freezes team operations.
*   **Progress Tracking:** Tracks Level 1 to 6 milestones, verifying thresholds before unlocking claims.
*   **Team Member Counter Strategy:** Maintain precalculated `member_count` in the `teams` table to support teams with thousands of members. The database must increment `member_count` when a member joins and decrement it when a member leaves. User dashboards must read `member_count` directly, strictly prohibiting expensive SQL `COUNT` queries on `team_members` to protect connection pools.

---

## 8. Referral Domain

The referral domain manages invite creation, utilization tracking, and expirations.

*   **Relational Maps:** Many-to-One between `referral_codes` and `teams`.
*   **Referral Types:** Manages single-use `LEADER_REFERRAL` codes and multi-use `TEAM_REFERRAL` codes.
*   **Referral Lifecycle:**
    ```
    [GENERATED] -> [ACTIVE] -> [MAX_CAPACITY / EXPIRED / MANUALLY_DISABLED]
    ```

---

## 9. Level Domain

The level domain manages progression rules and milestone configurations.

*   **Progression Specifications:** Coordinates linear, sequential progression paths:
    *   *Team Levels (1–6):* Incremented by Leaders based on verified team size.
    *   *Personal Levels (7–11):* Incremented individually by all users based on approved waste weights.
*   **Balance Resets:** Personal level completion resets the active waste balance to $0\text{ KG}$ for the next level.

---

## 10. Waste Domain

The waste domain logs waste submissions, geocodes, and verification statuses.

```
┌────────────────────────────────────────────────────────┐
│                     waste_records                      │
└───────────────────────────┬────────────────────────────┘
                            │ (One-to-Many)
                            ▼
┌────────────────────────────────────────────────────────┐
│                 waste_status_history                   │
└────────────────────────────────────────────────────────┘
```

*   **Relational Maps:** One-to-Many between `waste_records` and `waste_status_history`.
*   **Verification Timeline:** Submissions route to the Admin Verification Queue. Status transitions are logged in `waste_status_history`.

---

## 11. Collection Center Domain

The collection center domain registers geocoded physical collection centers.

*   **Location Specifications:** Centers map latitude/longitude coordinates to support geosearch queries.
*   **Visibility Controls:** Active centers are visible to users. Admins can disable centers, hiding them from search results.

---

## 12. Reward Domain

The reward domain manages claim requests submitted by eligible users.

*   **Relational Maps:** Many-to-One between `reward_claims` and the primary `users` table.
*   **Vetting Checkpoints:** Reaching milestones sets level progress status to `COMPLETED`, enabling manual claims.

---

## 13. Payment Domain

The payment domain tracks financial disbursement records.

*   **Relational Maps:** One-to-One link between `payment_transactions` and `reward_claims`.
*   **Disbursement Records:** Mark claims as paid only after logging official bank transaction reference numbers.

---

## 14. Notification Domain

The notification domain routes in-app alerts and tracks read/unread states.

*   **Relational Maps:** One-to-Many between `notifications` and `notification_logs`.
*   **Inbox Tracking:** Logs track the read/unread states of user notifications.

---

## 15. Audit Domain

The audit domain stores permanent, system-wide transaction logs.

*   **Ledger Specifications & Permanent Immutability:** The audit logs must be permanent. The database blocks any update and delete operations on `audit_logs`, `notification_logs`, and `payment_audit_logs` tables, enforcing a strict *INSERT-only* immutable registry to prevent fraud.
*   **Log Retention:** Logs are retained for $7\text{ years}$ to meet regulatory audit standards.

---

## 16. Analytics Domain

The analytics domain stores precalculated system metrics to optimize dashboard performance.

*   **Precalculated Snapshots:** An aggregation engine processes database metrics asynchronously during off-peak hours, storing results in `analytics_snapshots` tables.
*   **Reporting Support:** Dashboard charts fetch precalculated snapshots, rendering platform growth trends and waste metrics.

---

## 17. UUID Strategy

*   **UUIDv7 Primary Key Strategy:** Transactional tables must utilize time-ordered **UUIDv7** primary keys (`users`, `teams`, `referral_codes`, `waste_records`, `reward_claims`, `payment_transactions`, `notifications`, `audit_logs`) to optimize index performance, insert speeds, scalability, and chronological sorting support, preventing ID scanning attacks.
*   **Technical Rationale:** Simplifies database scaling and protects user profiles from scan exploitation.
*   **Standard Keys:** Reference tables (like `levels`) use standard integers.

---

## 18. Relationship Design

*   **One-to-One:** Enforces explicit link profiles (e.g., `users` to `user_profiles`).
*   **One-to-Many:** Standard parent-child relations (e.g., `users` to `waste_records`).
*   **Many-to-Many:** Implemented via join tables (e.g., `team_members` linking `teams` and `users`).

---

## 19. Foreign Key Strategy

*   **Relational Controls:** Enforces foreign keys with `ON DELETE RESTRICT` constraints, preventing accidental cascading data deletions.
*   **Standard Key Mapping:** Primary key and foreign key variables must share exact UUID definitions.

---

## 20. Constraint Strategy

*   **Unique Constraints:** Enforced on unique fields (e.g., `username`, `phone_number`, `team_name`).
*   **Check Constraints:** Numeric checks validate bounds (e.g., waste weights locked from $0.1$ to $50.0\text{ KG}$).
*   **Relational Constraints:** Foreign key configurations prevent orphaned entries.

---

## 21. Indexing Strategy

*   **Primary Keys:** Standard B-Tree indexes are created automatically on UUID primary keys.
*   **Search Indexes:** Explicit B-Tree indexes are created on frequently searched columns (e.g., `username`, `phone_number`, `team_code`, `verification_status`).
*   **Reporting Indexes:** Date indexes optimize analytical queries.

---

## 22. Enum Strategy

The platform standardizes status transitions using strict database ENUM datatypes:

```
┌────────────────────────────────────────────────────────┐
│                   System ENUM Sets                     │
├────────────────────────────────────────────────────────┤
│  UserStatus:        [REGISTERED, ACTIVE, SUSPENDED]     │
│  ApplicationStatus: [SUBMITTED, PENDING, APPROVED,      │
│                      REJECTED]                         │
│  ReferralStatus:    [ACTIVE, EXPIRED, DISABLED]        │
│  WasteStatus:       [SUBMITTED, PENDING, APPROVED,      │
│                      REJECTED]                         │
│  ClaimStatus:       [INITIATED, PENDING, APPROVED,      │
│                      REJECTED]                         │
│  PaymentStatus:     [PENDING, PROCESSING, PAID, FAILED]│
└────────────────────────────────────────────────────────┘
```

---

## 23. Soft Delete Strategy

*   **Relational Integrity Rules:** Transactional tables block physical database row deletions to protect audit histories.
*   **Anonymization Protocols:** Profiles marked for deletion undergo anonymization, removing contact details and PII while preserving historical records for audit compliance.

---

## 24. Audit Data Strategy

*   **Asynchronous Database Logging:** System mutations write entries asynchronously to the `audit_logs` table to prevent connection bottlenecks.
*   **Ledger Security Guards:** The database blocks update and delete queries targeting the audit log table, protecting logs from modification.

---

## 25. Data Retention Strategy

*   **User Data:** Retained for $7\text{ years}$ after account closure to meet audit compliance requirements.
*   **Citizen Document scans:** Expire and are archived $1\text{ year}$ after verification validation.
*   **Dashboard Alerts:** Retained for $90\text{ days}$ before automatic cleanup.

---

## 26. Data Security Strategy

*   **PII Encryption & Duplicate Prevention:** Encrypts PII fields at rest using AES-256 algorithms. Storing plain Aadhaar is prohibited. Profiles utilize `aadhaar_encrypted` for display/verification (masked as `XXXX-XXXX-1234`) and cryptographic `aadhaar_hash` for duplicate checks. Bank accounts are treated as highly sensitive data, encrypted at rest, masked as `XXXXXX4589`, restricted strictly, and any accesses trigger entries in `audit_logs`.
*   **Secure Access Controls:** Restricts document uploads to secure MIME-types, verifying that files do not exceed the $5\text{MB}$ limit. Serves files to authorized Admins via temporary, expiring secure URLs.

---

## 27. Backup Strategy

*   **Daily Full Backups:** Automated pg_dump scripts run daily during off-peak hours.
*   **Hourly Incremental Backups:** Hourly write-ahead log (WAL) archiving ensures minimal data loss in case of hardware failures.
*   **Recovery Operations:** Point-in-time recovery validations verify restored database states to ensure data consistency.

---

## 28. Performance Strategy

*   **Analytical Snapshots Strategy:** Dashboard aggregates read from precalculated snapshot tables (`analytics_snapshots`), avoiding heavy real-time query bottlenecks.
*   **Payload Pagination:** Queries returning list rosters use pagination bounds to keep database query loads light.
*   **Performance Requirements:** The database engine, queries, and index strategies are optimized to maintain dashboard load times below **2 seconds**, search lookups below **1 second**, and API responses below **500 ms**. Mandatory pagination is enforced for Users, Teams, Members, Waste Records, Payments, Audit Logs, and Notifications.

---

## 29. Scalability Strategy

*   **Connection Pool Management:** Database connections are managed via PgBouncer, preventing backend processes from exhausting connection pools.
*   **Database Scaling:** Stateless API instances allow developers to scale the backend horizontally behind a load balancer.

---

## 30. Skill India Database Expansion (Phase 2)

*   **Modular Database Migrations:** Adds new course registries, assignments, and certification tables via Alembic.
*   **Relational Compatibility:** Connects new tables to existing `users` without altering core profile fields.

---

## 31. Clean India Database Expansion (Phase 3)

*   **Registry Adaptability:** Phase 1 collection center registries are extended to support regional logistics registries (`clean_india_centers`, `waste_processing`).
*   **Relational Compatibility:** Links transport records and processing logs to existing users and centers without modifying baseline relational keys.

---

## 32. Naming Standards

*   **Tables:** Lowercase snake_case plural naming (e.g., `users`, `waste_records`).
*   **Columns:** Lowercase snake_case singular names (e.g., `user_id`, `created_at`).
*   **Indexes:** Structured prefix formats (e.g., `idx_users_username`).
*   **Constraints:** Structured prefix formats (e.g., `fk_user_profiles_user_id`).

---

## 33. Migration Standards

*   **Alembic Schema migrations:** Schema modifications must use versioned Alembic scripts, keeping databases synchronized.
*   **Rollback Workflows:** Migration scripts must include rollback paths (`down_revision`) to support system recoveries.

---

## 34. Data Integrity Rules

*   **Relational Integrity Rules:** Transactional tables block physical database row deletions to protect audit histories.
*   **Double-Verification Checks:** Waste submissions require geocodes, photo evidence, weight logs, and collection center receipts before approval.

---

## 35. Conclusion

This Database Design Document (`06_DATABASE_DESIGN.md`) provides the absolute logical data architecture, entity relationships, constraints, indexes, enums, soft delete policies, and backup strategies for the Athiyaman Platform – Digital India Phase 1. By detailing users, profiles, teams, waste logs, claim registers, and audit log tables logically, it serves as a complete technical guide for database engineers. All SQL queries, migrations, and database schema updates must adhere strictly to these principles, ensuring the platform remains highly secure, transparent, traceable, and scalable over its lifecycle.
