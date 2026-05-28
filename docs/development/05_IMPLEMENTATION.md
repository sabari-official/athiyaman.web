# Athiyaman Platform - Implementation Guide
## Phase 1 – Digital India Developer Handbook & Engineering Standards

---

## 1. Implementation Overview

This Implementation Guide serves as the official Developer Handbook and Engineering Standards reference for the Athiyaman Platform - Digital India Phase 1. It details the development strategies, coding practices, testing suites, CI/CD configurations, server environments, and governance policies required to build and maintain the platform.

*   **Implementation Goals:** To construct a secure, modular, highly auditable, and performant web platform that runs efficiently on Linux hosting environments.
*   **Development Strategy:** Follow a feature-modularized approach. Implement standard development patterns (Clean Architecture, Service Layer, Repository Pattern) to decouple logic and simplify future growth.
*   **Development Philosophy:** Prioritize stability, static typing, explicit data validations, and comprehensive audit logs over complex visual polish or styling animations.
*   **Quality Standards:** Target high test coverage ($>85\%$ core business paths), strict static type checking (TypeScript strict mode, Python type hints), and complete OWASP Top 10 security compliance.
*   **Team Responsibilities:** Product Owners define rules, UI/UX designers map user journeys, Frontend and Backend developers build decoupled layers, QA engineers validate logic, and DevOps engineers manage container releases.
*   **Project Lifecycle:** Iterative sprint delivery covering planning, coding, local validation, code review, staging audits, production release, and continuous diagnostics.

---

## 2. Development Environment

To maintain coding consistency, all developers must configure their local environments according to these specifications:

*   **Supported Operating Systems:**
    *   *Windows 10/11:* Enabled using WSL2 (Ubuntu 22.04 LTS preferred) or native PowerShell environments.
    *   *Linux:* Ubuntu 22.04 LTS or CentOS equivalents.
*   **Essential Development Tools:**
    *   *VS Code:* Selected IDE. Enforces standard configuration workspace files for formatting on save.
    *   *Git:* Version control client configured with default branch parameters.
    *   *Postman:* Rest API testing environment.
    *   *Database clients:* DBeaver or pgAdmin 4 for managing PostgreSQL engines.
*   **Required VS Code Extensions:**
    *   *Frontend:* Prettier - Code formatter, ESLint, Tailwind CSS IntelliSense, TypeScript Hero.
    *   *Backend:* Python (Microsoft extension package), Pylance (static analysis), Ruff (linting), SQLAlchemy Snippets.
    *   *System:* Docker, Markdown All in One, GitLens.

---

## 3. Project Structure

The project uses a clean workspace directory organization, separating client and server environments.

### 3.1 Frontend Directory Structure (`/src`)
```
src/
├── assets/             # Static media assets (official logos, graphics)
├── components/         # Reusable presentation components (custom forms, buttons)
├── contexts/           # Unified contexts managing session states
├── features/           # Self-contained business modules
│   ├── auth/           # Login screens, OTP challenges, and signup pages
│   ├── teams/          # Team registration and member roster screens
│   └── waste/          # Waste log forms, centers list, and geocoded maps
├── hooks/              # Global custom hooks managing device contexts
├── layouts/            # Page shell containers (menus, footers, sidebars)
├── pages/              # Unprotected info displays (Home, About, Contact)
├── services/           # Network API adapters (Axios clients)
├── types/              # Unified TypeScript definitions
└── utils/              # Helper utilities (IFSC verification, formatters)
```

### 3.2 Backend Directory Structure (`/app`)
```
app/
├── api/                # API router entry hubs mapping to module endpoints
├── core/               # Central configurations (JWT, database connections)
├── database/           # ORM session managers and migration scripts
├── middleware/         # System pipelines (CORS, error handlers, audit logs)
├── modules/            # Feature directories (router, schema, model, service)
│   ├── auth/           # Login services, OTP actions, and password hashes
│   ├── teams/          # Team managers, rosters, and validation checks
│   └── waste/          # Waste logs, center registers, geocodes, and maps
├── utils/              # Helper utilities (Aadhaar checking, geolocation, phone)
└── main.py             # Application entry point configuring middleware and routes
```

### 3.3 Database & System Directories
*   `/database/migrations`: Alembic schema migration script history files.
*   `/docs`: Standardized documentation resources (context models, deployment guides).
*   `/nginx`: Config files managing proxy routers and SSL certifications.

---

## 4. Repository Management

All developers must adhere to this Git branching strategy:

```
[main] ─────────────────────────────────────────────────────────────► (Production)
  ▲
  └─ [release/*] ───────────────────────────────────► (Staging QA)
       ▲
       └─ [dev] ──────────────────────────────► (Integration Hub)
            ▲
            ├─ [feature/*] ─────────► (Local Dev)
            └─ [hotfix/*] ──────────► (Emergency Patches)
```

*   **Branch Topology:**
    *   `main`: Active production branch. Direct commits here are blocked, requiring pull requests from release branches.
    *   `dev`: Integration hub for feature builds.
    *   `feature/*`: Branch for developing new features. Must branch off `dev` and merge back via audited PRs.
    *   `release/*`: Staging candidate branches used for quality audits.
    *   `hotfix/*`: Emergency patch branches addressing production bugs. Must branch off `main` and merge back to both `main` and `dev`.
*   **Branch Naming Rules:**
    *   Features: `feature/auth-otp-integration`
    *   Hotfixes: `hotfix/bank-ifsc-validation-patch`
*   **Commit Message Standards:** Commit messages must follow Conventional Commit guidelines:
    *   *Features:* `feat: add OTP validation to member signup`
    *   *Bugfixes:* `fix: correct password complexity validation check`
    *   *Documentation:* `docs: update deployment environment instructions`

---

## 5. Team Development Workflow

*   **Feature Development:** Developers create dedicated `feature/*` branches off the active `dev` branch.
*   **Code Review Process:** Merging code back to `dev` requires an open Pull Request, passing local linting checks, and receiving approval from at least one senior reviewer.
*   **Merge Guidelines:** Pull requests use squash-and-merge strategies, keeping the integration history clean.
*   **Staging QA Audits:** The DevOps team branches `release/*` from `dev` to deploy staging environments, running automated test suites before approval.
*   **Production Deployment:** Successful validation triggers merges from `release/*` to `main`, releasing container builds to production.

---

## 6. Frontend Setup Standards

*   **TypeScript Configurations:** Ensure `"strict": true` is configured in `tsconfig.json`. Avoid using the `any` type, defining explicit contracts and interfaces for all models and state payloads.
*   **Functional Components:** Enforce functional components with arrow-syntax definitions. Keep rendering components small and focused on layout duties.
*   **State Separation:** Business rules, calculations, and state mutations live inside custom hooks or context managers, keeping UI components clean.
*   **Data Synchronization:** Utilize **React Query** for all server-state API calls. UI states use local context or simple React hook parameters.
*   **Protected Route Boundaries:** Use route protection wrappers in React Router to intercept requests, validating JWT permissions before opening dashboards.

---

## 7. Backend Setup Standards

*   **FastAPI Modular Development:** Decouple FastAPI endpoints, validating request details using custom Pydantic schemas.
*   **Typed Endpoint Signatures:** Functional parameters, request models, and return states must declare strict Pydantic configurations.
*   **Pure Business Services:** Business rules and level progression calculations live inside dedicated Service classes. Routers route calls, and Services process logic.
*   **Repository Isolation Boundaries:** Repositories handle database interactions via SQLAlchemy ORM, managing transactional boundaries cleanly.
*   **Exception Interceptions:** Wrap logic in try-except blocks, catching exceptions and returning standardized HTTP error payloads.

---

## 8. Database Development Standards

*   **Naming Conventions:** Transactional tables (`users`, `teams`, `waste_records`) use lowercase, snake_case plural naming. Column definitions use lowercase snake_case singular names.
*   **UUIDv7 Primary Keys:** Enforce time-ordered **UUIDv7** datatypes for primary keys in all major transactional tables (`users`, `teams`, `referral_codes`, `waste_records`, `reward_claims`, `payment_transactions`, `notifications`, `audit_logs`) to optimize index trees, insert speeds, and chronological sorting. Standard integer keys are restricted strictly to master configurations (`levels`).
*   **Foreign Key Constraints:** Enforce relational integrity across all database tables. Define `ON DELETE RESTRICT` constraints to prevent accidental cascading data deletions.
*   **Index Optimization:** Create indexes on columns frequently searched or joined (e.g., `username`, `phone_number`, `team_code`, `verification_status`) to optimize query speeds.
*   **Database Schema Migrations:** Mutating database schemas requires generating and applying Alembic migration scripts, keeping version controls synchronized.

---

## 9. Environment Configuration

The platform defines four independent runtime environments:

*   **Development:** Docker-compose sandbox running hot-reloading servers and local database engines for rapid debugging.
*   **Testing:** Local automated testing environments used to validate databases, run integration suites, and perform security scans.
*   **Staging:** Identical replica of the production environment used to run quality audits and validate database migrations.
*   **Production:** Active environment hosting active profiles, geocoded maps, and reward payout claims.
*   **Secrets Management:** Sensitive keys (JWT credentials, database passwords, API keys) must be loaded from external environments using Pydantic Settings, keeping credentials out of repositories.

---

## 10. Configuration Management

*   **Unified Backend Environment Variables:** Configured using Pydantic Settings:
    ```ini
    DATABASE_URL=postgresql+psycopg2://db_user:secure_pwd@db_host:5432/athiyaman
    JWT_SECRET=super_secret_cryptographic_key_32_bytes_min
    JWT_ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=15
    REFRESH_TOKEN_EXPIRE_DAYS=7
    STORAGE_TYPE=LOCAL
    STORAGE_PATH=/var/www/athiyaman/uploads
    GOOGLE_MAPS_KEY=gmaps_api_credential_key
    ```
*   **Unified Frontend Environment Variables:**
    ```ini
    VITE_API_URL=https://api.athiyaman.in/api/v1
    VITE_GOOGLE_MAPS_KEY=gmaps_api_credential_key
    ```

---

## 11. General Coding Standards

*   **Readability:** Code must be highly readable and self-documenting. Use descriptive variable and function names.
*   **Consistency:** Follow PEP 8 guidelines in Python and standard ESLint configurations in React.
*   **Reusability:** Refactor shared logic (such as date formatters and input checks) into global helper utilities.
*   **Documentation Requirements:** Public modules, routes, service functions, and custom hooks must include clear docstrings and inline comments detailing logic and error paths.

---

## 12. Frontend Coding Standards

*   **Component File Naming:** Component files must use PascalCase (e.g., `LeaderCard.tsx`). Helper files and hooks must use camelCase (e.g., `useWasteRecords.ts`).
*   **TypeScript Props Interfaces:** Enforce strict type definitions for all props in React components, avoiding anonymous type declarations.
*   **Visual Optimization:** Avoid using heavy visual packages or custom animation libraries. All layouts must remain responsive, clean, and accessible on low-end budget mobile devices.
*   **Error Catching:** Implement catch blocks on all promise calls, displaying descriptive toast warnings to notify users of network errors.

---

## 13. Backend Coding Standards

*   **PEP 8 Compliance:** Adhere strictly to PEP 8 formatting rules, validating code styles using Ruff before commits.
*   **Naming Configurations:**
    *   Classes use PascalCase (e.g., `TeamService`).
    *   Functions and variables use snake_case (e.g., `calculate_level_progress`).
    *   Constants use uppercase snake_case (e.g., `MAX_OTP_ATTEMPTS`).
*   **Response Schemas:** API routers must explicitly declare response models, preventing the leakage of internal database structures to client networks.

---

## 14. API Development Standards

*   **REST Principles:** Follow RESTful conventions. API paths must use lowercase plural nouns (e.g., `/api/v1/teams`).
*   **API Versioning Strategy:** Include version prefixes in API endpoints (e.g., `/api/v1/*`) to support future upgrades.
*   **Pagination Standards:** Queries returning list rosters must enforce standard parameters (`page`, `limit`) and return paginated payloads:
    ```json
    {
      "items": [...],
      "total": 124,
      "page": 1,
      "limit": 20
    }
    ```
*   **API Error Standard Format:**
    ```json
    {
      "detail": {
        "code": "INVALID_REFERRAL_CODE",
        "message": "The referral code entered is either expired or at maximum capacity."
      }
    }
    ```

---

## 15. Security Implementation Standards

*   **Authentication & Session Management:**
    *   Passwords must be hashed using high-computation **Argon2id** algorithms, preventing brute-force compromises.
    *   Authentication APIs issue short-lived JWT access tokens ($15\text{ minutes}$) containing user identity and role scopes.
    *   Session persistence utilizes HTTP-only, secure, `SameSite=Strict` cookies hosting refresh tokens ($7\text{ days}$) to block Cross-Site Scripting (XSS) and Cross-Site Request Forgery (CSRF).
*   **Role-Based Access Control (RBAC):**
    *   Strict, server-side route guards. A Team Member trying to reach `/api/v1/admin/*` is blocked at the FastAPI router injection layer, throwing an immediate `403 Forbidden` response.
    *   Role boundaries are enforced within SQL queries using session-bounded conditions (e.g., matching requested user records directly to the authenticated caller's JWT user ID).
*   **Input & Document Validation:**
    *   All external payloads undergo strict schema enforcement via Pydantic, escaping characters to block SQL injection and Cross-Site Scripting (XSS).
    *   Document upload engines allow only certified MIME-types (`image/jpeg`, `image/png`, `application/pdf`).
    *   Uploaded files are dynamically renamed with UUID paths and checked for size boundaries ($5\text{MB}$ maximum) to prevent disk space exhaustion.
*   **Rate Limiting & Threat Prevention:**
    *   API gateways apply strict rate limits (e.g., standard endpoints capped at $60\text{ requests/minute}$; authentication points limited to $5\text{ attempts/minute}$ per IP).
    *   Consecutive failed logins lock user accounts temporarily, notifying developers via the Security Center interface.
*   **Comprehensive Audit Logs:**
    *   Every business transaction writes to the `audit_logs` table.
    *   Audit logs contain: User UUID, active role, action type, entity ID, request IP address, client device footprint, and timestamp.
    *   Once written, these logs are database-restricted from modifications or deletions, maintaining audit immutability.

---

## 16. Logging Standards

*   **Application Logs:** Capture baseline server actions (e.g., startup events, connection successes) using clean standard outputs.
*   **Security Logs:** Tracks security alerts, failed login attempts, IP blocks, and unauthorized access attempts.
*   **Audit Logging:** Mutating database events write immutable entries to the database audit log.
*   **Log Retention:** Logs are retained for $7\text{ years}$ to meet compliance and performance reporting standards.

---

## 17. Audit Implementation Standards

*   **Captured Events:** User registrations, logins, profile updates, team creations, waste approvals, and payment transactions.
*   **Audit Log Payload Format:**
    ```json
    {
      "timestamp": "2026-05-23T12:00:00Z",
      "user_id": "usr-8291-uuid-value",
      "role": "ADMIN",
      "action": "APPROVE_CLAIM",
      "entity_type": "CLAIM",
      "entity_id": "clm-9021-uuid-value",
      "ip_address": "192.168.1.1",
      "device": "Mozilla/5.0 ... Chrome/120.0"
    }
    ```
*   **Access Protections & Immutability:** Audit logs are visible only to Admins and Developers through read-only portals. The database blocks any update and delete queries on `audit_logs`, `notification_logs`, and `payment_audit_logs` tables, enforcing permanent *INSERT-only* immutability to prevent fraud and ensure compliance.

---

## 18. Notification Standards

*   **Asynchronous Alerts:** The notification engine routes alerts asynchronously to prevent application bottlenecks.
*   **Notification Targets:** Allows broadcasting alerts to all users, specific roles, specific teams, or individual users, and logs read/unread states.
*   **SMS/WhatsApp Adaptability:** Third-party integrations are managed via interface adapters, allowing developers to connect SMS and WhatsApp providers by adjusting configs.

---

## 19. File Storage Standards

*   **Storage Folder Layout:** Files are stored in secure directories outside the public web server, organized by upload categories.
*   **Upload Rules:** Restricts uploads to secure image and document types (JPEG, PNG, PDF), verifying that files do not exceed the $5\text{MB}$ limit.
*   **Access Control:** Files are served to authorized Admins via temporary, expiring secure URLs.
*   **Data Erasure Protocols:** Profiles marked for deletion undergo anonymization, removing contact details while preserving historical records for audit compliance.

---

## 20. Error Handling Standards

*   **Axios Interceptors:** The frontend uses interceptors to catch HTTP error codes, redirecting expired token sessions to the login gateway.
*   **Backend Exception Middleware:** A catch-all middleware intercepts system errors, logs details in Sentry, and returns standardized API error payloads.
*   **Data Rollback Procedures:** Database errors trigger transaction rollbacks, keeping data registers consistent during failures.

---

## 21. Testing Strategy

High quality is maintained through strict validation strategies:

```
┌────────────────────────────────────────────────────────┐
│                        Unit Tests                      │
│             (Pytest & Vitest: Logic & Utils)           │
├────────────────────────────────────────────────────────┤
│                     Integration Tests                  │
│             (API Endpoints & Database States)          │
├────────────────────────────────────────────────────────┤
│                       Security Scans                   │
│             (RBAC Checks & File Upload Protections)    │
├────────────────────────────────────────────────────────┤
│                    User Acceptance (UAT)               │
│             (Full Journey Workflows & UI Scans)        │
└────────────────────────────────────────────────────────┘
```

*   **Unit Testing:**
    *   *Backend:* Written using **Pytest**. Focuses on testing standalone components, mathematical formulas, and helper utilities.
    *   *Frontend:* Written using **Vitest**. Tests key utility handlers and isolated UI rendering.
*   **Integration Testing:**
    *   Validates complete database-to-endpoint integrations.
    *   Tests multi-step API workflows, such as checking that creating a team creates the team record, updates user roles, and increments audit logs in a single transaction.
*   **Security Testing:**
    *   Automated scripts verify endpoint protection, confirming that Member accounts receive strict `403 Forbidden` errors when accessing `/api/v1/admin/*` endpoints.
    *   Validates upload filters by testing malicious extensions, and tests rate limiters using rapid mock API calls.
*   **User Acceptance Testing (UAT):**
    *   Tests end-to-end citizen journeys (from Visitor sign-up and Leader team-up to Waste collection and Payout disbursement) using browser automation scripts.

---

## 22. Frontend Testing Standards

*   **Component Tests:** Validate standard UI rendering, checking that buttons, inputs, and elements display correctly.
*   **Form Validations:** Tests check input bounds (e.g., verifying that phone inputs reject alphabetical characters).
*   **State Navigations:** Verifies that routing wrappers intercept access requests, redirecting unauthorized sessions to the login gateway.

---

## 23. Backend Testing Standards

*   **Service Core Tests:** Test business rules, progression metrics, and level validation checks.
*   **Repository Persistence Tests:** Verify that repository queries execute successfully, managing relations and constraints.
*   **API Integrations:** Validate endpoints using mock database sessions, confirming that routers return clean JSON payloads.
*   **RBAC Route Guards:** Test route permissions, confirming that unprivileged users receive `403 Forbidden` errors.

---

## 24. Database Testing Standards

*   **Constraint Verifications:** Validate constraints, checking that duplicate user registrations are blocked.
*   **Relational Integrity Tests:** Confirm that deleting a team leader account is blocked while active members are linked to the team.
*   **Migration Script Validations:** Validate Alembic scripts, ensuring schema upgrades and rollbacks run successfully without data loss.

---

## 25. Performance Standards

*   **API Response Target:** Standard API endpoints must respond in less than $200\text{ms}$ under normal load conditions.
*   **Frontend Mobile Assets:** Dashboard assets must be highly optimized, load in under $1.5\text{ seconds}$ on standard mobile connections, and avoid heavy visual rendering libraries.
*   **Precalculated Dashboards:** Analytical dashboards fetch precalculated snapshots, avoiding heavy real-time query bottlenecks.

---

## 26. Monitoring Standards

*   **Server Health Metrics:** Capture CPU usage, memory utilization, and active database connection pool stats.
*   **Endpoint Health Monitoring:** Grafana dashboards track system health, alert developers to bottlenecks, and log API response speeds.
*   **Crash Integrations:** System crashes and coding exceptions are sent to the Developer Portal via Sentry for diagnosis.

---

## 27. Backup Standards

*   **Scheduled Backups:** Daily full backups and hourly incremental backups run automatically during off-peak hours.
*   **Backup Verification:** Backups are encrypted and stored in independent, secure cloud storage buckets, running restore validation tests weekly to ensure backup integrity.
*   **Manual Backups:** Developers can trigger manual backups before deploying feature updates.

---

## 28. Recovery Standards

*   **Point-in-Time Recovery (PITR):** Utilizes PostgreSQL WAL logs to restore database states to the exact second before a crash occurred.
*   **Application Container Rollbacks:** If a production update fails, the DevOps team rolls back the application containers to the latest stable release.
*   **Data Health Audits:** Validation scripts check database keys and relational constraints after a recovery restore to ensure data consistency.

---

## 29. Deployment Strategy

*   **Local Developer Environments:** Docker-compose containers run hot-reloading backend servers, PostgreSQL databases, and local frontends.
*   **Testing Environments:** Local automated scripts verify endpoints and run unit/integration test suites before deployments.
*   **Staging Environments:** A replication of the production hosting setup used to validate database migrations and run end-to-end integration tests.
*   **Production Hosting Environments:** The live application hosting active profiles, geocoded maps, and reward payout claims.

---

## 30. Linux Server Standards

*   **Configuration Security:** Disable root logins and configure firewall rules, allowing incoming traffic only on secure ports ($80\text{ (HTTP)}$, $443\text{ (HTTPS)}$).
*   **Directory Permissions:** Run applications under unprivileged system users (e.g., `www-data`), keeping folders locked to read-only permissions except for secure upload paths.
*   **Reverse Proxy Routing:** NGINX handles static files, manages SSL configurations, and proxies API requests to the Uvicorn application server.

---

## 31. DirectAdmin Deployment Standards

*   **Static Asset Delivery:** Compile frontend assets and serve them directly via NGINX.
*   **Backend Run Managers:** Deploy backend code inside isolated Python virtual environments, managing active processes using Systemd.
*   **SSL Certificates:** Configure Let's Encrypt SSL certificates to enforce secure HTTPS traffic.
*   **Database Management:** PostgreSQL runs on a localized port, rejecting external connections.

---

## 32. CI/CD Strategy

*   **GitHub Actions Pipelines:**
    ```
    Developer Push ──► Lint & Type Audits ──► Test Suites ──► Build Containers ──► Deploy to Staging
    ```
*   **Release Validations:** Successful staging tests enable deployment triggers to push updates to the production cluster.
*   **Automatic Rollbacks:** If health checks fail post-deployment, the pipeline rolls back application containers to the latest stable release.

---

## 33. Release Management

*   **Semantic Versioning:** Releases must use semantic versioning structures (`vMAJOR.MINOR.PATCH`):
    *   *Major:* Substantial architectural updates.
    *   *Minor:* New modular features.
    *   *Patch:* Minor bugfixes and performance updates.
*   **Release Approvals:** Merging to the `main` branch requires approval from the Lead Developer and successful validation testing.
*   **Release Notes:** Documentation detailing release changes, bugfixes, and database migrations must accompany all deployments.

---

## 34. Documentation Standards

*   **Docstring Standards:** Backend code must include PEP 257 docstring parameters.
*   **API Documentation:** Enforce automated Swagger documentation for backend endpoints.
*   **System Overviews:** Keep architecture and operational documentation updated in the repository `/docs` directory.

---

## 35. Maintenance Standards

*   **Scheduled Maintenance:** Bug fixes, performance optimizations, and package updates are batched and deployed during off-peak hours.
*   **Database Maintenance:** Automated vacuum operations run weekly to optimize indexes and keep database performance high.
*   **Security Patches:** Critical security updates are prioritised and deployed immediately.

---

## 36. Security Maintenance

*   **Dependency Audits:** Automated security scans check for vulnerable packages weekly.
*   **Administrative Audits:** Conduct monthly reviews of admin access logs and system settings to confirm security compliance.
*   **Vulnerability Remediation:** High-priority vulnerabilities require immediate updates, logging actions in the audit trail.

---

## 37. Scalability Standards

*   **Horizontal Scalability:** Keep the FastAPI backend stateless, allowing developers to scale instances horizontally behind a load balancer.
*   **Team Member Counter Strategy:** Maintain precalculated `member_count` in the `teams` table to support teams with thousands of members. The database must increment `member_count` when a member joins and decrement it when a member leaves. User dashboards must read `member_count` directly, strictly prohibiting expensive SQL `COUNT` queries on `team_members` to protect connection pools.
*   **Database PgBouncer Pool Managers:** Manage database connections using PgBouncer, preventing backend processes from exhausting connection pools.
*   **Analytical aggregates:** Precalculated snapshots avoid real-time query bottlenecks, ensuring fast dashboard load times.

---

## 38. Skill India Implementation Preparation (Phase 2)

*   **User Role Extension:** Simply add a `TRAINER` role in system auth configs, unlocking new dashboards.
*   **Isolated Database Migrations:** Add new courses, assignments, and certification tables via Alembic, linking to existing `users` without altering core profile fields.
*   **Decoupled Endpoint Routers:** Create a new `/api/v1/skills` API router mapping to its own services and repositories, ensuring zero changes to existing waste collection modules.

---

## 39. Clean India Implementation Preparation (Phase 3)

*   **Registry Adaptability:** Phase 1 collection center registries are extended to support regional logistics registries (`clean_india_centers`, `waste_processing`).
*   **Role Adaptability:** Adds new administrative roles (Center Staff, District Coordinators) inheriting baseline Admin permissions while adding geolocated verification permissions.
*   **Extended Analytics Snapshots:** The existing analytics engine is easily extended to support advanced regional reporting, enabling detailed state-wide dashboards.

---

## 40. Production Readiness Checklist

Before launching Phase 1, ensure all items on this checklist are completed:

*   [ ] **Security Checklist:**
    *   Confirm all passwords hash using Argon2id.
    *   Verify all endpoint route guards are protected by RBAC.
    *   Verify PII fields (Aadhaar, bank records) are encrypted at rest.
    *   Verify SSL certificates are active, enforcing secure HTTPS traffic.
*   [ ] **Testing Checklist:**
    *   Confirm core unit and integration test coverage exceeds $85\%$.
    *   Verify all endpoint tests pass successfully.
    *   Confirm form input checks are validated against Pydantic schemas.
*   [ ] **Deployment Checklist:**
    *   Verify CI/CD pipelines run without errors.
    *   Confirm environmental secrets are loaded securely from external environments.
    *   Verify backup cron jobs run daily.
*   [ ] **Monitoring Checklist:**
    *   Confirm system diagnostic tools capture CPU, memory, and database metrics.
    *   Verify crash integration alerts are routed successfully to Sentry.
*   [ ] **Documentation Checklist:**
    *   Verify API swagger documentation generates successfully.
    *   Confirm repository `/docs` directories contain updated deployment guides.

---

## 41. Development KPIs

*   **Code Coverage:** Maintain test coverage for core business logic above $85\%$.
*   **API Response Uptime:** Maintain standard endpoint response latencies under $200\text{ms}$.
*   **Security Compliance:** Maintain zero high-priority vulnerabilities in dependency scans.
*   **Bug Resolution Time:** Average bug resolution turnaround times must stay under $24\text{ hours}$ for critical items.

---

## 42. Team Governance

*   **Code Reviews:** Every pull request requires review and approval from at least one senior developer.
*   **Ownership Boundaries:** Developers are assigned explicit ownership of specific modules (e.g., Auth, Waste), serving as primary reviewers for related code changes.
*   **Approval Process:** Operational modifications and changes to database structures require approval from the Lead Developer and Product Owner.

---

## 43. Long-Term Maintenance Plan

*   **Year 1 (Stability & Optimization):** Focus on stabilizing pilot operations, optimizing database queries, and refining waste verification turnaround queues.
*   **Year 2 (Phase 2 & Mobile Apps):** Integrate Phase 2 (Skill India) modules and develop native mobile applications.
*   **Year 3 (Phase 3 & Integrations):** Launch Phase 3 (Clean India) environmental operations, integrate automated payment APIs, and expand services nationally.
*   **Technical Debt Strategy:** Devote $15\%$ of each sprint cycle to refactoring, updating dependencies, and keeping the codebase clean.

---

## 44. Conclusion

This Implementation Guide (`05_IMPLEMENTATION.md`) serves as the official Developer Handbook and Development Standard Guide for the Athiyaman Platform - Digital India Phase 1. By detailing local setups, repository controls, coding practices, testing strategies, deployment setups, and release management rules, it provides a comprehensive guide for developers. All code changes, API updates, and system operations must align with these guidelines, ensuring the platform remains highly secure, traceable, performant, and scalable over its lifecycle.
