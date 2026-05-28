# Athiyaman Platform - Testing Implementation Document
## Phase 1 – Digital India Comprehensive Quality Assurance & Testing Standards

---

## 1. Testing Philosophy

The Athiyaman Platform’s testing philosophy enforces high technical standards, prioritizing code stability, data integrity, and strict security validation over visual polish.

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

*   **Logic Isolation:** Core business logic and validations (such as level updates and referral checks) must be fully validated using automated unit tests before integration.
*   **Decoupled Vetting:** Test scripts must mock database connections and API networks during unit tests, keeping tests lightweight and fast-running.
*   **Security Hardening:** Every non-public API endpoint must be tested against unauthorized access attempts, confirming that unprivileged users receive `403 Forbidden` responses.
*   **Quality Benchmarks:** Target a test coverage threshold of $>85\%$ for all core business workflows, making test suites mandatory in CI/CD build pipelines.

---

## 2. Unit Testing

*   **Backend Pytest Guidelines:** Unit tests are executed using **Pytest**. We use mock database sessions to validate helper functions and service class metrics:
    ```python
    # Example unit test for profile completion scoring logic
    from app.modules.profiles.service import calculate_completion_percentage
    
    def test_calculate_completion_percentage_empty():
        payload = {}
        score = calculate_completion_percentage(payload)
        assert score == 0
        
    def test_calculate_completion_percentage_complete():
        payload = {
            "full_name": "Ramesh Kumar",
            "email": "ramesh@email.com",
            "phone_number": "9842101234",
            "aadhaar_encrypted": "encrypted_value",
            "bank_account_encrypted": "encrypted_value",
            "nominee_name": "Sita Kumar"
        }
        score = calculate_completion_percentage(payload)
        assert score == 100
    ```
*   **Frontend Vitest Guidelines:** Renders visual components inside **Vitest** testing workspaces, validating prop types, formatting utilities, and UI layout components.

---

## 3. Integration Testing

*   **Database Transaction Verification:** Integration tests validate full database-to-endpoint integrations, verifying that multiple tables update correctly in a single transaction.
*   **Test Suite Integration Code:**
    ```python
    import pytest
    from sqlalchemy import create_session
    from app.modules.teams.service import TeamService
    
    def test_team_creation_transactional_flow(db_session):
        service = TeamService(db_session)
        
        # 1. Create team record in transaction
        team = service.create_new_team(
            leader_id="leader_uuid_string",
            team_name="Athiyaman Madurai West",
            district="Madurai",
            area="West Ward",
            pincode="625001"
        )
        
        # 2. Verify team was successfully created
        assert team.team_code is not None
        assert team.member_count == 0
    ```

---

## 4. API Testing

*   **REST Endpoint Validations:** Automated API tests invoke endpoints using Mock clients, verifying Pydantic request inputs and response schemas:
    ```python
    def test_create_team_api_validation(client):
        # Submitting duplicate team name payload
        response = client.post("/api/v1/teams", json={
            "team_name": "Duplicate Team Name",
            "district": "Madurai",
            "area": "West Ward",
            "pincode": "625001"
        })
        assert response.status_code == 400
        assert response.json()["detail"] == "DUPLICATE_TEAM_NAME"
    ```

---

## 5. Authentication Testing

*   **Session Access Validations:** Automated test scripts verify credentials verification, check password hashing, and test JWT token issuance and cookie settings.
*   **OTP Challenges Testing:** Verifies that signup endpoints reject expired or invalid OTP codes, and tests that lockout triggers block IPs after consecutive failed logins.

---

## 6. Referral Testing

*   **Referral Code Validations:** Tests verify code generation limits, validate codes against database constraints, and confirm invite usage capacities:
    *   *Leader Codes:* Confirm codes are single-use and expire after $48\text{ hours}$.
    *   *Team Codes:* Verify codes are multi-use and expire when levels are completed.

---

## 7. Team Testing

*   **Relational Database Validations:** Tests verify *One Leader = One Team* constraints, check team name uniqueness, and validate member roster additions.
*   **Roster Updates Verification:** Confirm that joining members increment team member counts, and leaving members decrement counts dynamically.

---

## 8. Waste Testing

*   **Waste Log Validations:** Tests check input bounds (weights locked between $0.1$ and $50.0\text{ KG}$), verify geocodes, check photo uploads, and validate status transitions.
*   **State History Logs:** Confirms that all review actions write logs to `waste_status_history`, updating progress weights dynamically upon approval.

---

## 9. Claim Testing

*   **Level Milestone Validations:** Tests verify that claims can only be submitted once the progression engine marks a level as completed.
*   **Duplicate Claim Prevention:** Confirms that the backend blocks attempts to submit secondary claims for a level while a payout request is pending.

---

## 10. Payment Testing

*   **Disbursement Records Validations:** Tests check the Payment Queue routing, verify manual payment logging, and confirm bank transaction reference entries.
*   **Payment Failure Recoveries:** Confirms that failed transfers return claims to the Payment Queue, lock payouts, and notify the user to correct bank details.

---

## 11. Admin Testing

*   **Vetting Queue Operations:** Tests verify that Admins can review leader applications, audit documents, verify waste records, and approve claims using dashboard queues.
*   **Database Mutating Rules:** Confirms that Admins are blocked from mutating raw database tables directly, logging all dashboard actions in the audit trail.

---

## 12. Developer Testing

*   **Technical Controls Verification:** Tests verify system status metrics, log exploration queries, backup creations, and feature flag toggles.
*   **Diagnostics Diagnostics:** Confirms that feature toggles change application parameters instantly without requiring code deploys.

---

## 13. Security Testing

Verify endpoint permissions dynamically by parsing JWT role payloads at the router layer:

```python
def test_rbac_endpoint_access_guards(client):
    # Standard Member attempting to access Admin endpoints
    member_headers = {"Authorization": "Bearer member_jwt_token_string"}
    response = client.get("/api/v1/admin/users", headers=member_headers)
    assert response.status_code == 403
    assert response.json()["detail"] == "INSUFFICIENT_PERMISSIONS"
```

---

## 14. Performance Testing

*   **API Response Targets:** Verify that standard endpoint response times maintain latency limits of less than $500\text{ms}$.
*   **Client Loading Metrics:** Confirm that dashboard assets load in under $2\text{ seconds}$ on standard mobile connections.
*   **Database Query Optimization:** Verify that B-Tree indexes optimize query speeds and analytical dashboards fetch precalculated snapshots.

---

## 15. Load Testing

*   **Concurrent Traffic Audits:** Simulate concurrent user actions (e.g., $10,000$ active connections) using Locust testing tools, validating that database pool managers handle traffic loads cleanly.
*   **Server Limits Checks:** Confirms that API latency stays below $500\text{ms}$ under load, checking that Redis queue workers process background tasks successfully.

---

## 16. Regression Testing

*   **Automated Regression Suites:** Automated regression tests run on all pull requests, confirming that database migration schema updates do not break existing business logic.
*   **CI/CD Pipeline Integration:** Regression test suites must run and pass successfully in build pipelines before code merges to integration branches.

---

## 17. UAT Testing

*   **End-to-End Citizen Journeys:** Browser automation scripts (Cypress/Playwright) simulate complete user workflows, verifying layout responsiveness and accessibility.
*   **Roster Flows Verification:** Rerun complete journeys (Visitor signup $\rightarrow$ Profile completion $\rightarrow$ Rules acceptance $\rightarrow$ Waste logging $\rightarrow$ Claim processing $\rightarrow$ Payment settlement) to confirm system integrity.

---

## 18. Test Data Strategy

*   **Data Seed Engines:** Database migration scripts seed mock datasets (reference levels, collection centers, mock users, active teams) during testing setups:
    ```sql
    -- Standard seed inserts for Level configurations
    INSERT INTO levels (level_number, requirement_type, requirement_value, reward_amount)
    VALUES 
        (1, 'MEMBERS', 10, 100.00),
        (2, 'MEMBERS', 90, 1000.00),
        (7, 'WASTE_KG', 10, 10000.00);
    ```
*   **Test Data Cleanup:** Test suites use database rollbacks to wipe mock data records post-execution, keeping test databases clean.

---

## 19. Test Environment Strategy

*   **Sandbox Isolation:** Automated test suites run inside isolated testing environments, using temporary SQLite or PostgreSQL test databases.
*   **Secrets Isolation:** Test scripts load mock keys from custom `.env.test` files, keeping real production credentials secure.

---

## 20. Production Validation Checklist

Before launching Phase 1, ensure all items on this validation checklist are completed:

*   [ ] **Infrastructure Vetting:** Confirm all port blocks are configured and NGINX redirects HTTP traffic successfully.
*   [ ] **API Endpoint Vetting:** Verify all endpoint tests pass successfully and input schemas check values.
*   [ ] **Database Vetting:** Confirm PostgreSQL schemas are migrated successfully and PgBouncer pool managers are active.
*   [ ] **Security Vetting:** Confirm passwords hash using Argon2id and PII columns are encrypted.
*   [ ] **Monitoring Vetting:** Verify Prometheus/Grafana dashboards capture server metrics and Sentry integrations are active.
*   [ ] **Backup Vetting:** Confirm backup cron jobs run daily and restore validation tests are successful.

---

## 21. Conclusion

This Testing Implementation Document (`14_TESTING_IMPLEMENTATION.md`) establishes the absolute quality benchmarks, testing suites, test data strategies, environments configurations, and production validation checklists for the Athiyaman Platform – Digital India Phase 1. By detailing test architectures and providing complete SQL and Python snippets, it serves as a complete testing manual for QA and backend engineering teams. All code changes, database migrations, and release builds must pass these tests, ensuring the platform remains highly secure, performance-optimized, and traceable over its lifecycle.
