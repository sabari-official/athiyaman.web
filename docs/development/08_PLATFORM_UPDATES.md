# Athiyaman Platform - Consolidated Review & Requirements Integration Manual
## Phase 1 – Digital India Security, Scalability, and Payment Abstraction Standards

---

## 1. Consolidated Platform Review

This document provides a comprehensive architecture, security, scalability, database, payment, audit, and implementation review for the Athiyaman Platform - Digital India Phase 1. It integrates 11 mandatory platform updates as permanent engineering standards across the system documentation.

### 1.1 Architectural Review
The core architecture is solid, utilizing decoupled layers (Presentation, Controller, Business Service, and Repository). However, to prevent user request blocking during high-volume processes, the system is upgraded to utilize asynchronous, **Queue-Based Processing** for resource-intensive tasks (such as payment processing, notifications delivery, report generation, and document validation). Additionally, the payment subsystem has been upgraded to a provider-agnostic structure using the **Payment Provider Abstraction** pattern.

### 1.2 Security Review
Security holds the highest priority. To prevent data leakage and ensure DPDP Act compliance, strict boundaries are enforced for sensitive Citizen PII. The system is hardened using **Aadhaar Encryption & Hashing**, **Bank Data Encryption**, **Structural File Upload Validations**, and explicit **Security Hardening** (such as rate limiters, secure headers, CORS configurations, and an account lockout policy of 5 failed attempts).

### 1.3 Scalability & Database Review
To support hundreds of thousands of active users and millions of collections without performance degradation, the relational schema is optimized. We integrate a **UUIDv7 Time-Ordered Key Strategy** across all major transactional entities to ensure sequential index insertion speeds. We also deploy the **Team Member Counter Strategy** to replace expensive relational aggregation queries with precalculated counters.

### 1.4 Payments & Claims Review
The reward system is hardened to prevent double-claiming. Under the **Duplicate Claim Prevention** policy, the system locks level progress states and blocks secondary claims while a payout request is pending. Payment modules are decoupled using the **Payment Provider Abstraction** pattern, allowing seamless provider replacements (RazorpayX, Bank Uploads, or future providers) without modifying business logic or relational schemas.

### 1.5 Auditing Review
To maintain absolute accountability and prevent administrative fraud, the platform implements **Audit Immutability**. System logs (`audit_logs`, `notification_logs`, `payment_audit_logs`) are locked to read-only states immediately upon creation, allowing `INSERT` queries while blocking all `UPDATE` or `DELETE` commands.

---

## 2. Integrated Platform Standards

The following standards are mandatory across all development and database deployment phases of the Athiyaman Platform:

```
┌────────────────────────────────────────────────────────┐
│             Team Member Counter Strategy               │
├────────────────────────────────────────────────────────┤
│              UUIDv7 Chronological Identifiers          │
├────────────────────────────────────────────────────────┤
│             Aadhaar Encryption & Hashing               │
├────────────────────────────────────────────────────────┤
│            Encrypted & Masked Bank Data Accounts       │
├────────────────────────────────────────────────────────┤
│             Safe Structure-Audit File Uploads          │
├────────────────────────────────────────────────────────┤
│               Immutable Log Transactions               │
├────────────────────────────────────────────────────────┤
│             Locked Progress Claim Prevention           │
├────────────────────────────────────────────────────────┤
│             Decoupled Payment Service Interfaces       │
├────────────────────────────────────────────────────────┤
│             Asynchronous Queue Task Workers            │
├────────────────────────────────────────────────────────┤
│             Optimized Performance Targets              │
├────────────────────────────────────────────────────────┤
│              Hardened Access Guard lockouts            │
└────────────────────────────────────────────────────────┘
```

1.  **Team Member Counter Strategy:** Maintain `member_count` (INTEGER) in the `teams` table. Increment on joins and decrement on exits. Dashboards must read `member_count` directly, avoiding expensive relational `COUNT` operations.
2.  **UUIDv7 Strategy:** Use time-ordered UUIDv7 keys for primary keys in `users`, `teams`, `referral_codes`, `waste_records`, `reward_claims`, `payment_transactions`, `notifications`, and `audit_logs` to optimize indexing speeds.
3.  **Aadhaar Security:** Aadhaar numbers must never be saved in plain text. Store the encrypted string in `aadhaar_encrypted` and a cryptographic hash in `aadhaar_hash` for duplicate checks. Dashboards must mask displays as `XXXX-XXXX-1234`.
4.  **Bank Data Security:** Encrypt routing fields at rest. Dashboards must mask displays as `XXXXXX4589`. Logging processes must capture access details when bank details are read.
5.  **File Upload Security:** Upload validations must inspect file signatures, check size constraints (max $5\text{MB}$), remove unneeded metadata, rename files, store uploads outside public directories, and enforce authorization checks.
6.  **Audit Immutability:** The database blocks `UPDATE` and `DELETE` queries targeting `audit_logs`, `notification_logs`, and `payment_audit_logs`, keeping records immutable.
7.  **Duplicate Claim Prevention:** Progress states are locked and secondary claims are blocked while a payout claim is pending. Business progress values are logged in separate registries.
8.  **Payment Provider Abstraction:** Decouples payment engines using the Payment Service Interface, allowing provider switches (RazorpayX, Bank Uploads, or future providers) without modifying business logic.
9.  **Queue-Based Processing:** Heavy operations (payments, notifications, analytics aggregates, report generation, document validation) are processed asynchronously via background queue workers.
10. **Performance Requirements:** Enforces targets for dashboard loads ($<2\text{s}$), search queries ($<1\text{s}$), and API responses ($<500\text{ms}$), making pagination mandatory across all list endpoints.
11. **Security Hardening:** Enforces comprehensive security rules: OAuth2 JWT auth, refresh tokens, Argon2 password hashing, rate limiters, input checks, file checks, audit logging, session guards, RBAC, secure headers, CORS configuration, and an account lockout policy of 5 failed attempts.

---

## 3. Revised Sections: 04_ARCHITECTURE.md

### 3.1 Revision 1: System Technologies Updates
*   **Location:** Insert in **Section 3: Technology Architecture**, after the existing *Hosting* entry.
*   **Revised Standard Block:**
    > [!IMPORTANT]
    > **PAYMENT & ASYNC QUEUE ABSTRACTION:**
    > *   **Payment Provider Abstraction:** Decouples payment engines using the Payment Service Interface, allowing provider switches (RazorpayX, Bank Uploads, or future providers) without modifying business logic.
    > *   **Queue-Based Processing:** Heavy operations (payments, notifications, analytics aggregates, report generation, document validation) are processed asynchronously via background queue workers.

### 3.2 Revision 2: UUIDv7 & Security Architecture Standardizations
*   **Location:** Replace details in **Section 30: Security Architecture**.
*   **Revised Standard Block:**
    ```markdown
    ### 30.1 Dynamic Identity Security (UUIDv7 & PII Encryption)
    *   **UUIDv7 Primary Keys:** Major transactional tables (`users`, `teams`, `referral_codes`, `waste_records`, `reward_claims`, `payment_transactions`, `notifications`, `audit_logs`) must use UUIDv7 keys to optimize indexing speeds.
    *   **Encrypted Aadhaar Storage:** Aadhaar details must be encrypted using AES-256 algorithms (`aadhaar_encrypted`), saving a unique cryptographic hash in `aadhaar_hash` for duplicate checks. Dashboards must mask displays as `XXXX-XXXX-1234`.
    *   **Encrypted Bank Routing:** Bank accounts are encrypted at rest and masked as `XXXXXX4589` on user interfaces. Access details are logged in the audit trail.
    
    ### 30.2 Structural File Upload Validations
    *   **MIME Signature Inspections:** Upload engines must inspect file signatures, check size constraints (max $5\text{MB}$), remove unneeded metadata, rename files, store uploads outside public directories, and enforce authorization checks.
    ```

### 3.3 Revision 3: Security Hardening & Lockout Policies
*   **Location:** Insert in **Section 30: Security Architecture**, at the end of the section.
*   **Revised Standard Block:**
    > [!CAUTION]
    > **ACCOUNT LOCKOUT & HARDENING STANDARDS:**
    > The backend must enforce a strict account lockout policy, disabling accounts for $15\text{ minutes}$ after $5\text{ failed login attempts}$ to prevent brute-force attacks. Secure headers, strict CORS rules, and rate limiters are mandatory.

---

## 4. Revised Sections: 05_IMPLEMENTATION.md

### 4.1 Revision 1: Project Setup & Variables Configuration
*   **Location:** Insert in **Section 10: Configuration Management**, after the existing *Logging Configuration* variables.
*   **Revised Standard Block:**
    ```ini
    # Payment Provider Configuration
    PAYMENT_PROVIDER=RAZORPAYX # Options: RAZORPAYX | BANK_UPLOAD | FUTURE_PROVIDER
    
    # Asynchronous Queue Configuration
    REDIS_QUEUE_URL=redis://localhost:6379/1
    QUEUE_WORKERS_COUNT=4
    ```

### 4.2 Revision 2: File Upload Security Validations
*   **Location:** Replace details in **Section 19: File Storage Standards**.
*   **Revised Standard Block:**
    ```markdown
    ### 19.1 Secure File Upload Implementation
    1. **MIME Verification:** Read file bytes to verify signatures, rejecting forbidden extensions (EXE, BAT, JS, SH, DLL).
    2. **Metadata Strip:** Process images to strip EXIF and location metadata before storage.
    3. **File Renaming:** Save files using UUIDv7 strings to prevent path traversal exploits.
    4. **Access Isolation:** Store files outside public directories, serving uploads to authorized users via temporary, expiring secure URLs.
    ```

### 4.3 Revision 3: Account Lockout Controls
*   **Location:** Insert in **Section 15: Security Implementation Standards**, after the *Rate Limiting* rules.
*   **Revised Standard Block:**
    > [!WARNING]
    > **LOCKOUT CONTROL IMPLEMENTATION:**
    > Track failed login attempts using Redis keys. Reaching 5 failed attempts locks the account, logs a high-priority alert, and requires an Admin reactivation or a $15\text{-minute}$ cooldown.

---

## 5. Revised Sections: 06_DATABASE_DESIGN.md

### 5.1 Revision 1: Team Member Counter Strategy
*   **Location:** Insert in **Section 7: Team Domain**, at the beginning of the section.
*   **Revised Standard Block:**
    ```markdown
    ### 7.1 Precalculated Member Counters
    *   **Table Variable:** Add `member_count` (INTEGER, DEFAULT 0) to the `teams` table.
    *   **Operational Rules:**
        *   Increment `member_count` automatically when a member joins.
        *   Decrement `member_count` when a member leaves.
        *   User and admin dashboards must read `member_count` directly, avoiding expensive relational `COUNT` operations.
    ```

### 5.2 Revision 2: UUIDv7 Relational Strategy
*   **Location:** Replace details in **Section 17: UUID Strategy**.
*   **Revised Standard Block:**
    ```markdown
    ### 17.1 UUIDv7 Time-Ordered Strategy
    *   **Strategy Standard:** Major transactional tables (`users`, `teams`, `referral_codes`, `waste_records`, `reward_claims`, `payment_transactions`, `notifications`, `audit_logs`) must use UUIDv7 keys.
    *   **System Benefits:** Ensures sequential index insertion, improves write performance, and supports chronological sorting natively.
    ```

### 5.3 Revision 3: PII Security & Encryption Columns
*   **Location:** Replace details in **Section 26: Data Security Strategy**.
*   **Revised Standard Block:**
    ```markdown
    ### 26.1 Encrypted Identity Columns
    *   **Aadhaar Columns:** Replace the plain text Aadhaar column in `user_profiles` with:
        *   `aadhaar_encrypted` (VARCHAR): Encrypted string used for display and verification.
        *   `aadhaar_hash` (VARCHAR): Cryptographic hash used for duplicate detection.
    *   **Banking Columns:** Replace the account number column with:
        *   `bank_account_encrypted` (VARCHAR): Encrypted account number string.
    *   **Masking Rules:** Mask displays as `XXXX-XXXX-1234` for Aadhaar and `XXXXXX4589` for bank accounts.
    ```

### 5.4 Revision 4: Immutable Audit Trail Tables
*   **Location:** Replace details in **Section 24: Audit Data Strategy**.
*   **Revised Standard Block:**
    ```markdown
    ### 24.1 Immutable Log Registries
    *   **Standard Rule:** The database blocks `UPDATE` and `DELETE` queries targeting `audit_logs`, `notification_logs`, and `payment_audit_logs`.
    *   **Enforcement:** Implemented via database trigger mechanisms, locking logs to read-only states immediately upon creation.
    ```

---

## 6. Revised Sections: 07_API_SPECIFICATION.md

### 6.1 Revision 1: File Upload Validations
*   **Location:** Insert in **Section 15: Document APIs**, under the *Upload Document* validations.
*   **Revised Standard Block:**
    > [!IMPORTANT]
    > **UPLOAD VALIDATION CRITERIA:**
    > API endpoints must check file headers and inspect magic bytes, rejecting forbidden extensions (EXE, BAT, JS, SH, DLL). Uploaded files are renamed using UUIDv7 strings.

### 6.2 Revision 2: Duplicate Claim Prevention Workflows
*   **Location:** Replace details in **Section 12: Reward Claim APIs**.
*   **Revised Standard Block:**
    ```markdown
    ### 12.1 Claim Vetting Rules
    *   **Validation Checkpoints:**
        *   The claims engine validates that the user's profile is complete, documents are verified, and no other active claims exist for the same level.
        *   No second claim is allowed while a payout request is pending.
        *   Level progression is locked during claim reviews; progress from new activities is saved in a separate progress registry.
    ```

### 6.3 Revision 3: Payment Abstraction Endpoints
*   **Location:** Replace details in **Section 13: Payment APIs**.
*   **Revised Standard Block:**
    ```markdown
    ### 13.1 Decoupled Payment Integrations
    *   **Integration Strategy:** API endpoints route payments through abstract Payment Service interfaces. Adapters manage processing for RazorpayX or bank transfer ledger sheets without altering backend business workflows.
    ```

### 6.4 Revision 4: API Pagination Standards
*   **Location:** Replace details in **Section 32: API Pagination Standards**.
*   **Revised Standard Block:**
    ```markdown
    ### 32.1 Mandatory Pagination Standard
    *   **Pagination Filters:** Queries returning list rosters (`users`, `teams`, `members`, `waste_records`, `payments`, `audit_logs`, `notifications`) must enforce standard parameters (`page`, `limit`) to optimize database query speeds.
    ```

---

## 7. Conclusion

This Consolidated Review & Requirements Integration Manual (`08_PLATFORM_UPDATES.md`) establishes the absolute technical, security, and scalability standards for the Athiyaman Platform – Digital India Phase 1. By detailing precalculated member counters, UUIDv7 keys, Aadhaar/banking encryption, secure file handling, immutable audit trails, duplicate claim prevention, payment provider abstractions, and asynchronous background queues, it serves as a complete technical guide for engineering teams. All software builds, database migrations, and operational workflows must adhere strictly to these integrated principles, ensuring the platform remains highly secure, transparent, traceable, and scalable over its lifecycle.
