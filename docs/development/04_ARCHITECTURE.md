# Athiyaman Platform - Technical Architecture Document
## Phase 1 – Digital India Enterprise System Design Blueprint

---

## 1. Architecture Overview

This document defines the technical architecture of the Athiyaman Platform - Digital India Phase 1. It details the design patterns, system layers, folder layouts, and security matrices required to construct a highly reliable, modular, and performant web platform.

*   **System Architecture Vision:** To establish a stateless, highly auditable, feature-modularized software layout utilizing decoupled layers (Presentation, Controller, Business Service, and Repository layers) to ensure rapid developer cycles and frictionless horizontal expansion.
*   **Technical Goals:**
    *   *Ultra-low Latency:* Maintain sub-$200\text{ms}$ API server response limits.
    *   *High availability:* Target $99.9\%$ system availability.
    *   *Zero Security Vulnerabilities:* Native protection against OWASP Top 10 exploits.
*   **Architecture Principles:** Decoupling, strict static typing, explicit validation boundaries, clean dependency injections, and data access isolation.
*   **Scalability Goals:** Relational optimizations supporting $500,000$ active users, $10\text{ million}$ audit entries, and concurrent requests.
*   **Security Goals:** Robust OAuth2 JWT session guards, Argon2 hashing, AES-256 rest-encryption of PII, and sanitization parameters.
*   **Maintainability Goals:** Clean Architecture layer rules, Repository Pattern boundaries, and feature modular folder structures.
*   **Future Expansion Goals:** Support seamless integration of Phase 2 (Skill India) and Phase 3 (Clean India) by isolating module domain layers.

---

## 2. Architectural Principles

To guarantee modularity, stability, and maintainability, the platform enforces nine core design principles:

```
┌────────────────────────────────────────────────────────┐
│                  Separation of Concerns                │
├────────────────────────────────────────────────────────┤
│                 Single Responsibility                  │
├────────────────────────────────────────────────────────┤
│                 Feature Modularity                     │
├────────────────────────────────────────────────────────┤
│                    Loose Coupling                      │
├────────────────────────────────────────────────────────┤
│                    High Cohesion                       │
├────────────────────────────────────────────────────────┤
│                 Asynchronous Auditing                  │
├────────────────────────────────────────────────────────┤
│                    Security First                      │
├────────────────────────────────────────────────────────┤
│                   Scalability First                    │
├────────────────────────────────────────────────────────┤
│                 Maintainability First                  │
└────────────────────────────────────────────────────────┘
```

*   **Separation of Concerns (SoC):** Distinct technical duties live in dedicated code layers. UI renders grids, controllers route parameters, services process business logic, and repositories persist data records.
*   **Single Responsibility Principle (SRP):** Each class, function, or hook has exactly one reason to change, preventing large monolithic files.
*   **Feature Modularity:** The codebase is organized by business feature areas rather than generic layer directories. All code relating to a feature (e.g., Waste) is self-contained.
*   **Loose Coupling:** Code components interact via abstract schemas and interfaces rather than tight class instances, allowing easy modifications.
*   **High Cohesion:** Logic, models, and validations within a module are closely related and self-contained.
*   **Asynchronous Auditing:** Mutations to critical records trigger non-blocking, asynchronous logs to avoid request bottlenecks.
*   **Security First:** Validations and route guards are enforced at the server-side API layer, treating the client as untrusted.
*   **Scalability First:** Relational tables use UUIDs and database indexing to optimize high-traffic queries.
*   **Maintainability First:** Strictly enforces strict typing and linting configurations to ensure long-term code health.

---

## 3. Technology Architecture

The technology decisions support portable, direct-hosting compatibility.

### 3.1 Frontend Tech-Stack

*   **React (v18+):** Leveraged as our SPA component library. Chosen for its performance, Virtual DOM rendering efficiency, and rich component ecosystem.
*   **TypeScript:** Enforces strict static typing, eliminating type mismatch errors during development.
*   **Tailwind CSS:** Utility-first CSS engine. Provides rapid responsive styling and compiles into a tiny, high-contrast visual footprint.
*   **React Router (v6+):** Client-side router. Handles nested layout routes, protecting administrative routes natively.
*   **React Query (TanStack):** Handles server-state caching, background queries, error states, and mutations.

### 3.2 Backend Tech-Stack

*   **Python (v3.11+):** Leveraged for its secure syntax, reading simplicity, and performance.
*   **FastAPI:** Asynchronous framework built on ASGI. Provides high performance, automatic Swagger docs, and Pydantic validation.
*   **SQLAlchemy ORM:** Python's enterprise ORM. Combines relational design with object modeling to prevent SQL injections.
*   **Alembic:** Database migration manager for SQLAlchemy. Tracks schema version adjustments in version-controlled script files.
*   **Pydantic:** Strictly validates incoming requests and outgoing payloads using Python types.

### 3.3 Database & Hosting Infrastructure

*   **PostgreSQL:** Relational database chosen for ACID compliance and support for precalculating analytical snapshots.
*   **JWT (JSON Web Tokens):** Stateless authentication standard carrying active scopes and role parameters.
*   **Local File Storage:** Low-cost storage utilizing abstract adapters to support simple migrations to S3.
*   **Google Maps API:** Geocodes and maps active regional collection centers for search lookups.
*   **In-App Alerts:** Dashboard inbox alerts, coupled with mock adapters for SMS and WhatsApp.
*   **Linux / DirectAdmin:** Designed to support cost-effective deployment matching local host environments.

---

## 4. System Architecture

The platform uses a decoupled, four-tier architecture model to isolate concerns and protect backend logic:

```
[ USERS ] <───(HTTPS / JSON)───> [ PRESENTATION TIER ] <───(API Gateway)───> [ APPLICATION SERVICES ] <───(SQLAlchemy)───> [ DATABASE TIER ]
```

### 4.1 Presentation Tier (React Frontend)
Renders forms, displays trees, and manages visual states. Accesses API networks using client gateways, caching states locally via React Query to reduce load.

### 4.2 Gateway & Controller Tier (FastAPI Backend)
Intercepts incoming HTTPS calls, validates payloads against Pydantic schemas, logs access attempts, and checks JWT permissions before routing requests to the service layer.

### 4.3 Application Service Tier (Business Workflows)
Contains pure business logic, such as validation checks, level calculation formulas, geocoordinate updates, and reward parameters. This layer is completely isolated from HTTP details or raw SQL operations.

### 4.4 Persistence Tier (Repository & Database)
Executes relational database queries via SQLAlchemy ORM. Keeps data operations isolated from business rules, managing transactions to ensure database consistency.

---

## 5. High-Level Architecture Diagram

```
                                  [ CITIZENS / ADMINS ]
                                            │
                                            ▼ (HTTPS / JSON)
                            ┌───────────────────────────────┐
                            │    Vercel Static Frontend     │
                            │  (React / TS / Tailwind CSS)  │
                            └───────────────┬───────────────┘
                                            │
                                            ▼ (Protected API Gateway)
                            ┌───────────────────────────────┐
                            │     FastAPI Core Backend      │
                            │   (WSGI / ASGI Docker Container)│
                            └───────┬───────────────┬───────┘
                                    │               │
            ┌───────────────────────┘               └───────────────────────┐
            ▼ (SQLAlchemy)                                                  ▼ (Expiring URL Files)
 ┌─────────────────────────────┐                                     ┌─────────────────────────────┐
 │    PostgreSQL Database      │                                     │     Local File Storage      │
 │  (ACID Relational Engine)   │                                     │  (Direct Directory/S3 Path) │
 └──────────┬──────────────────┘                                     └─────────────────────────────┘
            │
            ▼ (Asynchronous)
 ┌─────────────────────────────┐
 │       Analytics Engine      │
 │ (Precomputed Snapshots Pool)│
 └──────────┬──────────────────┘
            │
            ▼ (Asynchronous)
 ┌─────────────────────────────┐
 │     Audit Log Service       │
 │   (Immutable Audit Table)   │
 └─────────────────────────────┘
```

---

## 6. Frontend Architecture

The React Single Page Application focuses on decoupling UI layout components from state caching logic.

*   **React Architecture:** Component logic is modularized. Page templates define structural layouts, features handle business domains, and presentation elements render visual details.
*   **State Management:**
    *   *Server State:* Synchronized via **React Query**, which handles data queries, caching, background updates, and mutations.
    *   *UI State:* Handled using React's native `useState` and `useContext` hooks, keeping the runtime clean and performance overhead low.
*   **Routing System:** Configured via **React Router**. Uses protected route panels to check user authorization states, redirecting unauthorized traffic to the login screen.
*   **API Network Layer:** Utilizes **Axios** clients configured with interceptor functions. These functions inject authorization header tokens automatically and catch expired token errors to prompt logins.
*   **Error Boundaries:** Wraps interface elements inside react-error-boundary controllers to catch unexpected rendering failures and display user-friendly fallback screens.
*   **Performance Configurations:** Utilizes code-splitting and dynamic route loading to keep initial asset bundles small and fast-loading.

---

## 7. Frontend Folder Structure

The frontend application uses a clean, standardized workspace structure:

```
src/
├── assets/             # Static visual media (branding, logos, SVGs)
├── components/         # Shared presentation elements (buttons, inputs)
├── contexts/           # Global context providers (User sessions, styles)
├── features/           # Modular business feature directories
│   ├── auth/           # Login, OTP validation, and password forms
│   ├── teams/          # Team registration, profiles, and member rosters
│   └── waste/          # Waste log forms, collections tables, and maps
├── hooks/              # Global custom hooks (useDebounce, useMediaQuery)
├── layouts/            # Page shell containers (Header menus, sidebars)
├── pages/              # Unprotected info displays (Home, About, Initiatives)
├── services/           # Network API adapters
├── types/              # Unified TypeScript definitions (.ts files)
└── utils/              # Functional helper utilities (IFSC checking, dates)
```

---

## 8. Backend Architecture

The FastAPI backend uses an asynchronous design to ensure fast response speeds and low resource usage.

*   **FastAPI Execution Router:** Decouples endpoint routing from service logic. Routers define path targets, validate request schemas, check JWT permissions, and return typed JSON payloads.
*   **Payload Validation Lifecycle:** Input data undergoes validation checks in a strict sequence:
    $$\text{Payload Arrival} \rightarrow \text{Pydantic Type Check} \rightarrow \text{Endpoint Router Guards} \rightarrow \text{Service Logic Checks}$$
*   **Service Layer Isolations:** Service classes manage validation checks, geocoordinate updates, level milestones, and reward calculations, keeping logic decoupled from the web framework.
*   **Repository Isolation Boundaries:** Database interactions are managed exclusively by Repositories via SQLAlchemy, keeping SQL queries separate from business rules.
*   **Middleware Pipeline:**
    *   *CORS Middleware:* Restricts origin endpoints to secure hosts.
    *   *Exceptions Middleware:* Intercepts application failures, logs errors, and returns user-friendly JSON payloads to the frontend.
    *   *Audit Log Middleware:* Captures audit trails asynchronously, logging security events without locking threads.

---

## 9. Backend Folder Structure

The FastAPI application uses a modular, feature-based folder layout:

```
app/
├── api/                # API router entry hubs mapping to module endpoints
├── core/               # Central configurations (JWT, database connections)
├── database/           # ORM session managers and migration scripts
├── middleware/         # System pipelines (CORS, error handlers, audit trails)
├── modules/            # Feature directories (router, schema, model, service)
│   ├── auth/           # Login services, OTP actions, and password hashes
│   ├── teams/          # Team managers, rosters, and validation checks
│   └── waste/          # Waste logs, center registers, geocodes, and maps
├── utils/              # Helper utilities (Aadhaar checking, geolocation, phone)
└── main.py             # Application entry point configuring middleware and routes
```

---

## 10. Feature Modularization

The application decouples systems into 14 distinct feature modules to isolate domains and simplify future scaling.

```
┌────────────────────────────────────────────────────────┐
│                        Developer                       │
├────────────────────────────────────────────────────────┤
│                          Admin                         │
├────────────────────────────────────────────────────────┤
│                          Audit                         │
├────────────────────────────────────────────────────────┤
│                        Analytics                       │
├───────────────────────────┬────────────────────────────┘
                            ▼
┌────────────────────────────────────────────────────────┐
│  Auth ──► Profiles ──► Teams ──► Referrals ──► Levels  │
├────────────────────────────────────────────────────────┤
│    Waste ──► Collection Centers ──► Claims ──► Payments│
└────────────────────────────────────────────────────────┘
```

*   **auth:** Manages JWT validation, OTP challenges, registration workflows, and logins.
*   **profiles:** Manages biography records, nominee entries, and bank accounts.
*   **teams:** Enforces unique team names and maps regional district borders.
*   **referrals:** Generates, validates, and manages `LEADER_REFERRAL` and `TEAM_REFERRAL` codes.
*   **levels:** Standardizes rules and milestone thresholds for Levels 1–11.
*   **waste:** Manages waste submissions, audits, photo evidence, and weight logs.
*   **collection_centers:** Lists authorized centers geocoded by latitude/longitude.
*   **claims:** Tracks reward claim states, amounts, and level milestones.
*   **payments:** Manages manual payment execution details and bank references.
*   **notifications:** Routes in-app alerts and maps unread/read states.
*   **audit:** Captures and stores audit logs for all mutating database events.
*   **analytics:** Asynchronously aggregates system performance and growth trends.
*   **admin:** Provides dashboard queues for vetting applications and approvals.
*   **developer:** Tracks system health, runs backups, and manages feature flags.

---

## 11. Clean Architecture Design

The backend separates code into four distinct layers, managing dependencies strictly from outer presentation layers to inner domain layers.

*   **Presentation Layer (Routers & Schema DTOs):** Defines HTTP paths, parameters, response codes, and serialization models.
*   **Application Layer (Services & Logic Core):** Coordinates business workflows (such as level updates and claims checking) across multiple repositories.
*   **Domain Layer (Entity Definitions & Rules):** Standardizes system data shapes, mapping database constraints and relational entities directly.
*   **Infrastructure Layer (Repositories & Adapters):** Integrates external systems, managing local files, database connections, and notification adapters.
*   **Strict Dependency Flow:** Outer layers can depend on inner layers, but inner layers must remain completely independent of outer details (e.g., domain entities cannot depend on HTTP schemas).

---

## 12. Repository Pattern

*   **Decoupled Relational Persistence:** All database queries are isolated inside Repositories using SQLAlchemy ORM. Business services never write raw SQL queries or manage database session lifetimes directly.
*   **Session Management Strategy:** Uses FastAPI dependencies to inject scoped database sessions per request, ensuring clean rollbacks if transactions fail.
*   **Technical Rationale:** Simplifies testing by allowing developers to mock database calls easily, and ensures smooth database migrations in the future.

---

## 13. Service Layer Pattern

*   **Decoupled Workflows:** The business rules and validations of the Athiyaman platform live exclusively in Service classes (e.g., `LevelService`, `ClaimService`), separating logic from API routers.
*   **State Validations:** Enforces platform constraints (such as One Leader One Team and linear level progression) and calculates milestones before database writes.
*   **Clean Framework Transitions:** Ensures that changes to framework adapters (such as migrating from FastAPI to another library) do not require rewrites of our business logic.

---

## 14. Dependency Injection (DI) Strategy

The backend leverages FastAPI's injection system to manage service and repository lifetimes cleanly.

```
┌────────────────────────────────────────────────────────┐
│                  FastAPI Request Endpoint              │
├────────────────────────────────────────────────────────┤
│  Depends(get_db) ──► Injects Scoped DB Session         │
│  Depends(get_current_user) ──► Validates JWT & User    │
│  Depends(get_team_service) ──► Resolves Team Workspace │
└────────────────────────────────────────────────────────┘
```

*   **Asynchronous Database Injectors:** Endpoint routes request scoped database sessions using a `Depends(get_db)` injector, managing connection pools automatically.
*   **Modular Component Resolution:** Servicing libraries are resolved dynamically using injection structures, resolving dependent classes recursively.
*   **Simplified Mock Testing:** Enables developers to swap real database repositories with mock implementations in test suits, speeding up test runs.

---

## 15. Authentication Architecture

*   **Dual JWT Token Management:**
    *   *Access Token:* Short-lived token ($15\text{ minutes}$) containing identity details and role scopes, stored in local memory.
    *   *Refresh Token:* Secure token ($7\text{ days}$) stored in an HTTP-only, secure, `SameSite=Strict` cookie to prevent theft.
*   **Token Refresh Workflows:** Standard APIs accept JWT access headers. When an access token expires, the client uses the HTTP-only refresh cookie to request a new access token, preventing session interruptions.
*   **Registration Workflows:** Requires verifying the user's mobile number via a $6$-digit OTP, validating registration referral codes before enabling profiles.
*   **Secure Logouts:** Triggers server-side session cleanup, invalidates the HTTP-only refresh cookie, and logs the session end in the audit trail.

---

## 16. Authorization Architecture (RBAC)

The platform implements Role-Based Access Control (RBAC) to enforce security boundaries across all endpoints:

```
┌────────────────────────────────────────────────────────┐
│             Endpoint Route Permission Guards           │
├────────────────────────────────────────────────────────┤
│  Member Endpoints:  [MEMBER, LEADER, ADMIN, DEVELOPER]  │
│  Leader Endpoints:  [LEADER, ADMIN, DEVELOPER]          │
│  Admin Endpoints:   [ADMIN, DEVELOPER]                  │
│  Dev Endpoints:     [DEVELOPER]                         │
└────────────────────────────────────────────────────────┘
```

*   **Role Boundaries:** Endpoints check the user's active role dynamically using JWT payloads:
    *   `MEMBER` $\rightarrow$ Profile and waste logging features.
    *   `LEADER` $\rightarrow$ Team recruitment and leader claim tools.
    *   `ADMIN` $\rightarrow$ System queues, verifications, and approvals.
    *   `DEVELOPER` $\rightarrow$ Diagnostics, logs, backups, and feature flags.
*   **Gateway Permission Verification:** Middleware checks role authorizations at the gateway level, returning `403 Forbidden` responses immediately if access is unauthorized.

---

## 17. User Management Architecture

*   **Unified Roster Registers:** Manages baseline user data records, verifying identity details and tracking dashboard access.
*   **User Lifecycle Lifecycle:**
    ```
    [REGISTERED] -> [ACTIVE] <-> [SUSPENDED]
    ```
*   **Administrative Operations:** Allows Admins to toggle user statuses, suspend accounts flagged for fraud, and trigger password resets.
*   **Auditing Integrations:** Logs all account updates, status toggles, and resets, capturing the admin ID and IP.

---

## 18. Profile Architecture

*   **Secure Biographical Storage & Encryption:** Encrypts sensitive citizen PII at rest using AES-256 algorithms. 
    *   **Aadhaar Security standards:** The platform strictly prohibits storing plain text Aadhaar numbers. Profiles must contain:
        *   `aadhaar_encrypted`: Encrypted Aadhaar string used strictly for display and verification reviews.
        *   `aadhaar_hash`: Cryptographic one-way hash of Aadhaar used exclusively for duplicate leader application/account detection.
        *   Aadhaar display must be masked as `XXXX-XXXX-1234` in all interfaces.
    *   **Bank Account Security standards:** Bank account details are treated as highly sensitive data. Information must be encrypted at rest, masked as `XXXXXX4589` in displays, restricted strictly to authorized administrative workflows, and any access attempts must trigger an immediate high-priority entry in `audit_logs`.
*   **File Upload Validation:** Validates scans against MIME types, limits file size (max $5\text{MB}$), and saves files under UUID-masked paths to prevent path traversal attacks.
*   **Profile Completion Scoring:** Tracks and updates profile completeness scores dynamically as sections are completed.

---

## 19. Team Architecture

*   **Unique Team Registries:** Enforces globally unique team names and logs unique team codes linked to the leader's ID.
*   **Membership Association:** Connects members to the team owned by the leader whose referral code was used during registration.
*   **Team Member Counter Strategy:** To support teams containing thousands or tens of thousands of members, the database schema must maintain a pre-calculated `member_count` in the `teams` table. The counter increments immediately when a member joins and decrements when a member leaves. All dashboard queries read `member_count` directly, strictly prohibiting expensive SQL `COUNT` queries on `team_members` to reduce database load.
*   **Lifecycle Management:** Enables Admins to monitor team status, manage rosters, and suspend teams flagged for systemic collection issues.

---

## 20. Referral Architecture

*   **Vetted Code Generation:** Generates single-use `LEADER_REFERRAL` codes with $48$-hour expirations, and multi-use `TEAM_REFERRAL` codes managed by active Leaders.
*   **Validation Checkpoints:** Registration endpoints verify that codes exist, are active, have usage capacity, and are not expired.
*   **Auditing Integrations:** Logs all referral activities in the database audit trail to maintain complete accountability.

---

## 21. Level Engine Architecture

*   **Sequential Progression Verification:** The level engine validates milestone criteria, preventing users from skipping levels:
    *   *Team Levels (1–6):* Incremented by Leaders based on verified team size.
    *   *Personal Levels (7–11):* Incremented individually by all users based on approved waste weights.
*   **Automated Progress Tracking:** Updates progress weights dynamically upon waste record approval, completing levels automatically when thresholds are reached.
*   **Reward Claim Workflows:** Reaching milestones sets level progress status to `COMPLETED` and enables the payout claim button.

---

## 22. Waste Management Architecture

*   **Submission Vetting:** Validates weight logs ($0.1$ to $50.0\text{ KG}$), registers geocodes, and accepts photo proof uploads.
*   **Verification Timeline:** Submissions route to the Admin Verification Queue. Admins manually review photos and receipts to verify record accuracy.
*   **Relational Database Mapping:** Approved weights update the user's level progress balance. Every status transition is logged in the `waste_status_history` ledger.

---

## 23. Collection Center Architecture

*   **Registry Maintenance:** Lists authorized locations geocoded by latitude/longitude.
*   **Geosearch Integrations:** Translates user pincode queries into nearest sorted geocoordinate center lists.
*   **Visibility Flags:** Active center registries are visible to users. Admins can disable centers for maintenance, hiding them from search results.

---

## 24. Reward Architecture

*   **Milestone Checkpoints:** Integrates with the level engine, verifying level status parameters before enabling payout claims.
*   **Manual Claim Workflows:** Reaching milestones enables the claim button. Users submit claims manually to verify their bank details before payouts are processed.
*   **Duplicate Claim Prevention standards:** The claims engine strictly blocks duplicate payout requests. The workflow follows:
    $$\text{Level Completed} \rightarrow \text{Claim Created} \rightarrow \text{Claim Pending} \rightarrow \text{Admin Review} \rightarrow \text{Approved or Rejected}$$
    *   No second claim is permitted for any level milestone.
    *   No second claim can be created while a claim is in `PENDING` state.
    *   Progress is locked during claim review; new progress accumulated is separate and stored in future level buckets, preventing double-claiming.
*   ** Vetting Actions:** Admins manually verify document scans and profile logs before approving claims.

---

## 25. Payment Architecture

*   **Transaction Queue Management:** Approved claims are assigned a `PENDING_PAYMENT` status, routing them to the Payment Queue.
*   **Manual Banking Disbursals:** Admins execute bank transfers externally, inputting unique bank transaction reference codes to confirm payouts.
*   **Payment Provider Abstraction Layer:** The payment module must not directly depend on RazorpayX or any single vendor. It utilizes an abstract Payment Service Interface mapping to modular Provider Adapters (supporting RazorpayX, Bank Upload, and future aggregators). This enables swapping payment providers without changing business logic, database schemas, or reward workflows.
*   **Failure Recovery Workflows:** Failed transfers return claims to the Payment Queue, lock payouts temporarily, and prompt the user to correct their banking details.

---

## 26. Notification Architecture

*   **Asynchronous Notification Dispatch:** The notification engine routes alerts asynchronously to prevent application bottlenecks.
*   **Multi-channel Adapters:** Employs dynamic system interfaces, sending dashboard updates natively and routing SMS/WhatsApp notifications via mock adapters.
*   **Dashboard Alerts:** Lists system updates in user notifications boxes, tracking unread and read states dynamically.

---

## 27. Analytics Architecture

*   **Asynchronous Analytics Processing:** The analytics engine processes database metrics asynchronously during off-peak hours, preventing real-time query bottlenecks.
*   **Precalculated Snapshots:** Stores precalculated metrics in `analytics_snapshots` tables.
*   **Dashboard Renderings:** Dashboard charts fetch precalculated snapshots, rendering platform growth trends, waste collection volumes, and financial payout metrics.

---

## 28. Audit Architecture

*   **Immutable Logs Registry:** Database queries write mutating actions asynchronously to the read-only `audit_logs` table.
*   **Complete Log Footprints:** Captured logs record the user ID, role, action, target entity, IP address, device footprint, and timestamp.
*   **Ledger Security Guards & Permanent Immutability:** Audit records are strictly immutable after creation. The database engine enforces a strict *INSERT-only* policy, returning access errors for any `UPDATE` or `DELETE` operations targeting `audit_logs`, `notification_logs`, and `payment_audit_logs`. This ensures complete fraud prevention, compliance support, and comprehensive investigation logs.
*   **Compliance Compliance:** Logs are retained for $7\text{ years}$ to meet regulatory audit and security compliance standards.

---

## 29. Developer Monitoring Architecture

*   **Diagnostics Monitoring:** Displays real-time diagnostics, including server CPU load, memory utilization, and active database connection pool stats.
*   **Vulnerability Detections:** Security logs capture and alert developers to failed logins, IP blocks, and unauthorized route access events.
*   **Crash Integrations:** Code exceptions and system errors are sent to the Developer Portal via Sentry for diagnosis.

---

## 30. Security Architecture

*   **Zero-Trust API Guards:** All non-public APIs require valid JWT tokens. Routers check permissions at the gateway level.
*   **Secure Hashing Protocols:** Passwords must be hashed using high-computation **Argon2id** algorithms, preventing brute-force compromises.
*   **Rate Limiting Prevention:** Caps request volumes (e.g., standard endpoints capped at $60\text{ requests/minute}$) to prevent denial-of-service threats.
*   **File Upload Protections:** Document uploads are restricted to secure MIME-types, verified for size (max $5\text{MB}$), and saved under UUID-masked paths to prevent path traversal attacks.

---

## 31. File Storage Architecture

*   **Isolated Storage Layout:** Files are stored in secure directories outside the public web server, organized by upload categories.
*   **Upload Validation:** Restricts uploads to secure image and document types (JPEG, PNG, PDF), verifying that files do not exceed the $5\text{MB}$ limit.
*   **Access Control:** Files are served to authorized Admins via temporary, expiring secure URLs.
*   **Data Erasure Protocols:** Profiles marked for deletion undergo anonymization, removing contact details while preserving historical records for audit compliance.

---

## 32. API Architecture

*   **REST Principles:** Follows strict RESTful design patterns. Uses standard HTTP methods: `GET` (fetch data), `POST` (create), `PUT` (update), and `DELETE` (delete).
*   **API Versioning Strategy:** Includes explicit version prefixes in API endpoints (e.g., `/api/v1/*`) to support future upgrades without breaking active integrations.
*   **JSON Payloads Standard:** Standardizes communications using JSON format, validating payloads using Pydantic schemas.
*   **API Error Payload Layout:**
    ```json
    {
      "detail": {
        "code": "INVALID_REFERRAL_CODE",
        "message": "The referral code entered is either expired or at maximum capacity."
      }
    }
    ```
*   ** Roster Pagination Rules:** Queries returning list rosters use standard parameter structures (`?page=1&limit=20`) to keep database query loads light.

---

## 33. Database Architecture Strategy

*   **Relational PostgreSQL Strategy:** Enforces time-ordered **UUIDv7** primary keys for all major entities (including `users`, `teams`, `referral_codes`, `waste_records`, `reward_claims`, `payment_transactions`, `notifications`, and `audit_logs`). UUIDv7 guarantees time-ordered identifiers, yielding significantly improved indexing and insert performance, chronological sorting support, and robust scalability, while preventing ID scanning attacks. Enforces foreign key constraints across all relationships to prevent orphaned records.
*   **Database Indexing Guidelines:** Frequently queried columns (e.g., `username`, `phone_number`, `team_code`, `verification_status`) are optimized using explicit B-Tree database indexes.
*   **Asynchronous Snapshots Strategy:** Dashboard aggregates read from precalculated snapshot tables (`analytics_snapshots`), avoiding heavy real-time query bottlenecks.
*   **Data Archival Policies:** Inactive profiles are archived after the retention period, removing contact details while preserving historical records for audit compliance.
*   **Database Backup Cycles:** Daily full backups and hourly incremental backups run automatically during off-peak hours.

---

## 34. Error Handling Architecture

*   **Frontend Error Handling:** Implements Axios interceptors to catch HTTP error codes, redirecting expired token sessions to the login gateway.
*   **Backend Error Handling:** Wraps logic inside try-except blocks, catching exceptions and returning standardized API error payloads to the frontend.
*   **Validation Failures:** Pydantic schema errors trigger clear, user-friendly forms warnings in the user interface.
*   **System Failures Recovery:** Database errors trigger transaction rollbacks, log details in Sentry, and return friendly JSON alerts to users.

---

## 35. Logging Architecture

*   **Application Logging:** Python log handlers capture operational activities (e.g., connection successes, task execution).
*   **Security Logging:** Tracks security alerts, including consecutive failed logins, blocked IPs, and unauthorized access attempts.
*   **Audit Logging:** Mutating database events write immutable entries to the database audit log.
*   **Log Retention:** Logs are retained for $7\text{ years}$ to meet compliance and performance reporting standards.

---

## 36. Backup Architecture

*   **Daily Full Backups:** Automated pg_dump scripts run daily during off-peak hours.
*   **Hourly Incremental Backups:** Hourly write-ahead log (WAL) archiving ensures minimal data loss in case of hardware failures.
*   **Off-site Storage:** Backups are encrypted and stored in independent, secure cloud storage buckets.
*   **Recovery Operations:** Point-in-time recovery validations verify restored database states to ensure data consistency.

---

## 37. Performance Architecture

*   **Server State Caching:** React Query caches API responses locally, reducing redundant backend queries.
*   **Database Query Optimization:** Frequently queried columns are optimized using indexes, and dashboard aggregates read from precalculated snapshot tables.
*   **Payload Pagination:** Queries returning list rosters use pagination bounds to keep database query loads light.
*   **Asset Performance:** Compiles frontend resources into optimized, light-weight bundles to ensure fast mobile page loads.

---

## 38. Scalability Architecture

*   **Stateless API Instances:** The FastAPI backend is stateless, allowing developers to scale instances horizontally behind a load balancer.
*   **Database Pool Management:** Database connections are managed via PgBouncer, preventing backend processes from exhausting connection pools.
*   **Asynchronous Queues:** Analytical calculations and log tracking are processed asynchronously to prevent request bottlenecks.
*   **Modular Extensibility:** Isolating feature modules in the directory layout prepares the platform to support Phase 2 and 3 without database alterations.

---

## 39. Deployment Architecture

The platform uses a standardized environment topology to guarantee system reliability:

*   **Local Developer Environments:** Docker-compose containers run hot-reloading backend servers, PostgreSQL databases, and local frontends.
*   **Testing Environments:** Local automated scripts verify endpoints and run unit/integration test suites before deployments.
*   **Staging Environments:** A replication of the production hosting setup used to validate database migrations and run end-to-end integration tests.
*   **Production Hosting Environments:** The live application hosting active profiles, geocoded maps, and reward payout claims.

---

## 40. Infrastructure Architecture

The hosting stack is designed for direct DirectAdmin compatibility and low hosting overhead:

*   **Operating System:** Standard Linux distribution (Ubuntu LTS or CentOS).
*   **Web Server / Proxy:** NGINX handles SSL termination, static files, and routes API queries to the Gunicorn/Uvicorn backend.
*   **Application Server:** ASGI backend (FastAPI) managed by Uvicorn.
*   **Relational Database:** High-availability managed PostgreSQL server.
*   **Local Storage Engine:** Local storage directory configured on the server, prepared for AWS S3 integration.
*   **SSL Certificates:** Let's Encrypt certificates managed automatically to enforce secure HTTPS traffic.
*   **Monitoring Agents:** Prometheus and Grafana gather server diagnostic metrics.

---

## 41. Disaster Recovery Architecture

*   **Point-in-Time Recovery (PITR):** Utilizes PostgreSQL WAL logs to restore database states to the exact second before a crash occurred.
*   **Infrastructure Redundancy:** Stateless API servers run across independent host regions to prevent outages.
*   **Rollback Workflows:** If a production update fails, the DevOps team rolls back application containers to the latest stable release.

---

## 42. Skill India Integration Strategy (Phase 2)

*   **Isolated Database Migrations:** New courses, assignments, and certification tables are added via Alembic, linking to existing `users` without altering core profile fields.
*   **User Role Extension:** Adds a `TRAINER` role in system configs, unlocking new dashboards.
*   **Decoupled Endpoint Routers:** Create a new `/api/v1/skills` API router mapping to its own services and repositories, ensuring zero changes to existing waste collection modules.

---

## 43. Clean India Integration Strategy (Phase 3)

*   **Registry Adaptability:** Phase 1 collection center registries are extended to support regional logistics registries (`clean_india_centers`, `waste_processing`).
*   **Role Adaptability:** Adds new administrative roles (Center Staff, District Coordinators) inheriting baseline Admin permissions while adding geolocated verification permissions.
*   **Extended Analytics Snapshots:** The existing analytics engine is easily extended to support advanced regional reporting, enabling detailed state-wide dashboards.

---

## 44. Technical Standards

### 44.1 Frontend Standards (React / TypeScript)
*   **Strict Typing:** `"strict": true` is mandatory in TypeScript configurations. Define explicit interfaces for components and API responses, avoiding the `any` type.
*   **Visual Optimization:** Never add heavy animations or visual packages. The frontend must remain lightweight and responsive on budget mobile devices.

### 44.2 Backend Standards (Python / FastAPI)
*   **PEP 8 Compliance:** Adhere to PEP 8 style standards. Type hints are mandatory on all functions, inputs, and output parameters.
*   **Decoupled Architecture:** Enforce strict boundaries. HTTP controllers only route paths, services manage business rules, and repositories interact with the database.

### 44.3 Database Standards (PostgreSQL)
*   **UUID Keys:** Transactional tables must utilize time-ordered **UUIDv7** primary keys for all major entities (`users`, `teams`, `referral_codes`, `waste_records`, `reward_claims`, `payment_transactions`, `notifications`, and `audit_logs`), enforcing foreign key constraints and `ON DELETE RESTRICT` rules to prevent orphaned records. UUIDv7 provides excellent index performance, chronological ordering, and fast inserts.
*   **Index Optimization:** Create explicit indexes on columns frequently searched or joined (e.g., `username`, `phone_number`, `team_code`).

### 44.4 API & Security Standards
*   **API Versioning:** Include version prefixes in endpoints (e.g., `/api/v1/*`) to support future upgrades without breaking integrations.
*   **Secure Sessions:** Access tokens carry a $15\text{ minute}$ lifespan, supported by HTTP-only refresh cookies ($7\text{ days}$) to block XSS and CSRF.

---

## 45. Conclusion

This Technical Architecture Document (`04_ARCHITECTURE.md`) provides the absolute software design, system layer, security configuration, and database strategy blueprints for the Athiyaman Platform – Digital India Phase 1. By detailing frontend modularity, FastAPI layer isolation, RBAC constraints, repository decouplings, geocoded map interfaces, and DirectAdmin deployment steps, it serves as a complete technical guide for engineering teams. All software builds, API integrations, and database modifications must adhere strictly to these principles, ensuring the platform remains secure, modular, performant, and scalable over its lifecycle.
