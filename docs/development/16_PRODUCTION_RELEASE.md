# Athiyaman Platform - Production Release Document
## Phase 1 – Digital India Production Launch & Release Runbooks

---

## 1. Release Objectives

This Production Release Document defines the production launch criteria, feature completion checklists, approval processes, go-live procedures, post-release monitoring workflows, and incident response runbooks for the Athiyaman Platform - Digital India Phase 1. It acts as the official release guide for engineering and operational teams during the launch.

*   **Launch Goals:**
    *   *Zero Downtime:* Ensure seamless backend deployments and static asset CDN updates.
    *   *Secure PII Management:* Enforce AES-256 rest-encryption for Aadhaar and bank details.
    *   *System Reliability:* Confirm PgBouncer pools and Celery background workers are active.
    *   *Complete Audit Trails:* Verify audit log triggers block updates and deletions natively.

---

## 2. Release Criteria

To authorize the production release of Phase 1, the platform must meet six strict release criteria:

```
┌────────────────────────────────────────────────────────┐
│             1. Code Vetting & linting                  │
├────────────────────────────────────────────────────────┤
│             2. Complete Test Coverage (>85%)           │
├────────────────────────────────────────────────────────┤
│             3. Security Vetting & PII Checks           │
├────────────────────────────────────────────────────────┤
│             4. Database Migrations Validations         │
├────────────────────────────────────────────────────────┤
│             5. System Load Capacity Audits             │
├────────────────────────────────────────────────────────┤
│             6. Operational Vetting Sign-Offs           │
└────────────────────────────────────────────────────────┘
```

*   **Code Quality:** All scripts must pass strict linter and static analysis checks (TypeScript strict mode, Ruff style compliance).
*   **Test Coverage:** Test coverage for core business services and database migrations must exceed $85\%$.
*   **Security Audits:** The platform must record zero open high-priority security vulnerabilities in dependency scans.
*   **Data Integrity:** Verify database constraints, indexes, and write triggers successfully protect data.
*   **System Performance:** Confirm API response latencies remain under $500\text{ms}$ under load.
*   **Operational Readiness:** Admins and support teams must receive complete training on operational queues.

---

## 3. Feature Completion Checklist

Verify that all Phase 1 features are completed and ready for release:

- [ ] **Authentication Module:** Complete OTP-based logins, JWT token generation, refresh tokens, and password reset flows.
- [ ] **Profiles Module:** Verified biographical, address, Aadhaar, nominee, and banking input forms.
- [ ] **Teams Module:** Active unique team codes, rosters lists, and leader capacity constraints.
- [ ] **Referrals Module:** Vetted `LEADER_REFERRAL` (single-use) and `TEAM_REFERRAL` (multi-use) code generators.
- [ ] **Level Progression:** Automated level calculation logic for Team Levels 1–6 and Personal Levels 7–11.
- [ ] **Waste Registry:** Complete waste submission, photo upload, geocoded map integration, and verification queue features.
- [ ] **Collection Centers:** Active geocoded center locator registry.
- [ ] **Claims Module:** Milestone-based reward claim requests.
- [ ] **Payment Ledger:** Completed manual payout processing registries.

---

## 4. Security Approval Checklist

- [ ] **PII Protection:** Verify Aadhaar and bank account columns are encrypted at rest using AES-256.
- [ ] **Aadhaar Duplicate Check:** Verify cryptographic hashing checks in `aadhaar_hash` detect duplicate accounts.
- [ ] **Data Masking:** Confirm PII fields are masked on dashboards (`XXXX-XXXX-1234` for Aadhaar, `XXXXXX4589` for bank).
- [ ] **Upload Protection:** Verify file validation rules check file signatures and restrict uploads to secure types.
- [ ] **Access Controls:** Confirm route protection guards block unprivileged access attempts.
- [ ] **Rate Limiting:** Verify API gateway rate limiters are active.

---

## 5. Database Approval Checklist

- [ ] **Schema Migration:** Confirm Alembic migration scripts run successfully without errors.
- [ ] **Relational Keys:** Verify foreign keys are active with `ON DELETE RESTRICT` constraints.
- [ ] **Default UUIDv7 Keys:** Verify primary keys in transactional tables default to `generate_uuid_v7()`.
- [ ] **Audit Trail Immutability:** Verify trigger functions block UPDATE and DELETE queries on audit logs.
- [ ] **Member Counter Strategy:** Confirm team rosters use precalculated `member_count` to optimize queries.

---

## 6. Backend Approval Checklist

- [ ] **Systemd Configuration:** Verify FastAPI application runs under system virtual environments managed by Gunicorn.
- [ ] **Environment Configuration:** Verify all secrets are loaded from secure `.env` files.
- [ ] **Exception Interception:** Confirm API error handlers capture database failures and return standard JSON payloads.
- [ ] **Background Queues:** Verify Celery worker pools and Redis queues process tasks successfully.

---

## 7. Frontend Approval Checklist

- [ ] **React Bundle:** Confirm frontend build processes compile static assets successfully.
- [ ] **Axios Interceptors:** Verify interceptors handle expired access tokens and renew sessions automatically.
- [ ] **Protected Routes:** Verify route guards protect dashboards, redirecting unauthorized traffic.
- [ ] **Form Validations:** Confirm all input fields validate data before submissions.
- [ ] **Theme Consistency:** Verify layout styling meets government-style theme rules.

---

## 8. Testing Approval Checklist

- [ ] **Logic Testing:** Confirm Pytest unit tests validate core business services successfully.
- [ ] **Endpoint Testing:** Verify API integration tests check all routes and schemas.
- [ ] **Security Testing:** Confirm automated scripts verify role restrictions.
- [ ] **Performance Testing:** Confirm dashboard load times are under $2\text{ seconds}$ on standard mobile connections.
- [ ] **UAT Validation:** Confirm Playwright browser tests validate citizen journeys successfully.

---

## 9. Deployment Approval Checklist

- [ ] **Port Security:** Confirm UFW firewall rules allow incoming traffic only on secure ports ($80$, $443$, $22$).
- [ ] **SSL Certification:** Verify Let's Encrypt certificates are active, enforcing secure HTTPS connections.
- [ ] **NGINX Proxy:** Verify NGINX reverse proxies route static files and API requests successfully.
- [ ] **DirectAdmin Layout:** Confirm static assets and backend virtual directories are mapped correctly.

---

## 10. Monitoring Approval Checklist

- [ ] **Grafana Dashboard:** Verify server diagnostics capture CPU, memory, and database metrics.
- [ ] **Error Tracking:** Confirm crash integration alerts route successfully to Sentry.
- [ ] **Alerting Adaptability:** Verify critical alerts route successfully to developers via WhatsApp.

---

## 11. Backup Approval Checklist

- [ ] **Scheduled Backups:** Confirm daily full backups and hourly WAL logs are active.
- [ ] **Off-site Storage:** Verify backups are encrypted and stored in independent, secure off-site cloud storage.
- [ ] **Restore Testing:** Confirm restore validation tests run successfully, verifying backup integrity.

---

## 12. Go-Live Process

Perform the following operations in sequence during the scheduled maintenance window:

```
┌────────────────────────────────────────────────────────┐
│           Step 1: Maintenance Banner Activation        │
├────────────────────────────────────────────────────────┤
│           Step 2: Database Migration Run               │
├────────────────────────────────────────────────────────┤
│           Step 3: Backend Process Upgrades             │
├────────────────────────────────────────────────────────┤
│           Step 4: Static CDN Builds Push               │
├────────────────────────────────────────────────────────┤
│          Step 5: Health Check & Access Tests           │
├────────────────────────────────────────────────────────┤
│           Step 6: Maintenance Banner Removal           │
└────────────────────────────────────────────────────────┘
```

1.  **Maintenance Banner Activation:** Enable static maintenance banners on NGINX proxies, redirecting incoming traffic to offline pages.
2.  **Database Migration Run:** Run Alembic migration scripts to upgrade production database schemas sequentially.
3.  **Backend Process Upgrades:** Deploy backend application updates and restart Systemd services.
4.  **Static CDN Builds Push:** Deploy compiled frontend assets to static delivery networks.
5.  **Health Check & Access Tests:** Run API connectivity checks and verify role restrictions.
6.  **Maintenance Banner Removal:** Disable maintenance banners on NGINX, routing live traffic to the production application.

---

## 13. Post-Release Monitoring

During the first $72\text{ hours}$ post-launch, monitor the following diagnostic metrics:

*   **API Response Speeds:** Confirm standard endpoint response latencies stay below $500\text{ms}$.
*   **Error Rates:** Sentry logs must record zero high-priority application failures or coding exceptions.
*   **Database connection pools:** Verify active connection counts stay below PgBouncer pool limits.
*   **Background task delivery:** Confirm Redis workers process queued background tasks successfully.

---

## 14. Incident Handling Runbook

If a critical incident occurs post-launch, follow these containment steps:

*   **Detection:** Automated diagnostics logs identify connection failures, high API latency, or security exceptions.
*   **Investigation:** Lead Developer reviews application logs and Sentry alerts to identify the crash source.
*   **Incident Containment:**
    *   *Security Threat:* Block the offending IP, lock affected accounts, and audit PII logs.
    *   *Database Outage:* Run database restoration procedures using WAL WAL logs.
*   **System rollback:** If updates introduce critical bugs, trigger rollback procedures to revert system services.
*   **Post-Incident Review:** Document the crash source, analyze system impacts, and define prevention measures.

---

## 15. First 30 Days Operational Plan

*   **Phase 1 Stability:** Monitor waste verification queues, targeting average review turnaround times of under $24\text{ hours}$.
*   **Payout Audits:** Audit claim queues daily to ensure payouts are processed within $48\text{ hours}$.
*   **System Maintenance:** Vacuum databases weekly to optimize indexes and keep query performance high.
*   **Performance Reviews:** Review server diagnostics to identify and resolve query bottlenecks.

---

## 16. Future Roadmap

*   **Phase 2 - Skill India:** Integrate course catalogs, trainer dashboards, attendance trackers, assessments, and certifications.
*   **Phase 3 - Clean India:** Scale environmental operations by integrating regional waste processing plants and transport logs.
*   **Mobile Applications:** Develop native mobile applications using API gateways optimized for low-bandwidth mobile environments.
*   **Financial Integrations:** Link direct UPI payouts and automated banking payment APIs.

---

## 17. Release Sign-Off

To authorize the production launch, all product owners and engineering leads must sign off on this release document:

```
Lead Developer Sign-Off:    _______________________   Date: ______________
Quality Assurance Sign-Off:  _______________________   Date: ______________
DevOps Engineer Sign-Off:   _______________________   Date: ______________
Product Owner Sign-Off:     _______________________   Date: ______________
```

---

## 18. Conclusion

This Production Release Document (`16_PRODUCTION_RELEASE.md`) establishes the absolute launch criteria, feature completion checklists, approvals, go-live steps, post-release monitoring workflows, and incident response runbooks for the Athiyaman Platform - Digital India Phase 1. By detailing approvals across all tiers and providing structured launch procedures, it serves as a complete technical guide for release teams, ensuring a secure, reliable, and successful production deployment.
