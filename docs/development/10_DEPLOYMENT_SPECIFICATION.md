# Athiyaman Platform - Deployment Specification Document
## Phase 1 – Digital India DevOps, Hosting & Production Operations Standards

---

## 1. Deployment Overview

This Deployment Specification Document defines the production infrastructure, deployment pipelines, hosting profiles, backup crons, disaster recovery coordinates, and monitoring models for the Athiyaman Platform - Digital India Phase 1. It acts as the official guide for DevOps engineers to configure, secure, monitor, and scale the platform in production environments.

*   **Objectives:**
    *   *High Performance:* Dashboard response limits under $2\text{ seconds}$ on mobile connections.
    *   *High Availability:* Target $99.9\%$ system availability.
    *   *Secure Infrastructures:* Comprehensive server hardening with native firewalls and SSL certificates.
    *   *Stateless Scalability:* Stateless API architecture supporting horizontal scaling behind a load balancer.

---

## 2. Infrastructure Overview

The platform uses a decoupled, four-tier architecture model to isolate concerns and protect backend logic:

```
                  ┌───────────────────────────────┐
                  │            Users              │
                  └───────────────┬───────────────┘
                                  │ (HTTPS / JSON)
                                  ▼
                  ┌───────────────────────────────┐
                  │       Vercel Frontend         │
                  │  (Static Edge Distribution)   │
                  └───────────────┬───────────────┘
                                  │
                                  ▼ (API Gateway / NGINX)
                  ┌───────────────────────────────┐
                  │       FastAPI Backend         │
                  │  (Stateless ASGI Containers)  │
                  └───────────────┬───────────────┘
                                  │
            ┌─────────────────────┴─────────────────────┐
            ▼ (SQLAlchemy)                              ▼ (Local Storage)
┌───────────────────────────┐               ┌───────────────────────────┐
│    PostgreSQL Database    │               │    Document File Storage  │
│  (ACID Relational Engine) │               │   (Private upload paths)  │
└───────────────────────────┘               └───────────────────────────┘
```

*   **Relational Database:** High-availability managed PostgreSQL server handles transactional persistence.
*   **File Storage:** Local upload paths isolate sensitive scans (Aadhaar, bank books) outside public web directories.
*   **Asynchronous Queues:** Redis handles task scheduling, routing heavy operations asynchronously to background workers.

---

## 3. Hosting Environment

The deployment stack is designed for direct DirectAdmin compatibility and low hosting overhead.

*   **Production Hosting:** High-performance Linux Virtual Private Server (VPS) configured on standard CentOS or Ubuntu LTS distributions.
*   **DirectAdmin Integration:** Manages domains, handles DNS mappings, manages PostgreSQL instances, and configures Let's Encrypt SSL certificates automatically.
*   **Subdomain Strategy:**
    *   *Production Frontend:* `https://athiyaman.in`
    *   *Production API Backend:* `https://api.athiyaman.in`
    *   *Staging Panel:* `https://staging.athiyaman.in`
*   **Future Scaling:** Lightweight, containerized virtual instances (Docker) allow scaling nodes horizontally behind a central NGINX gateway.

---

## 4. Server Architecture

*   **Application Server (FastAPI):** Resolves routes asynchronously using Uvicorn processes. Manages background workers to handle non-blocking, asynchronous tasks.
*   **Database Server (PostgreSQL):** PostgreSQL engine handles transactional persistence, using PgBouncer pool managers to optimize database connections.
*   **Storage Layer:** Local directories house upload scans, using AES-256 rest-encryption to secure PII data.
*   **Monitoring Layer:** Prometheus and Grafana gather server diagnostic metrics. Crash integration alerts are routed successfully to Sentry.
*   **Backup Layer:** Encrypted automated backups are saved in independent, secure off-site cloud storage buckets.

---

## 5. Environment Strategy

The platform maintains four isolated environments to ensure clean code transitions:

*   **Development:** Local developer machines running docker-compose sandboxes with hot-reloading configurations.
*   **Testing:** Automated testing pipelines used to run unit and integration test suites before staging.
*   **Staging:** Identical replica of the production hosting setup used to validate database migrations and run end-to-end integration tests.
*   **Production:** Active environment hosting active profiles, geocoded maps, and reward payout claims.

---

## 6. Linux Server Standards

*   **Operating System:** Enforces Ubuntu 22.04 LTS or CentOS 8 distributions, locked to $64\text{-bit}$ architectures.
*   **Directory Structure Standards:**
    *   *Static Web Assets:* `/var/www/athiyaman/frontend`
    *   *Backend Files:* `/var/www/athiyaman/backend`
    *   *Secure Upload Directory:* `/var/www/athiyaman/uploads`
*   **User Management:** Block direct root logins. Create an unprivileged system user (e.g., `athiyaman_user`) to execute processes.
*   **Directory Permissions:** Run applications under unprivileged system users (e.g., `www-data`), keeping folders locked to read-only permissions except for secure upload paths (`chmod 700`).
*   **Security Hardening:** Enable UFW firewalls, configure SSH key-only access on non-standard ports, and deploy Fail2Ban to block brute-force attacks.
*   **Resource Management:** Enforce process controls (`systemd` limit bounds) to prevent memory exhaustion.

---

## 7. DirectAdmin Configuration

*   **Domain & Subdomain Setup:** Map domains and configure virtual host directories to separate frontend assets from API routes.
*   **SSL Certificates:** Enable automated Let's Encrypt certificates to enforce secure HTTPS traffic.
*   **Application Server Process:** Deploy backend code inside isolated Python virtual environments, managing active processes using Systemd.
*   **Database Management:** Configure PostgreSQL database instances on local ports, denying external access.
*   **Maintenance Procedures:** DirectAdmin manages standard server task schedules, executing automated cleanup scripts during off-peak hours.

---

## 8. Frontend Deployment Strategy

*   **React Build Process:** Compile frontend assets into highly optimized, minified bundles, stripping debugging console logs.
*   **Static Asset Delivery:** Serve compiled assets directly via NGINX, using global edge content delivery networks (CDNs) to optimize load speeds.
*   **Browser Caching Rules:** Configure NGINX cache headers to cache static assets for $1\text{ year}$ while blocking HTML caching to force immediate updates.
*   **Asset Compression:** Enable Gzip or Brotli compression to minimize asset download footprints.
*   **Version Control:** Compile scripts with unique hash stamps to prevent browser cache conflicts.
*   **Rollback Strategy:** DevOps pipelines keep past production builds active in backup directories, enabling instant NGINX symlink rollbacks if updates fail.

---

## 9. Backend Deployment Strategy

*   **FastAPI Deployments:** Deploy backend services in containerized Gunicorn processes managing Uvicorn worker instances.
*   **Application Runtime:** Managed via Systemd service controllers, running under unprivileged system accounts:
    ```ini
    [Unit]
    Description=Athiyaman FastAPI ASGI Server
    After=network.target
    
    [Service]
    User=athiyaman_user
    WorkingDirectory=/var/www/athiyaman/backend
    ExecStart=/var/www/athiyaman/backend/venv/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 127.0.0.1:8000
    Restart=always
    RestartSec=5
    
    [Install]
    WantedBy=multi-user.target
    ```
*   **Environmental Secrets:** System configurations are loaded from secure `.env` files using Pydantic Settings, keeping credentials out of repositories.

---

## 10. Database Deployment Strategy

*   **PostgreSQL Configurations:** Installs PostgreSQL v15+ on standard database servers, configuring parameters to optimize resources:
    *   `shared_buffers`: Allocate $25\%$ of total system RAM.
    *   `max_connections`: Default capped at $100$ connections, utilizing PgBouncer pool managers to optimize active pools.
*   **Access Protections:** Bind PostgreSQL to the local loopback address (`127.0.0.1`), blocking external connections.
*   **Audit Logging:** Logs transactional mutations in the `audit_logs` table, blocking updates or deletions on the log registry.

---

## 11. File Storage Deployment

*   **Storage Folder Layout:** Files are stored in secure directories outside the public web server, organized by upload categories:
    *   `/var/www/athiyaman/uploads/aadhaar/`
    *   `/var/www/athiyaman/uploads/bank/`
    *   `/var/www/athiyaman/uploads/waste/`
*   **Access Control:** Files are served to authorized Admins via temporary, expiring secure URLs.
*   **Retention Policies:** User document scans expire and are archived $1\text{ year}$ after verification validation.

---

## 12. SSL & HTTPS Standards

*   **Let's Encrypt:** DirectAdmin manages Let's Encrypt certificates automatically, renewing credentials $30\text{ days}$ before expiry.
*   **HTTPS Redirection:** NGINX blocks standard port 80 traffic, redirecting queries to secure HTTPS connections.
*   **Security Protocol standards:** Restricts connections to TLS 1.2 or TLS 1.3 standards, blocking legacy SSL protocols to protect sessions.

---

## 13. Environment Variables

*   **Configuration Strategy:** Backend servers load variables from secure `.env` files, excluding local files from version control repositories.
*   **Application Secrets:** Configured using Pydantic Settings:
    ```ini
    DATABASE_URL=postgresql+psycopg2://db_user:secure_pwd@127.0.0.1:5432/athiyaman
    JWT_SECRET=super_secret_cryptographic_key_32_bytes_min
    JWT_ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=15
    REFRESH_TOKEN_EXPIRE_DAYS=7
    STORAGE_TYPE=LOCAL
    STORAGE_PATH=/var/www/athiyaman/uploads
    GOOGLE_MAPS_KEY=gmaps_api_credential_key
    ```

---

## 14. Security Hardening

*   **Firewall Configuration:** Configures UFW firewall blocks:
    ```bash
    ufw default deny incoming
    ufw default allow outgoing
    ufw allow 22/tcp  # Custom SSH port
    ufw allow 80/tcp  # HTTP port
    ufw allow 443/tcp # HTTPS port
    ufw enable
    ```
*   **Port Management:** Disable unneeded network services, keeping active database ports inaccessible from external networks.
*   **SSH Configurations:** Change default SSH ports, enforce key-based access controls, and disable root user access.

---

## 15. Authentication Security

*   **OAuth2 JWT Bearer Tokens:** Access tokens expire after $15\text{ minutes}$, carrying user role scopes.
*   **Refresh Tokens:** Secure, HTTP-only, `SameSite=Strict` refresh cookies expire after $7\text{ days}$.
*   **Account Lockout Policy:** Track failed logins in Redis. Reaching 5 failed login attempts blocks the account, locks the session for $15\text{ minutes}$, and logs a high-priority alert.
*   **API Rate Limiters:** Enforces limits (e.g., standard endpoints capped at $60\text{ requests/minute}$) to prevent spammed requests.

---

## 16. Aadhaar & Bank Data Protection

*   **PII Encryption at Rest:** Encrypts PII (Aadhaar entries, bank accounts) at rest using AES-256 algorithms. Displays masked values on user interfaces to protect privacy.
*   **Aadhaar Duplicate Check:** Cryptographic hashes of Aadhaar numbers are saved in `aadhaar_hash` to detect duplicate profiles without storing plain text credentials.
*   **Access Control Trails:** Reading unmasked PII values requires Admin role permissions and logs access events in the audit trail.

---

## 17. File Upload Security

*   **Upload Vetting Rules:** Upload validations must inspect file signatures, check size constraints (max $5\text{MB}$), remove unneeded metadata, rename files, store uploads outside public directories, and enforce authorization checks.
*   **Allowed File Formats:** Enforces whitelist limits: PDF, PNG, and JPEG files are allowed.
*   **Blocked File Formats:** Rejects executable formats (EXE, BAT, JS, SH, DLL), returning error alerts.

---

## 18. Nginx Architecture

```
User request ──► NGINX Reverse Proxy ──┬──► [Port 80 to 443 SSL Redirect]
                                       ├──► [Static Asset Caching]
                                       └──► [Gunicorn/FastAPI App Server]
```

*   **Reverse Proxy Settings:** NGINX handles static files, manages SSL configurations, and proxies API requests to the Gunicorn/Uvicorn backend.
*   **Compression Configurations:** Enable Gzip compression to minimize asset download footprints.
*   **Security Header Rules:** Enforces standard headers to protect sessions (X-Content-Type-Options, X-Frame-Options, X-XSS-Protection, Content-Security-Policy).

---

## 19. Logging Strategy

*   **Application Logs:** Logs operational activities using automated rotation systems.
*   **Security Logs:** Tracks failed logins, rate limit alerts, and IP blocks.
*   **Audit Logging:** Mutating database events write immutable entries to the database audit log.
*   **Log Retention:** Logs are retained for $7\text{ years}$ to meet regulatory audit standards.

---

## 20. Monitoring Strategy

*   **Server Diagnostics:** Prometheus collects CPU usage, memory utilization, and active database connection pool stats.
*   **Endpoint Health Monitoring:** Grafana dashboards track system health, alert developers to bottlenecks, and log API response speeds.
*   **Sentry Integrations:** Code exceptions and system errors are sent to the Developer Portal via Sentry for diagnosis.

---

## 21. Health Check Strategy

*   **Frontend Health Checks:** Pings static asset routes to confirm asset availability.
*   **Backend Health Checks:** API endpoint `/api/v1/health` checks backend service status.
*   **Database Connectivity Checks:** Health check queries verify PostgreSQL connection pools.

---

## 22. Alerting Strategy

*   **System Alerts:** Critical alerts are triggered if CPU/Memory usage exceeds $85\%$ for $5\text{ minutes}$.
*   **Vulnerability Detections:** Security logs alert developers to failed logins, IP blocks, and unauthorized access attempts.
*   **Notifications Routing:** Real-time system alerts are routed directly to developers via the WhatsApp API integration adapter.

---

## 23. Backup Strategy

*   **Daily Full Backups:** Automated pg_dump scripts run daily during off-peak hours.
*   **Hourly Incremental Backups:** Hourly write-ahead log (WAL) archiving ensures minimal data loss in case of hardware failures.
*   **Backup Verification:** Backups are encrypted and stored in independent, secure cloud storage buckets, running restore validation tests weekly to ensure backup integrity.
*   **Configuration Backups:** Backup files copy environment secrets and server configuration parameters to secure repositories.

---

## 24. Disaster Recovery Strategy

*   **Point-in-Time Recovery (PITR):** Utilizes PostgreSQL WAL logs to restore database states to the exact second before a crash occurred.
*   **Recovery Targets:**
    *   *RTO (Recovery Time Objective):* Restore system services in less than $2\text{ hours}$.
    *   *RPO (Recovery Point Objective):* Target minimal data loss (less than $1\text{ hour}$ of data transactions).
*   **Data Health Audits:** Validation scripts check database keys and relational constraints after a recovery restore to ensure data consistency.

---

## 25. Business Continuity Strategy

*   **Service Redundancy:** Stateless API servers run across independent host regions to prevent outages.
*   **Operational Continuity:** Vetting queues can be managed by other administrators in the event of local office disruptions.
*   **System Continuities:** Backups are stored in independent cloud storage locations, ensuring recovery options in case of major host outages.

---

## 26. CI/CD Strategy

*   **GitHub Actions Pipelines:**
    ```
    Developer Push ──► Lint & Type Audits ──► Test Suites ──► Build Containers ──► Deploy to Staging
    ```
*   **Release Validations:** Successful staging tests enable deployment triggers to push updates to the production cluster.
*   **Automatic Rollbacks:** If health checks fail post-deployment, the pipeline rolls back application containers to the latest stable release.

---

## 27. GitHub Workflow

*   **Repository Strategy:**
    *   `main`: Active production branch. Direct commits here are blocked.
    *   `dev`: Integration hub for feature builds.
    *   `feature/*`: Branch for developing new features, merged back to `dev` via pull requests.
    *   `release/*`: Staging candidate branches used for quality audits.
*   **Pull Requests Rules:** Merging requires passing local linting checks, completing test suites, and receiving approval from at least one senior reviewer.

---

## 28. Release Management

*   **Semantic Versioning:** Releases must use semantic versioning structures (`vMAJOR.MINOR.PATCH`).
*   **Release Approvals:** Merging to the `main` branch requires approval from the Lead Developer and Product Owner.
*   **Deployment Schedules:** Releases are scheduled and deployed during off-peak hours to minimize user disruption.

---

## 29. Queue & Background Job Deployment

*   **Asynchronous Queues:** Redis handles task scheduling, routing heavy operations asynchronously to background workers:
    *   *Payment Processing:* RazorpayX disbursements.
    *   *Notification Delivery:* In-app and SMS alerts.
    *   *Analytics Aggregation:* Precalculated analytical snapshots.
    *   *Report Generation:* PDF and CSV exports.
*   **Worker Strategy:** Systemd processes execute background workers, scaling worker counts based on queue loads.

---

## 30. Database Maintenance

*   **Vacuum Strategy:** Database vacuum operations run automatically weekly during off-peak hours to optimize indexes.
*   **Index Maintenance:** Rebuild database indexes periodically to keep database query performance high.
*   **Analytical aggregates:** Precalculated snapshots avoid real-time query bottlenecks, ensuring fast dashboard load times.

---

## 31. Performance Optimization

*   **Frontend Optimization:** Compiles frontend resources into optimized, light-weight bundles to ensure fast mobile page loads.
*   **Backend Optimization:** Gunicorn process managers run Uvicorn worker pools to execute backend routes asynchronously.
*   **Database Optimization:** Frequently queried columns are optimized using B-Tree indexes, and dashboard aggregates read from precalculated snapshot tables.

---

## 32. Scalability Planning

*   **Horizontal Scalability:** Keep the FastAPI backend stateless, allowing developers to scale instances horizontally behind a load balancer.
*   **PgBouncer Pool Managers:** Manage database connections using PgBouncer, preventing backend processes from exhausting connection pools.
*   **Asynchronous Processing:** Asynchronous background queues process heavy tasks, avoiding request bottlenecks.

---

## 33. Audit Compliance

*   **Access Rules:** Audit logs are visible only to Admins and Developers through read-only portals.
*   **Log Retention:** Logs are retained for $7\text{ years}$ to meet compliance and performance reporting standards.
*   **Immutability:** The database blocks `UPDATE` and `DELETE` queries targeting `audit_logs`, keeping records immutable.

---

## 34. Security Incident Response

*   **Threat Detection:** Consecutively failed logins trigger security alerts.
*   **Incident Isolation:** The system locks the affected account, blocking access attempts.
*   **Incident Containment:** Developers review incident details on security logs to determine the threat source, blocking the offending IP.

---

## 35. Production Monitoring Dashboard

*   **Metrics Grid:** Exposes platform diagnostics (active connection pools, API latency, CPU load).
*   **System Health Alerts:** Displays database connectivity status and warning indicators.

---

## 36. Deployment Validation Checklist

Before launching, verify all items on this validation checklist are completed:

*   [ ] **Infrastructure Vetting:** Confirm all port blocks are configured and NGINX redirects HTTP traffic successfully.
*   [ ] **Application Vetting:** Confirm environment secrets are loaded securely from external environments.
*   [ ] **Database Vetting:** Verify database instances run locally and PgBouncer pool managers are active.
*   [ ] **Security Vetting:** Verify all passwords hash using Argon2id and PII columns are encrypted.
*   [ ] **Monitoring Vetting:** Verify Prometheus/Grafana dashboards capture server metrics and Sentry integrations are active.
*   [ ] **Backup Vetting:** Confirm backup cron jobs run daily and restore validation tests are successful.

---

## 37. Production Readiness Checklist

*   [ ] **Security Audit:** Confirm SSL certificates are active, enforcing secure HTTPS traffic.
*   [ ] **Performance Audit:** Verify initial bundle sizes are optimized and dashboard load times are under $2\text{ seconds}$.
*   [ ] **Testing Audit:** Confirm core unit and integration test coverage exceeds $85\%$.
*   [ ] **Backup Audit:** Verify backups are encrypted and stored in independent, secure off-site cloud storage.
*   [ ] **Monitoring Audit:** Confirm crash integration alerts are routed successfully to Sentry.

---

## 38. Skill India Deployment Expansion (Phase 2)

*   **Future Infrastructure:** Add dedicated worker containers to handle online testing and certification processing.
*   **Compatibility Strategy:** Integrate Phase 2 tables and services under `/api/v1/skills/*`, avoiding schema conflicts with Phase 1 configurations.

---

## 39. Clean India Deployment Expansion (Phase 3)

*   **Future Infrastructure:** Add geocoded tracking pipelines to handle regional logistics and processing plants data.
*   **Compatibility Strategy:** Integrate logistics and processing services under `/api/v1/clean/*`, avoiding conflicts with Phase 1 networks.

---

## 40. Long-Term Operations Plan

*   **Year 1 (Stability):** Focus on stabilizing pilot operations, optimizing database queries, and refining waste verification turnaround queues.
*   **Year 2 (Mobile Apps):** Integrate Phase 2 (Skill India) modules and develop native mobile applications.
*   **Year 3 (National Expansion):** Launch Phase 3 (Clean India) environmental operations, integrate automated payment APIs, and expand services nationally.

---

## 41. Conclusion

This Deployment Specification Document (`10_DEPLOYMENT_SPECIFICATION.md`) establishes the absolute infrastructure architecture, deployment pipelines, hosting profiles, backup crons, disaster recovery coordinates, and monitoring models for the Athiyaman Platform - Digital India Phase 1. By detailing server configurations, NGINX setups, DirectAdmin directories, and database parameters, it serves as a complete technical guide for DevOps engineers, ensuring a secure, reliable, and scalable production deployment.
