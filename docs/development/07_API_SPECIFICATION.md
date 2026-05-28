# Athiyaman Platform - API Specification Document
## Phase 1 – Digital India Comprehensive API Contracts & Specifications

---

## 1. API Overview

This document defines the REST API Specification and Contracts for the Athiyaman Platform - Digital India Phase 1. It details the endpoints, request/response models, input validations, and security controls to ensure frontend and backend teams can work independently.

*   **Purpose:** To establish a secure, stateless, and strongly typed communication bridge between client interfaces and server services.
*   **Goals:**
    *   *System Modularity:* Pure REST interfaces decoupled from underlying implementations.
    *   *Type Safety:* Enforces validation contracts at the input and output levels.
    *   *Secure Session Handlers:* Implements stateless JWT access and secure HTTP-only refresh cookies.
*   **Architecture:** Decoupled routes leveraging FastAPI ASGI asynchronous engines, executing validations via Pydantic schemas.
*   **REST Standards:** Standardizes operations using standard HTTP methods (`GET`, `POST`, `PUT`, `DELETE`), custom error codes, and standardized payloads.
*   **Versioning Strategy:** Uses URL prefixes (e.g., `/api/v1/*`) to support seamless future API updates.

---

## 2. API Standards

*   **Base URL:**
    *   *Local Dev:* `http://localhost:8000/api/v1`
    *   *Production:* `https://api.athiyaman.in/api/v1`
*   **HTTP Methods Usage:**
    *   `GET`: Fetch resources. Safe and idempotent.
    *   `POST`: Create new resources or perform security operations (e.g., Login).
    *   `PUT`: Update existing resources.
    *   `DELETE`: Disable or soft-delete resources.
*   **Response Format:** Communicates using UTF-8 JSON payloads.
*   **Error Layout:** Standardizes API error structures across all modules:
    ```json
    {
      "detail": {
        "code": "ERROR_CODE_STRING",
        "message": "User-friendly description of the error."
      }
    }
    ```
*   **Performance Requirements:** All REST API endpoints must maintain latency limits of less than **500 ms**. Citizen and Admin dashboards must load in less than **2 seconds**, and search queries must complete in less than **1 second** under concurrent loads.
*   **HTTP Status Codes:** Standardizes responses using appropriate HTTP codes:
    *   `200 OK`: Successful fetch or update operations.
    *   `201 Created`: Successful resource creation.
    *   `400 Bad Request`: Validation failures or business constraint violations.
    *   `401 Unauthorized`: Invalid or expired authorization tokens.
    *   `403 Forbidden`: Insufficient user role permissions.
    *   `404 Not Found`: Resource does not exist in the database.
    *   `422 Unprocessable Entity`: Schema format exceptions.
    *   `429 Too Many Requests`: Triggered by rate-limiting rules.
    *   `500 Internal Error`: Database issues or unexpected exceptions.
*   **Authentication Requirements:** Non-public APIs require JWT access tokens in the HTTP Authorization header:
    ```http
    Authorization: Bearer <JWT_ACCESS_TOKEN>
    ```

---

## 3. Authentication APIs

### 3.1 Login
*   **Method & URL:** `POST /auth/login`
*   **Request Headers:** `Content-Type: application/json`
*   **Request Body:**
    ```json
    {
      "username": "santhosh",
      "password": "Password@123"
    }
    ```
*   **Success Response:**
    *   *Status Code:* `200 OK`
    *   *Set-Cookie Header:* `refresh_token=<JWT_REFRESH_TOKEN>; HttpOnly; Secure; SameSite=Strict; Path=/api/v1/auth/refresh`
    *   *Response Payload:*
        ```json
        {
          "access_token": "jwt_access_token_string",
          "expires_in": 900,
          "role": "LEADER"
        }
        ```
*   **Validation Rules:** Username must be alphanumeric. Password must meet complexity requirements.
*   **Permissions:** Public access (`VISITOR`).
*   **Error Responses:**
    *   *401 Unauthorized:* `"INVALID_CREDENTIALS"`
    *   *403 Forbidden:* `"ACCOUNT_SUSPENDED"`

### 3.2 Logout
*   **Method & URL:** `POST /auth/logout`
*   **Request Headers:** `Authorization: Bearer <JWT_ACCESS_TOKEN>`
*   **Response Body:**
    *   *Status Code:* `200 OK`
    *   *Set-Cookie Header:* `refresh_token=; HttpOnly; Secure; SameSite=Strict; Path=/api/v1/auth/refresh; Max-Age=0`
    *   *Response Payload:*
        ```json
        {
          "message": "Session invalidated successfully."
        }
        ```
*   **Permissions:** Authenticated users (`MEMBER`, `LEADER`, `ADMIN`, `DEVELOPER`).

### 3.3 Refresh Token
*   **Method & URL:** `POST /auth/refresh`
*   **Request Headers:** Requires the `refresh_token` in HTTP-only cookies.
*   **Success Response:**
    *   *Status Code:* `200 OK`
    *   *Response Payload:*
        ```json
        {
          "access_token": "new_jwt_access_token_string",
          "expires_in": 900
        }
        ```
*   **Permissions:** Public access, but requires a valid refresh cookie.

### 3.4 Forgot Password
*   **Method & URL:** `POST /auth/forgot-password`
*   **Request Body:**
    ```json
    {
      "phone_number": "9842101234"
    }
    ```
*   **Success Response:**
    *   *Status Code:* `200 OK`
    *   *Response Payload:*
        ```json
        {
          "message": "Verification OTP sent successfully.",
          "session_id": "session_uuid_string"
        }
        ```
*   **Permissions:** Public access.

### 3.5 Reset Password
*   **Method & URL:** `POST /auth/reset-password`
*   **Request Body:**
    ```json
    {
      "session_id": "session_uuid_string",
      "otp_code": "123456",
      "new_password": "NewSecure@Password123"
    }
    ```
*   **Success Response:**
    *   *Status Code:* `200 OK`
    *   *Response Payload:*
        ```json
        {
          "message": "Password updated successfully."
        }
        ```
*   **Permissions:** Public access.

### 3.6 OTP Verification
*   **Method & URL:** `POST /auth/verify-otp`
*   **Request Body:**
    ```json
    {
      "phone_number": "9842101234",
      "otp_code": "123456"
    }
    ```
*   **Success Response:**
    *   *Status Code:* `200 OK`
    *   *Response Payload:*
        ```json
        {
          "message": "Mobile verified successfully."
        }
        ```
*   **Permissions:** Public access.

### 3.7 Session Validation
*   **Method & URL:** `GET /auth/session`
*   **Request Headers:** `Authorization: Bearer <JWT_ACCESS_TOKEN>`
*   **Success Response:**
    *   *Status Code:* `200 OK`
    *   *Response Payload:*
        ```json
        {
          "user_id": "user_uuid_string",
          "role": "LEADER",
          "profile_complete": true
        }
        ```
*   **Permissions:** Authenticated users.

---

## 4. User APIs

### 4.1 Get Profile
*   **Method & URL:** `GET /user/profile`
*   **Request Headers:** `Authorization: Bearer <JWT_ACCESS_TOKEN>`
*   **Success Response:**
    *   *Status Code:* `200 OK`
    *   *Response Payload:*
        ```json
        {
          "full_name": "Ramesh Kumar",
          "email": "ramesh@email.com",
          "phone_number": "9842101234",
          "aadhaar_encrypted": "XXXX-XXXX-1234",
          "bank_account_encrypted": "XXXXXX4589",
          "address": "123 Main Street, Madurai",
          "profile_completion": 100,
          "is_verified": true
        }
        ```
*   **Permissions:** Authenticated users.

### 4.2 Update Profile
*   **Method & URL:** `PUT /user/profile`
*   **Request Headers:** `Authorization: Bearer <JWT_ACCESS_TOKEN>`
*   **Request Body:**
    ```json
    {
      "email": "ramesh.new@email.com",
      "phone_number": "9842101234",
      "address": "456 Side Street, Madurai"
    }
    ```
*   **Success Response:**
    *   *Status Code:* `200 OK`
*   **Validation Rules:** E-mail format must be valid. Phone numbers must contain exactly $10$ digits.
*   **Permissions:** Authenticated users.

### 4.3 Change Password
*   **Method & URL:** `POST /user/change-password`
*   **Request Headers:** `Authorization: Bearer <JWT_ACCESS_TOKEN>`
*   **Request Body:**
    ```json
    {
      "current_password": "Password@123",
      "new_password": "NewSecure@Password123"
    }
    ```
*   **Success Response:**
    *   *Status Code:* `200 OK`
*   **Permissions:** Authenticated users.

---

## 5. Leader Application APIs

### 5.1 Create Application
*   **Method & URL:** `POST /applications`
*   **Request Body:**
    ```json
    {
      "full_name": "K. Arumugam",
      "phone": "9842101234",
      "email": "aru@email.com",
      "aadhaar_number": "123456789012",
      "district": "Madurai",
      "pincode": "625001",
      "address": "123 Street Name, Madurai",
      "reason": "I want to coordinate local teams to improve environmental sanitation."
    }
    ```
*   **Success Response:**
    *   *Status Code:* `201 Created`
    *   *Response Payload:*
        ```json
        {
          "application_id": "app_uuid_string",
          "status": "PENDING",
          "message": "Application submitted successfully."
        }
        ```
*   **Validation Rules:** Enforces strict formatting rules: Aadhaar ($12$ digits), Phone ($10$ digits), and Pincode ($6$ digits).
*   **Permissions:** Public access (`VISITOR`).

### 5.2 View Application
*   **Method & URL:** `GET /applications/{id}`
*   **Success Response:**
    *   *Status Code:* `200 OK`
*   **Permissions:** Authenticated Admins.

---

## 6. Team APIs

### 6.1 Create Team
*   **Method & URL:** `POST /teams`
*   **Request Headers:** `Authorization: Bearer <JWT_ACCESS_TOKEN>`
*   **Request Body:**
    ```json
    {
      "team_name": "Athiyaman Madurai East",
      "district": "Madurai",
      "area": "East Ward",
      "pincode": "625001"
    }
    ```
*   **Success Response:**
    *   *Status Code:* `201 Created`
    *   *Response Payload:*
        ```json
        {
          "team_id": "team_uuid_string",
          "team_code": "ATH-MAD-EAST",
          "status": "ACTIVE"
        }
        ```
*   **Validation Rules:** Team name must be globally unique across the platform.
*   **Permissions:** Authenticated Leaders (`LEADER`).

### 6.2 View Team
*   **Method & URL:** `GET /teams/{id}`
*   **Request Headers:** `Authorization: Bearer <JWT_ACCESS_TOKEN>`
*   **Success Response:**
    *   *Status Code:* `200 OK`
*   **Permissions:** Authenticated users linked to the team.

### 6.3 View Team Members
*   **Method & URL:** `GET /teams/{id}/members`
*   **Request Headers:** `Authorization: Bearer <JWT_ACCESS_TOKEN>`
*   **Success Response:**
    *   *Status Code:* `200 OK`
*   **Permissions:** Team Leaders or Admins.

---

## 7. Member APIs

### 7.1 View Team Details
*   **Method & URL:** `GET /member/team`
*   **Request Headers:** `Authorization: Bearer <JWT_ACCESS_TOKEN>`
*   **Success Response:**
    *   *Status Code:* `200 OK`
*   **Permissions:** Authenticated Members (`MEMBER`).

### 7.2 View Leader Details
*   **Method & URL:** `GET /member/team/leader`
*   **Request Headers:** `Authorization: Bearer <JWT_ACCESS_TOKEN>`
*   **Success Response:**
    *   *Status Code:* `200 OK`
*   **Permissions:** Authenticated Members.

---

## 8. Referral APIs

### 8.1 Generate Referral
*   **Method & URL:** `POST /referrals/generate`
*   **Request Headers:** `Authorization: Bearer <JWT_ACCESS_TOKEN>`
*   **Success Response:**
    *   *Status Code:* `201 Created`
    *   *Response Payload:*
        ```json
        {
          "referral_code": "REF-MAD-LEADER-98",
          "type": "TEAM_REFERRAL",
          "usage_limit": 10
        }
        ```
*   **Permissions:** Authenticated Leaders or Admins.

### 8.2 Validate Referral
*   **Method & URL:** `GET /referrals/validate?code=REF-MAD-LEADER-98`
*   **Success Response:**
    *   *Status Code:* `200 OK`
    *   *Response Payload:*
        ```json
        {
          "is_valid": true,
          "type": "TEAM_REFERRAL",
          "team_name": "Athiyaman Madurai East"
        }
        ```
*   **Permissions:** Public access.

---

## 9. Level APIs

### 9.1 View Team Levels
*   **Method & URL:** `GET /levels/team`
*   **Request Headers:** `Authorization: Bearer <JWT_ACCESS_TOKEN>`
*   **Success Response:**
    *   *Status Code:* `200 OK`
*   **Permissions:** Authenticated Leaders or Admins.

### 9.2 View Personal Levels
*   **Method & URL:** `GET /levels/personal`
*   **Request Headers:** `Authorization: Bearer <JWT_ACCESS_TOKEN>`
*   **Success Response:**
    *   *Status Code:* `200 OK`
*   **Permissions:** Authenticated users.

---

## 10. Waste APIs

### 10.1 Create Waste Record
*   **Method & URL:** `POST /waste`
*   **Request Headers:** `Authorization: Bearer <JWT_ACCESS_TOKEN>`
*   **Request Body:**
    ```json
    {
      "center_id": "center_uuid_string",
      "weight_kg": 12.5,
      "image_url": "https://storage.athiyaman.in/uploads/waste/photo_uuid.png",
      "collection_date": "2026-05-22"
    }
    ```
*   **Success Response:**
    *   *Status Code:* `201 Created`
    *   *Response Payload:*
        ```json
        {
          "record_id": "waste_uuid_string",
          "status": "PENDING_VERIFICATION"
        }
        ```
*   **Validation Rules:** Weight must range from $0.1$ to $50.0\text{ KG}$. Requires a valid collection center ID.
*   **Permissions:** Authenticated Members or Leaders.

### 10.2 View Waste Records
*   **Method & URL:** `GET /waste`
*   **Request Headers:** `Authorization: Bearer <JWT_ACCESS_TOKEN>`
*   **Success Response:**
    *   *Status Code:* `200 OK`
*   **Permissions:** Authenticated users.

---

## 11. Collection Center APIs

### 11.1 Search Centers
*   **Method & URL:** `GET /centers?pincode=625001`
*   **Success Response:**
    *   *Status Code:* `200 OK`
    *   *Response Payload:*
        ```json
        {
          "items": [
            {
              "id": "center_uuid_string",
              "center_name": "Madurai Center A",
              "address": "123 Main Street, Madurai",
              "pincode": "625001",
              "phone": "0452-123456"
            }
          ]
        }
        ```
*   **Permissions:** Public access.

---

## 12. Reward Claim APIs

### 12.1 Create Claim
*   **Method & URL:** `POST /rewards/claims`
*   **Request Headers:** `Authorization: Bearer <JWT_ACCESS_TOKEN>`
*   **Request Body:**
    ```json
    {
      "claim_type": "PERSONAL_REWARD",
      "level_number": 7
    }
    ```
*   **Success Response:**
    *   *Status Code:* `201 Created`
    *   *Response Payload:*
        ```json
        {
          "claim_id": "claim_uuid_string",
          "amount": 10000.00,
          "status": "PENDING_AUDIT"
        }
        ```
*   **Validation Rules:** Reaching the level milestone is required before claim creation. No second claim can be created while one is in `PENDING` state, preventing duplicate claims. Level progress is locked during claim review; new progress accumulated is stored separately in future level buckets.
*   **Permissions:** Authenticated Members or Leaders.

---

## 13. Payment APIs

### 13.1 View Payments
*   **Method & URL:** `GET /payments`
*   **Request Headers:** `Authorization: Bearer <JWT_ACCESS_TOKEN>`
*   **Success Response:**
    *   *Status Code:* `200 OK`
*   **Permissions:** Authenticated users.

---

## 14. Notification APIs

### 14.1 Get Notifications
*   **Method & URL:** `GET /notifications`
*   **Request Headers:** `Authorization: Bearer <JWT_ACCESS_TOKEN>`
*   **Success Response:**
    *   *Status Code:* `200 OK`
*   **Permissions:** Authenticated users.

### 14.2 Mark As Read
*   **Method & URL:** `PUT /notifications/{id}/read`
*   **Request Headers:** `Authorization: Bearer <JWT_ACCESS_TOKEN>`
*   **Success Response:**
    *   *Status Code:* `200 OK`
*   **Permissions:** Authenticated users.

---

## 15. Document APIs

### 15.1 Upload Document
*   **Method & URL:** `POST /documents/upload`
*   **Request Headers:** `Authorization: Bearer <JWT_ACCESS_TOKEN>`, `Content-Type: multipart/form-data`
*   **Request Body:** Requires document file parameters and document type variables (`AADHAAR` / `BANK_PROOF`).
*   **Success Response:**
    *   *Status Code:* `201 Created`
    *   *Response Payload:*
        ```json
        {
          "document_id": "doc_uuid_string",
          "file_url": "https://storage.athiyaman.in/uploads/docs/doc_uuid.pdf",
          "status": "PENDING"
        }
        ```
*   **Validation Rules:** Uploads must be valid PDF, PNG, or JPEG files (max $5\text{MB}$).
*   **Permissions:** Authenticated users.

---

## 16. Admin User Management APIs

### 16.1 View Users List
*   **Method & URL:** `GET /admin/users?page=1&limit=20`
*   **Request Headers:** `Authorization: Bearer <JWT_ACCESS_TOKEN>`
*   **Success Response:**
    *   *Status Code:* `200 OK`
*   **Permissions:** Authenticated Admins (`ADMIN`).

### 16.2 Suspend User
*   **Method & URL:** `POST /admin/users/{id}/suspend`
*   **Request Headers:** `Authorization: Bearer <JWT_ACCESS_TOKEN>`
*   **Success Response:**
    *   *Status Code:* `200 OK`
*   **Permissions:** Authenticated Admins.

---

## 17. Admin Team Management APIs

### 17.1 View Teams List
*   **Method & URL:** `GET /admin/teams?page=1&limit=20`
*   **Request Headers:** `Authorization: Bearer <JWT_ACCESS_TOKEN>`
*   **Success Response:**
    *   *Status Code:* `200 OK`
*   **Permissions:** Authenticated Admins.

---

## 18. Admin Referral APIs

### 18.1 View Referrals List
*   **Method & URL:** `GET /admin/referrals`
*   **Request Headers:** `Authorization: Bearer <JWT_ACCESS_TOKEN>`
*   **Success Response:**
    *   *Status Code:* `200 OK`
*   **Permissions:** Authenticated Admins.

---

## 19. Admin Waste Verification APIs

### 19.1 Approve Waste Record
*   **Method & URL:** `POST /admin/waste/{id}/approve`
*   **Request Headers:** `Authorization: Bearer <JWT_ACCESS_TOKEN>`
*   **Request Body:**
    ```json
    {
      "comments": "Photo weight verified against center database logs."
    }
    ```
*   **Success Response:**
    *   *Status Code:* `200 OK`
*   **Permissions:** Authenticated Admins.

### 19.2 Reject Waste Record
*   **Method & URL:** `POST /admin/waste/{id}/reject`
*   **Request Headers:** `Authorization: Bearer <JWT_ACCESS_TOKEN>`
*   **Request Body:**
    ```json
    {
      "comments": "The uploaded photo is blurry and does not display the weight readings."
    }
    ```
*   **Success Response:**
    *   *Status Code:* `200 OK`
*   **Permissions:** Authenticated Admins.

---

## 20. Admin Claim APIs

### 20.1 Approve Claim
*   **Method & URL:** `POST /admin/claims/{id}/approve`
*   **Request Headers:** `Authorization: Bearer <JWT_ACCESS_TOKEN>`
*   **Success Response:**
    *   *Status Code:* `200 OK`
*   **Permissions:** Authenticated Admins.

---

## 21. Admin Payment APIs

### 21.1 Process Payout
*   **Method & URL:** `POST /admin/payments/{id}/paid`
*   **Request Headers:** `Authorization: Bearer <JWT_ACCESS_TOKEN>`
*   **Request Body:**
    ```json
    {
      "transaction_reference": "TXN-90218201",
      "paid_at": "2026-05-23T12:00:00Z"
    }
    ```
*   **Success Response:**
    *   *Status Code:* `200 OK`
*   **Permissions:** Authenticated Admins.

---

## 22. Admin Collection Center APIs

### 22.1 Add Center
*   **Method & URL:** `POST /admin/centers`
*   **Request Headers:** `Authorization: Bearer <JWT_ACCESS_TOKEN>`
*   **Request Body:**
    ```json
    {
      "center_name": "Madurai Center B",
      "district": "Madurai",
      "pincode": "625002",
      "latitude": 9.9252,
      "longitude": 78.1198,
      "phone": "0452-654321"
    }
    ```
*   **Success Response:**
    *   *Status Code:* `201 Created`
*   **Permissions:** Authenticated Admins.

---

## 23. Admin Notification APIs

### 23.1 Create Announcement
*   **Method & URL:** `POST /admin/announcements`
*   **Request Headers:** `Authorization: Bearer <JWT_ACCESS_TOKEN>`
*   **Request Body:**
    ```json
    {
      "target_type": "ALL_LEADERS",
      "title": "Scheduled Center Closures",
      "message": "Regional centers will close for standard audit testing on May 25, 2026."
    }
    ```
*   **Success Response:**
    *   *Status Code:* `201 Created`
*   **Permissions:** Authenticated Admins.

---

## 24. Analytics APIs

### 24.1 Get Dashboard Statistics
*   **Method & URL:** `GET /analytics/dashboard`
*   **Request Headers:** `Authorization: Bearer <JWT_ACCESS_TOKEN>`
*   **Success Response:**
    *   *Status Code:* `200 OK`
*   **Permissions:** Authenticated Admins.

---

## 25. Audit APIs

### 25.1 Get System Audit Logs
*   **Method & URL:** `GET /admin/audits?page=1&limit=50`
*   **Request Headers:** `Authorization: Bearer <JWT_ACCESS_TOKEN>`
*   **Success Response:**
    *   *Status Code:* `200 OK`
*   **Permissions:** Authenticated Admins.

---

## 26. Developer Monitoring APIs

### 26.1 Get System Health Status
*   **Method & URL:** `GET /developer/system/status`
*   **Request Headers:** `Authorization: Bearer <JWT_ACCESS_TOKEN>`
*   **Success Response:**
    *   *Status Code:* `200 OK`
    *   *Response Payload:*
        ```json
        {
          "cpu_usage": 12.5,
          "memory_usage": 42.1,
          "active_db_connections": 8,
          "api_latency_ms": 45
        }
        ```
*   **Permissions:** Authenticated Developers (`DEVELOPER`).

---

## 27. Backup APIs

### 27.1 Trigger Database Backup
*   **Method & URL:** `POST /developer/backups/create`
*   **Request Headers:** `Authorization: Bearer <JWT_ACCESS_TOKEN>`
*   **Success Response:**
    *   *Status Code:* `201 Created`
*   **Permissions:** Authenticated Developers.

---

## 28. Feature Control APIs

### 28.1 Toggle Platform Feature Flag
*   **Method & URL:** `POST /developer/features/toggle`
*   **Request Headers:** `Authorization: Bearer <JWT_ACCESS_TOKEN>`
*   **Request Body:**
    ```json
    {
      "module_name": "DIGITAL_INDIA",
      "is_enabled": false
    }
    ```
*   **Success Response:**
    *   *Status Code:* `200 OK`
*   **Permissions:** Authenticated Developers.

---

## 29. Authentication Rules

*   **OAuth2 JWT Bearer Tokens:** Access tokens expire after $15\text{ minutes}$, carrying user role scopes.
*   **Refresh Tokens:** Secure, HTTP-only, `SameSite=Strict` refresh cookies expire after $7\text{ days}$.

---

## 30. Role-Based Access Matrix

| API Category | Visitor | Member | Leader | Admin | Developer |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Authentication APIs** | Allowed | Allowed | Allowed | Allowed | Allowed |
| **Profile APIs** | Blocked | Allowed | Allowed | Allowed | Allowed |
| **Application APIs** | Allowed | Blocked | Blocked | Allowed | Allowed |
| **Team APIs** | Blocked | View Only | Allowed | Allowed | Allowed |
| **Referral APIs** | Validate | Blocked | Allowed | Allowed | Allowed |
| **Level APIs** | Blocked | Allowed | Allowed | Allowed | Allowed |
| **Waste APIs** | Blocked | Allowed | Allowed | Allowed | Allowed |
| **Collection Center APIs**| View Only | View Only | View Only | Allowed | Allowed |
| **Reward Claim APIs** | Blocked | Allowed | Allowed | Allowed | Allowed |
| **Payment APIs** | Blocked | View Only | View Only | Allowed | Allowed |
| **Admin APIs** | Blocked | Blocked | Blocked | Allowed | Allowed |
| **Developer APIs** | Blocked | Blocked | Blocked | Blocked | Allowed |

---

## 31. Payload Input Validations

*   **Username:** Alphanumeric ($5$ to $30$ characters).
*   **Password:** Min $8$ characters, containing uppercase, lowercase, numbers, and special characters.
*   **Phone Number:** Exactly $10$ numeric digits.
*   **Aadhaar Number:** Exactly $12$ numeric digits.
*   **IFSC Code:** Correct bank validation syntax matching local matrices.
*   **Referral Code:** Checks characters and length before validation checks.

---

## 32. API Pagination Standards

Pagination is mandatory for: Users, Teams, Members, Waste Records, Payments, Audit Logs, and Notifications. All API routes returning list collections must implement standard pagination filters:

```
[ Request: GET /api/v1/waste?page=1&limit=20&sort_by=created_at&order=desc ]
                             │
                             ▼
[ Response JSON: { "items": [...], "total": 142, "page": 1, "limit": 20 } ]
```

---

## 33. Response Standards

*   **Success Model:** HTTP Status `200` or `201` returning standardized JSON payloads.
*   **Error Model:** HTTP status codes (`400`, `401`, `403`, `404`, `422`, `429`, `500`) returning consistent details.
*   **Validation Failures:** Return code `422 Unprocessable Entity` with parameter details.

---

## 34. Error Code Catalog

*   `400 Bad Request` $\rightarrow$ `"INVALID_PAYLOAD"`, `"DUPLICATE_TEAM_NAME"`
*   `401 Unauthorized` $\rightarrow$ `"INVALID_CREDENTIALS"`, `"EXPIRED_TOKEN"`
*   `403 Forbidden` $\rightarrow$ `"INSUFFICIENT_PERMISSIONS"`, `"ACCOUNT_SUSPENDED"`
*   `404 Not Found` $\rightarrow$ `"RESOURCE_NOT_FOUND"`, `"CENTER_NOT_FOUND"`
*   `409 Conflict` $\rightarrow$ `"CLAIM_ALREADY_EXISTS"`, `"REFERRAL_LIMIT_REACHED"`
*   `429 Too Many Requests` $\rightarrow$ `"RATE_LIMIT_EXCEEDED"`
*   `500 Internal Error` $\rightarrow$ `"DATABASE_UNAVAILABLE"`, `"SYSTEM_ERROR"`

---

## 35. Rate Limiting Standards

*   **Authentication APIs:** Capped at $5\text{ requests/minute}$ per IP address to prevent brute-force compromises.
*   **Sensitive APIs (Profile, Claim):** Capped at $10\text{ requests/minute}$ per IP address to prevent spammed requests.
*   **Public APIs:** Capped at $60\text{ requests/minute}$ per IP address.
*   **Admin APIs:** Capped at $120\text{ requests/minute}$ per active account.

---

## 36. Security Standards

*   **JWT Payload Security:** Tokens carry zero unmasked PII. Scopes check role permissions dynamically at the gateway layer.
*   **Security Hardening & Account Lockout:** Force account lockout after **5 failed login attempts** within an hour. Integrate secure headers, CSRF protections, and CORS whitelists.
*   **Input Sanitization:** Parameter fields escape HTML characters to block cross-site scripting and SQL injection threats.
*   **File Upload Protections:** Enforces strict MIME validations, limits sizes (max $5\text{MB}$), and renames files to UUID paths.

---

## 37. API Lifecycle Management

*   **Version Prefixes:** Enforces explicit URL prefixes (e.g., `/api/v1/*`) on all active routes.
*   **Deprecation Rules:** Inactive API paths are marked `DEPRECATED` in Swagger schemas, logging migration warnings to notify frontend teams.
*   **Backwards Compatibility:** Changes to payloads must keep old keys intact, ensuring backward compatibility.

---

## 38. Skill India API Expansion (Phase 2)

*   **Future Endpoints:**
    *   `GET    /skills/courses`
    *   `POST   /skills/enrollments`
    *   `POST   /skills/attendance`
    *   `POST   /skills/assessments`
*   **Compatibility:** Mounts future routers in isolated configurations under `/api/v1/skills/*`, preserving existing waste and profile endpoints.

---

## 39. Clean India API Expansion (Phase 3)

*   **Future Endpoints:**
    *   `POST   /clean/logistics`
    *   `POST   /clean/processing`
    *   `GET    /clean/reports/district`
*   **Compatibility:** Mounts logistics and processing APIs under `/api/v1/clean/*`, avoiding schema conflicts with Phase 1 configurations.

---

## 40. Conclusion

This API Specification Document (`07_API_SPECIFICATION.md`) establishes the absolute REST contracts, payload schemas, security guards, input validations, error catalogs, and future integration guidelines for the Athiyaman Platform – Digital India Phase 1. By detailing endpoints for authentication, profiles, teams, waste logs, claims, and administrative queues, it serves as a complete reference for frontend and backend engineering teams, enabling independent development cycles.
