# Athiyaman Platform - Foundation Document
## Phase 1 – Digital India Business & Software Requirements Specification

---

## 1. Document Information

*   **Project Name:** Athiyaman Platform
*   **Document Name:** Foundation Document (Business & Software Requirements Specification)
*   **File Name:** `01_FOUNDATION.md`
*   **Version:** 1.0.0
*   **Prepared By:** Athiyaman Platform Core Systems Architect & Product Engineering Team
*   **Date:** May 23, 2026
*   **Purpose:** This document establishes the absolute Business Requirements Specification (BRS) and Software Requirements Specification (SRS) for Phase 1 (Digital India) of the Athiyaman Platform. It serves as the primary business, operational, and functional blueprint for all database design, API design, frontend interfaces, backend services, testing criteria, and deployment models.
*   **Audience:** Platform Owners, Product Managers, Frontend Developers, Backend Developers, Quality Assurance Engineers, System Administrators, and DevOps Engineers.
*   **Approval Status:** Approved
*   **Document History:**
    | Date | Version | Description | Author |
    | :--- | :--- | :--- | :--- |
    | 2026-05-23 | 1.0.0 | Initial release of complete Foundation specifications for Phase 1. | Core Architect |

---

## 2. Executive Summary

### 2.1 What is the Athiyaman Platform?
The Athiyaman Platform is a centralized, digital socio-economic ecosystem built to incentivize citizen-driven civic engagement. By providing structured, referral-based team-building structures alongside individual task completion modules, the platform enables users to progress through verified performance levels and claim financial rewards. 

### 2.2 Why it is Being Developed
Modern civic initiatives often suffer from administrative silos, lack of traceability, fraudulent reporting, and low citizen participation. The Athiyaman Platform is being developed to resolve these bottlenecks by creating a fully transparent, highly secure, and gamified portal where every action (recruitment, waste collection, and reward payment) is digitally verified and permanently recorded.

### 2.3 Problems Addressed
*   **Lack of Traceability:** Physical waste collection metrics are prone to misreporting and administrative loss.
*   **High Financial Fraud Risk:** Unverified bank accounts and manual document reviews lead to duplicate reward distributions.
*   **Opaque Administrative Activities:** The lack of open record-keeping damages public trust in community reward programs.
*   **Fragmented Citizen Recruitment:** Traditional volunteer drives lack clear progression metrics and systemic incentives.

### 2.4 Expected Outcomes
*   **Absolute Ledger Integrity:** $100\%$ digital traceability of every gram of collected waste and every Rupee of paid rewards.
*   **Zero-Fraud Disbursement:** Complete pre-payment checks, linking disbursements directly to verified Aadhaar and bank details.
*   **Active Citizen Retention:** Elevated community engagement via structural personal levels (7–11) and team levels (1–6).
*   **Seamless Architectural Expansion:** A core digital foundation ready to launch Phase 2 (Skill India) and Phase 3 (Clean India).

### 2.5 Alignment with Digital India
The platform is designed in strict alignment with the Union Government's **Digital India** initiative, converting paper-heavy field operations into secure, auditable, and paperless digital registries. It relies on digital identity verification, cloud-based data management, and direct-to-bank electronic reward transfers.

---

## 3. Background

To build a high-integrity community engine, the platform addresses seven critical operational challenges:

*   **Current Challenges:** Traditional civic and environmental collection drives rely on physical logs and manual checklists. These systems are highly vulnerable to transcription errors, lack of verification, double-claiming, and administrative delays.
*   **Need for a Unified Digital Platform:** A centralized, web-based digital workspace ensures that every participant, local collection center, and central administrator operates on a single, synchronized source of truth, removing local data discrepancies.
*   **Need for Structured Team Management:** Scalable public mobilization requires localized leadership. By establishing formal, digitally monitored team structures, the platform enables vetted Leaders to coordinate local community actions effectively.
*   **Need for Rigorous Waste Tracking:** To avoid duplicate reporting, waste submissions require dynamic geocoded registration, photo evidence, weight verification, and historical status logs.
*   **Need for Secure Reward Tracking:** To prevent the abuse of public/corporate funds, reward releases must be tied strictly to verified level milestones, preventing duplicate claims or manual overrides.
*   **Need for Administrative Transparency:** Providing a transparent dashboard allows citizens to see exactly how their contributions are reviewed, approved, and paid.
*   **Need for Immutable Auditability:** To ensure absolute accountability, every user transaction, profile update, and verification decision must be permanently logged in a read-only audit trail.

---

## 4. Vision Statement

### 4.1 Long-Term Platform Vision
To create India's most secure, scalable, and trusted civic-reward ecosystem, where micro-contributions are verifiably mapped to national growth, individual livelihood support, and regional ecological improvement.

```
                  ┌──────────────────────────────┐
                  │   National Scale Expansion   │
                  └──────────────▲───────────────┘
                                 │
                  ┌──────────────┴───────────────┐
                  │    Phase 3: Clean India      │
                  └──────────────▲───────────────┘
                                 │
                  ┌──────────────┴───────────────┐
                  │    Phase 2: Skill India      │
                  └──────────────▲───────────────┘
                                 │
                  ┌──────────────┴───────────────┐
                  │   Phase 1: Digital India     │
                  └──────────────────────────────┘
```

### 4.2 Community Participation Goals
To transition volunteer operations into a gamified, reward-aligned civic contribution system, turning environmental action into a viable livelihood stream.

### 4.3 Digital Ecosystem Goals
To implement an enterprise-grade platform with zero database bypasses, $100\%$ secure encryption of citizen data, and instant API validation of business constraints.

### 4.4 Future Expansion Goals
To scale the platform seamlessly across Indian states, integrating digital skill development (Skill India) and waste processing plants (Clean India) into a single, unified civic platform.

---

## 5. Mission Statement

*   **Operational Mission:** To maintain a highly reliable, low-latency web portal that guarantees swift, transparent processing of citizen claims and waste audits.
*   **Social Mission:** To empower marginalized local communities by providing fair economic rewards in exchange for direct environmental contributions.
*   **Technology Mission:** To build the platform using proven open-source technologies (FastAPI, React, PostgreSQL), ensuring modularity, type safety, and direct-hosting compatibility.
*   **Governance Mission:** To enforce strict, non-bypassable administrative workflows where every operational decision is linked to a validated credentials footprint and documented in an immutable audit trail.

---

## 6. Project Objectives

### 6.1 User Management
*   Provide secure registration, multi-factor credential validations, and robust profile lockouts.
*   Track complete biographical, bank, and nominee records, calculating profile completeness from $0\%$ to $100\%$.

### 6.2 Team Management
*   Enforce a strict "One Leader = One Team" constraint.
*   Maintain regional, pincode-specific team tables to prevent overlapping local jurisdictions.

### 6.3 Referral Management
*   Implement a strict, closed-loop referral system with complete validation, expiration controls, and utilization tracking.

### 6.4 Waste Management
*   Track the lifecycle of waste records, capturing weight metrics, geocodes, photos, and center details.
*   Maintain a detailed history of status changes (`waste_status_history`) for every audit event.

### 6.5 Level Management
*   Track linear, non-bypassable progression pathways: Team Levels 1–6 (member-count driven) and Personal Levels 7–11 (waste-weight driven).

### 6.6 Reward Management
*   Establish secure reward eligibility checks, validating milestones before allowing claims.

### 6.7 Payment Management
*   Provide a secure queue for claim processing, matching disbursed funds with official bank transaction reference codes.

### 6.8 Notification Management
*   Deliver real-time updates through in-app channels and secure out-of-band alerts for critical system events.

### 6.9 Administrative Monitoring
*   Equip operational managers with dashboards to vet applications, verify documents, and process payments without direct database access.

### 6.10 Developer Monitoring
*   Provide system diagnostics, real-time logging, data backup controls, and modular feature toggles.

### 6.11 Audit Compliance
*   Log all system-mutating actions asynchronously to ensure complete data integrity.

### 6.12 Analytics
*   Expose pre-aggregated performance dashboards, displaying regional growth, waste collection weights, and financial metrics.

---

## 7. Project Scope (Phase 1 – Digital India)

The following components are **IN SCOPE** for Phase 1:

*   **Public Website:** Home, About, Initiatives, Waste Management Info, Team Leader Application Form, and Contact Page.
*   **Authentication Engine:** OTP-based login, referral-forced signup, JWT access tokens, HTTP-only refresh cookies, and password reset flows.
*   **Profile System:** Personal information, encrypted Aadhaar entries, validated banking data, nominee fields, and document upload capabilities.
*   **Team System:** Unique team codes, team profiles, regional boundaries, and active member rosters.
*   **Referral System:** Secure generation, validation, and usage limits of `LEADER_REFERRAL` and `TEAM_REFERRAL` codes.
*   **Level Progression:** Automated tracking and milestone enforcement of Team Levels 1–6 and Personal Levels 7–11.
*   **Waste Registry:** Logging of waste deposits, geolocated collection maps, photo uploads, and verification status timelines.
*   **Collection Centers:** Registry of authorized locations geocoded by latitude/longitude, searchable by district and pincode.
*   **Claims System:** Submitting, reviewing, approving, and rejecting level reward claims.
*   **Payment Ledger:** Queue management for outstanding claims, transaction logs, and reference number audits.
*   **In-App Alerts:** Interactive user inbox notifications triggered by level milestones, claim approvals, and admin events.
*   **Admin Dashboard:** Central portal for vetting leaders, verifying waste records, and managing payments.
*   **Developer Dashboard:** Diagnostics panel for system health, real-time logs, backups, and feature flags.
*   **Audit Engine:** Immutable audit logs capturing the user, role, action, targeted entity, IP, and device.
*   **Analytics Engine:** Dashboard charts highlighting platform growth, collection totals, and financial metrics.

---

## 8. Out Of Scope

The following items are **EXCLUDED** from Phase 1:

> [!WARNING]
> **EXCLUSION BOUNDARIES:** The following modules and integrations are strictly out of scope for Phase 1. Any attempt to introduce them prematurely will violate project directives and delay the delivery of the core system.

*   **Skill India Modules (Phase 2):** Course catalogs, training class registries, trainer dashboards, attendance trackers, assignments, assessments, certifications, and salary databases.
*   **Clean India Processing (Phase 3):** Waste processing plants, logistics routing, transport records, regional environmental statistics, and manager dashboards.
*   **Native Mobile Apps:** Direct Android/iOS application packages (APKs/IPAs). The Phase 1 frontend is built strictly as a highly responsive, mobile-friendly web application.
*   **Automated Payment Gateways:** Real-time bank payouts via direct banking APIs. Phase 1 handles payments through an administrative ledger where payouts are marked as paid manually after recording external bank transaction references.
*   **Direct SMS/WhatsApp API Integrations:** Programmatic delivery of SMS or WhatsApp messages. These external networks are represented via mock adapters in the backend, preparing the system for live integrations in subsequent phases.
*   **AI Verification Systems:** Auto-classification of waste photos. Photo audits are processed manually by administrators.
*   **Offline Functionality:** Offline database caching and offline form submissions. The platform operates strictly in an online, connected state.

---

## 9. Future Scope

*   **Phase 2 – Skill India:** Adding physical training courses, student attendance metrics, assessments, digital certifications, and job matching.
*   **Phase 3 – Clean India:** Scaling environmental operations by integrating regional waste processing plants, logistics transport logs, and advanced district coordinator hierarchies.
*   **Mobile Applications:** Developing native iOS and Android apps using API gateways optimized for low-bandwidth mobile environments.
*   **Financial Integrations:** Linking direct UPI payouts, instant bank transfer rails, and corporate CSR sponsor accounts.
*   **Notification Upgrades:** Transitioning backend adapters to direct integrations with national SMS and WhatsApp gateways.
*   **Advanced Regional Analytics:** Expanding dashboards to generate custom state and municipal waste recycling reports.

---

## 10. Stakeholder Matrix

| Stakeholder Role | Responsibilities | Key Expectations | Common Platform Interactions |
| :--- | :--- | :--- | :--- |
| **Platform Owner** | Project sponsorship, funding allocations, and operational approvals. | Absolute transparency of payouts, zero financial leakage, and robust project scaling. | Accesses analytics dashboards and high-level audit reports. |
| **System Admin** | Manages daily operations, vets users, verifies waste collections, and processes payments. | Intuitive queues, clear photo evidence, and smooth validation checks. | Reviews leader applications, document uploads, waste records, and reward claims. |
| **Developer Team** | Maintains system health, fixes bugs, manages database integrity, and deploys features. | Highly modular code, clear API specifications, and detailed system logging. | Uses developer diagnostics, system logs, backups, and feature flags. |
| **Team Leaders** | Create unique teams, generate referral codes, and recruit and coordinate local members. | Instant referral generation, clear team growth dashboards, and quick payout processing. | Manages profiles, monitors teams, tracks progress (Levels 1–6), and claims rewards. |
| **Team Members** | Participate in collection events, record waste metrics, and earn rewards. | Fast mobile interfaces, clear progress tracking, and secure direct-to-bank payments. | Submits profiles, accepts rules, logs waste, and tracks personal progress (Levels 7–11). |
| **Clean India Team** *(Future)* | Manages processing plants, handles logistics, and coordinates district waste transit. | Relational, extensible data structures that connect easily with Phase 1 components. | Extends regional center registers and manages logistics logs. |
| **Skill India Team** *(Future)* | Administers physical training courses and tracks student certifications. | Flexible database schemas and reusable user validation components. | Manages courses, logs attendance, and issues digital certificates. |

---

## 11. User Roles & Workflow Boundaries

### 11.1 Visitor
*   **Purpose:** Unregistered guest visiting the public portal.
*   **Responsibilities:** Learn about platform goals and apply to become a vetted Team Leader.
*   **Permissions:** View public informational pages (Home, About, Initiatives, Waste Info, Contact) and submit a leader application.
*   **Restrictions:** Cannot log waste, view dashboards, access payment registries, or see internal collection center details.
*   **Workflow Participation:** Visitor $\rightarrow$ Leader Application Submission.

### 11.2 Team Member
*   **Purpose:** Registered community participant.
*   **Responsibilities:** Join local teams, participate in programs, record waste collections, and track personal milestones.
*   **Permissions:** Manage personal profile, upload waste records, view collection centers, track progress (Levels 7-11), and submit personal claims.
*   **Restrictions:** Cannot create a team, generate referral codes, access administrative queues, or view other users' files.
*   **Workflow Participation:** Signup with referral $\rightarrow$ Complete profile $\rightarrow$ Accept rules $\rightarrow$ Submit waste $\rightarrow$ Complete Levels 7-11 $\rightarrow$ Request payout.

### 11.3 Team Leader
*   **Purpose:** Registered team coordinator.
*   **Responsibilities:** Grow and manage a local team, generate referral codes, and participate in personal waste collection.
*   **Permissions:** All Team Member actions, create and manage a single team, generate team referral codes, and track team progress (Levels 1-6).
*   **Restrictions:** Cannot approve other leader applications, modify platform configurations, or view admin dashboard pages.
*   **Workflow Participation:** Apply $\rightarrow$ Sign up $\rightarrow$ Create team $\rightarrow$ Recruit members $\rightarrow$ Complete Levels 1-6 $\rightarrow$ Track personal Levels 7-11 $\rightarrow$ Claim rewards.

### 11.4 Admin
*   **Purpose:** Platform manager.
*   **Responsibilities:** Vet users, verify uploads, and manage reward payments.
*   **Permissions:** Approve leader applications, generate leader referral codes, verify documents, audit waste queues, and process reward payouts.
*   **Restrictions:** Cannot modify source code, alter audit database records, or access developer consoles.
*   **Workflow Participation:** Review leader applications $\rightarrow$ Issue registration codes $\rightarrow$ Audit documents $\rightarrow$ Verify waste $\rightarrow$ Approve claims $\rightarrow$ Mark payments.

### 11.5 Developer
*   **Purpose:** Technical system administrator.
*   **Responsibilities:** Maintain infrastructure, monitor health, and handle backup operations.
*   **Permissions:** View real-time logs, monitor metrics (CPU/Memory/DB Pools), trigger backups, and toggle feature flags.
*   **Restrictions:** Cannot approve financial reward claims, modify user bank details, or bypass database audit logs.
*   **Workflow Participation:** Monitor infrastructure health $\rightarrow$ Audit system security $\rightarrow$ Manage backups $\rightarrow$ Toggle feature releases.

---

## 12. Core Business Rules

To prevent fraud and maintain operational integrity, the platform enforces 12 core business rules:

```
┌────────────────────────────────────────────────────────┐
│             One Leader = One Team Requirement          │
├────────────────────────────────────────────────────────┤
│                 Unique Team Name Enforcement           │
├────────────────────────────────────────────────────────┤
│                Mandatory Referral Sign Up              │
├────────────────────────────────────────────────────────┤
│              100% Profile Completeness Lock            │
├────────────────────────────────────────────────────────┤
│                Explicit Rules Acceptance               │
├────────────────────────────────────────────────────────┤
│             Linear Level Progression (No Skips)        │
├────────────────────────────────────────────────────────┤
│           Double-Verification of Waste Weights         │
├────────────────────────────────────────────────────────┤
│             Manual Claim Approval Checkpoints          │
├────────────────────────────────────────────────────────┤
│             Mandatory Bank Transaction Logging        │
├────────────────────────────────────────────────────────┤
│                Immutable Audit Recording               │
├────────────────────────────────────────────────────────┤
│                Strict Token Session Security           │
├────────────────────────────────────────────────────────┤
│              Compliant Citizen PII Encryption          │
└────────────────────────────────────────────────────────┘
```

1.  **One Leader, One Team:** A Team Leader can create, name, and manage exactly one team. Creating secondary teams or transferring team ownership is blocked at the service layer, requiring overriding permissions from an Admin.
2.  **Unique Team Names:** Every team name must be globally unique across the platform. Duplicates (e.g., two teams named "Athiyaman Madurai") are blocked during creation to prevent copycat teams.
3.  **Mandatory Referral Signup:** Public signup is entirely disabled. Every account registration requires a valid, active referral code.
4.  **Profile Completeness Lock:** Standard dashboard pages are locked until profile details (biography, Aadhaar, bank routing, nominee fields) are $100\%$ complete.
5.  **Mandatory Rules Acceptance:** Users must explicitly accept the platform's rules via a click-wrap checkbox before dashboard features are unlocked.
6.  **Linear Level Progression:** Level-ups must be earned sequentially. Users cannot skip levels (e.g., jumping from Level 1 directly to Level 3 is blocked by the progression service).
7.  **Rigorous Waste Verification:** A waste record only counts toward level progress once an Admin verifies its photo, weight, location, and collection center details, transitioning its status to `APPROVED`.
8.  **Manual Payout Claims:** Achieving level milestones makes a user eligible for rewards, but payouts are not released automatically. Users must submit a formal Claim Request, which is reviewed manually by an Admin.
9.  **Direct Payout Verification:** Payout claims are processed only after Aadhaar documents and bank account numbers are fully vetted, reducing payment risks.
10. **Immutable Audit Trails:** Any system-mutating operation (such as updating bank routing info or changing claim states) must write an entry to the `audit_logs` table. Mutation or deletion of these logs is blocked at the database layer.
11. **Session Expiry Guards:** Citizen dashboards require valid JWT credentials. Inactive sessions are logged out automatically after $15\text{ minutes}$, requiring token refresh validations.
12. **PII Encryption at Rest:** Citizen Aadhaar entries and bank routing numbers are stored using dynamic encryption, shielding private citizen information from unprivileged database lookups.

---

## 13. Registration Rules

*   **Leader Registration:** Requires a valid, active `LEADER_REFERRAL` code generated by an Admin. Vetted leaders receive the registration link via official email/SMS.
*   **Member Registration:** Requires a valid, active `TEAM_REFERRAL` code generated by an active Team Leader. The registration service links the member to the leader's team.
*   **Referral Code Validation:** Before rendering registration fields, the signup service validates that the inputted code exists, is marked active, has usage capacity, and is not expired.
*   **OTP Verification:** Signup requires verifying the user's mobile number via a $6$-digit one-time password (OTP). OTPs are active for $5\text{ minutes}$ and limited to $3\text{ generation attempts}$ within an hour per IP to prevent spam.
*   **Username Standards:** Usernames must be alphanumeric, containing between $5$ and $30$ characters, and globally unique.
*   **Password Complexity:** Passwords must be at least $8$ characters long, containing at least one uppercase letter, one lowercase letter, one number, and one special character.
*   **User Account Lifecycle:**
    ```
    [REGISTERED] -> [PROFILE_PENDING] -> [RULES_PENDING] -> [ACTIVE] <-> [SUSPENDED]
    ```
*   **Suspension Rules:** Admins can suspend accounts flagged for security alerts or fraudulent submissions. Suspension blocks dashboard access and active referrals instantly.
*   **Reactivation Rules:** Suspended users can be reactivated by Admins after resolving verification issues, which writes an entry to the audit log.
*   **Failure Scenarios:** Inputs containing expired referral codes, invalid OTPs, or non-unique usernames are rejected with clear error codes.

---

## 14. Profile Management Rules

*   **Required Personal Fields:** Full name, gender selection, date of birth, profile photo, active contact phone, and verified email address.
*   **Required Identity Fields:** $12$-digit Aadhaar number, physical address details (State, District, Pincode), and Aadhaar document scans.
*   **Required Banking Fields:** Account holder name, verified bank name, account number, IFSC routing code, and passbook scan uploads.
*   **Required Nominee Fields:** Full name of the beneficiary nominee, relationship type, and active contact number.
*   **Document Scan Verification:** Aadhaar card and banking passbook scans must be clear, high-contrast file uploads in PDF, PNG, or JPEG formats (max $5\text{MB}$).
*   **Profile Completion Scoring:** The backend calculates a dynamic completeness score as follows:
    *   *Section A: Personal details* $\rightarrow 20\%$
    *   *Section B: Contact details* $\rightarrow 10\%$
    *   *Section C: Address details* $\rightarrow 10\%$
    *   *Section D: Aadhaar details* $\rightarrow 20\%$
    *   *Section E: Bank routing* $\rightarrow 30\%$
    *   *Section F: Nominee details* $\rightarrow 10\%$
*   **Validation Checkpoints:** Bank routing structures are checked against local database matrices using IFSC verification rules to catch entry typos early.
*   **Profile Update Boundaries:** Bank account and Aadhaar numbers are locked once verified by an Admin. Any subsequent modifications require a support request, logging a high-priority entry in the audit trail.

---

## 15. Team Management Rules

*   **Team Creation:** Approved Team Leaders create a team by submitting a unique name, regional district, area description, and pincode.
*   **Team Membership:** A Member is linked to the team of the Leader whose referral code was used during registration. Members cannot switch teams without Admin intervention.
*   **Team Ownership Constraints:** Leaders can own exactly one team. They cannot manage secondary teams or transfer team ownership without Admin approvals.
*   **Validation Rules:** Team names undergo strict validation checks, filtering out profanity, special characters, and matches with existing team names.
*   **Member Capacity Constraints:** A team can scale to support up to $50,000$ members, aligned with the requirements of Team Level 6.
*   **Team Lifecycle:**
    ```
    [CREATED] -> [ACTIVE] <-> [SUSPENDED]
    ```
*   **Status Management:** Admins can suspend teams flagged for systemic collection fraud or spam registrations. Suspending a team freezes referral operations and halts progression calculations.

---

## 16. Referral Management Rules

*   **Admin Referrals (`LEADER_REFERRAL`):** Generated by Admins to register approved leaders. These codes are single-use and expire after $48\text{ hours}$.
*   **Leader Referrals (`TEAM_REFERRAL`):** Generated by active Leaders to recruit members. These codes are multi-use, limited to the capacity required for the leader's current level.
*   **Usage Tracking:** Every referral code tracks its current utilization counts, linking newly registered users to their referrers in a database ledger.
*   **Expiration Standards:** Team referral codes expire automatically when the leader completes their current level or when manually deactivated by the leader.
*   **Manual Deactivation:** Leaders can manually deactivate their active codes to freeze new signups, keeping their team size stable.
*   **Referral Lifecycle:**
    ```
    [GENERATED] -> [ACTIVE] -> [MAX_CAPACITY / EXPIRED / MANUALLY_DISABLED]
    ```
*   **Referral Audits:** The generation, validation, and deactivation of referral codes are logged in the audit trail, tracking the IP address and active user ID.

---

## 17. Level Management Rules

The platform enforces two distinct progression structures, maintaining linear progression checks at the database layer.

### 17.1 Team Levels (1–6)
Designed for Leaders, tracking growth based on total verified team size.

| Level | Required Verified Members | Financial Reward | Validation Rules |
| :--- | :--- | :--- | :--- |
| **Level 1** | $10\text{ Members}$ | ₹100 | Requires $10$ active members with $100\%$ complete profiles. |
| **Level 2** | $90\text{ Members}$ | ₹1,000 | Requires $90$ active members with $100\%$ complete profiles. |
| **Level 3** | $720\text{ Members}$ | ₹2,000 | Requires $720$ active members with $100\%$ complete profiles. |
| **Level 4** | $5,040\text{ Members}$ | ₹3,000 | Requires $5,040$ active members with $100\%$ complete profiles. |
| **Level 5** | $30,240\text{ Members}$ | ₹4,000 | Requires $30,240$ active members with $100\%$ complete profiles. |
| **Level 6** | $50,000\text{ Members}$ | ₹5,000 | Requires $50,000$ active members with $100\%$ complete profiles. |

### 17.2 Personal Levels (7–11)
Available to all registered users (Members and Leaders), tracking individual environmental action.

| Level | Required Weight per Level | Financial Reward | Validation Rules |
| :--- | :--- | :--- | :--- |
| **Level 7** | $10\text{ KG}$ of Approved Waste | ₹10,000 | Requires $10\text{ KG}$ of approved waste collected at authorized centers. |
| **Level 8** | $10\text{ KG}$ of Approved Waste | ₹20,000 | Requires a new $10\text{ KG}$ of approved waste after Level 7 completion. |
| **Level 9** | $10\text{ KG}$ of Approved Waste | ₹30,000 | Requires a new $10\text{ KG}$ of approved waste after Level 8 completion. |
| **Level 10** | $10\text{ KG}$ of Approved Waste | ₹40,000 | Requires a new $10\text{ KG}$ of approved waste after Level 9 completion. |
| **Level 11** | $10\text{ KG}$ of Approved Waste | ₹50,000 | Requires a new $10\text{ KG}$ of approved waste after Level 10 completion. |

### 17.3 Progression Rules
*   **Linear Sequence Enforcement:** Users must complete levels in order. The progression service blocks attempts to skip levels.
*   **Level Completion Logic:**
    *   *Team Levels:* Checked automatically when a new member completes their profile. Reaching the threshold marks the level as complete and enables the leader's claim button.
    *   *Personal Levels:* Reaching the $10\text{ KG}$ approved waste threshold marks the level as complete and opens the personal claim button.
*   **Personal level-up boundaries:** Once a personal level is completed, the waste balance resets to $0\text{ KG}$ for the next level's tracking. Excess waste from a previous level does not roll over.

---

## 18. Waste Management Rules

*   **Waste Log Fields:** User ID, selected collection center ID, photo upload, weight in KG, collection date, geocodes, and status fields.
*   **Weight Verification:** Submissions must reflect physical weight metrics ($0.1\text{ KG}$ minimum up to $50.0\text{ KG}$ maximum per upload).
*   **Photo Evidence:** Submissions require a clear photo showing the waste on a scale at an authorized collection center.
*   **Allowed Materials:** Clean plastic bottles, dry packaging covers, and plastic containers.
*   **Prohibited Materials:** Medical waste, organic garbage, hazardous waste, and chemicals are rejected.
*   **Verification Workflow:**
    ```
    [SUBMITTED] -> [PENDING_VERIFICATION] -> [APPROVED] OR [REJECTED]
    ```
*   **Verification Timeline:** Admins verify waste records manually within $24\text{ hours}$ by comparing uploaded weights with the center's receipts.
*   **Audit Requirements:** State transitions are logged in `waste_status_history`, recording the admin ID, comments, and timestamp.

---

## 19. Collection Center Rules

*   **Registry Details:** Center name, district, pincode, geocoordinates, contact number, and status flag.
*   **Pincode Search:** Users can locate centers using pincode searches or geographic sorted lists based on their current locations.
*   **Geocoding Standards:** Coordinate coordinates (Latitude and Longitude) must be verified via Google Maps.
*   **Visibility Controls:** Only centers marked `ACTIVE` by an Admin are visible to users.
*   **Operational Controls:** Admins can edit details or temporarily disable centers for maintenance, hiding them from search results.

---

## 20. Reward Management Rules

*   **Milestone Eligibility:** Users become eligible for rewards once the level progression service marks a level status as `COMPLETED`.
*   **Manual Claim Submission:** Reaching a milestone enables the "Claim Reward" button. Users submit claims manually to verify their bank details before payouts are processed.
*   **Vetting Checkpoints:** The claims engine validates that the user's profile is complete, documents are verified, and no other active claims exist for the same level.
*   **Claim Rejection Rules:** Admins can reject claims if identity discrepancies or profile changes are flagged, returning the level progress status to `COMPLETED` for review.
*   **Claim Lifecycle:**
    ```
    [INITIATED] -> [PENDING_AUDIT] -> [APPROVED] OR [REJECTED]
    ```
*   **Audit Trail Logs:** Every claim creation, review, and status update is logged in the audit trail.

---

## 21. Payment Management Rules

*   **Queue Management:** Approved claims route to the Payment Queue. Admins process disbursements manually using external banking portals.
*   **Disbursement Records:** When marking a claim as `PAID`, Admins must input the official bank transaction reference number, payment date, and auditing notes.
*   **Direct Bank Transfers:** Payments are sent directly to the verified bank account recorded in the user's profile.
*   **Payment Lifecycle:**
    ```
    [UNPAID] -> [PROCESSING] -> [PAID] OR [FAILED]
    ```
*   **Failure Recovery:** If a transfer fails (e.g., due to bank rejection), the Admin marks the transaction as `FAILED`, returns the claim to the queue, and notifies the user to update their banking details.
*   **Auditing Controls:** Any update to payment registers must write an immutable entry to the audit logs, capturing transaction references and admin IDs.

---

## 22. Notification Rules

*   **In-App Alerts:** Interactive inbox messages delivered on the dashboard. Inbox items track their own read/unread states.
*   **System Event Triggers:** Automated alerts are sent for key events:
    *   *Registration:* Welcome note and profile completion instructions.
    *   *Team Growth:* Notice to the leader when a new member joins.
    *   *Level Completion:* Milestone alerts when a level is completed.
    *   *Waste Actions:* Submission updates, approvals, and rejections.
    *   *Payments:* Payout approval and bank transaction reference details.
*   **Security Alerts:** Asynchronous alerts sent for failed logins, profile edits, and password updates.
*   **WhatsApp Operational Alerts:** Urgent security and system alerts are routed directly to developers via the WhatsApp API integration adapter.

---

## 23. Audit Trail Rules

*   **Log Coverage:** The audit ledger captures all system-mutating operations:
    *   *Auth:* Successful logins, failed attempts, and password resets.
    *   *Users:* Account suspensions, reactivations, and profile updates.
    *   *Teams:* Team creations, roster changes, and suspensions.
    *   *Waste:* Submissions, approvals, and rejections.
    *   *Claims & Payments:* Submissions, audits, approvals, and payouts.
*   **Access Restrictions:** Audit logs are visible only to Admins and Developers through read-only dashboard portals.
*   **Data Integrity Protection:** The audit table (`audit_logs`) has no update or delete routes, protecting the ledger from modification.
*   **Retention Period:** Audit logs are retained for $7\text{ years}$ to meet compliance and operational needs.

---

## 24. Security Principles

*   **Zero-Trust Authentication:** All non-public APIs require JWT token validation. Tokens are checked for active roles and user statuses.
*   **Secure Password Hashing:** Passwords must be hashed using high-computation **Argon2id** algorithms, preventing brute-force compromises.
*   **Granular Session Security:** Access tokens carry a $15\text{ minute}$ lifespan, supported by HTTP-only refresh cookies ($7\text{ days}$) to block XSS and CSRF.
*   **Role-Based Access Control (RBAC):** Standard users are blocked from administrative routes at the gateway level.
*   **Safe File Handlers:** Document uploads are restricted to secure MIME-types, verified for size (max $5\text{MB}$), and saved under UUID-masked paths to prevent path traversal attacks.
*   **Encrypted Storage:** Personal identity metrics and banking data are encrypted at rest using industry-standard AES-256 algorithms.
*   **Rate Limiting Guards:** API gateways apply rate limits (e.g., standard endpoints capped at $60\text{ requests/minute}$) to prevent denial-of-service threats.

---

## 25. Privacy Principles

*   **Data Isolation:** PII data (Aadhaar, bank account numbers) is encrypted in the database. Dashboards display masked values (e.g., `XXXX-XXXX-1234`) to prevent exposure.
*   **Expiring Document Links:** Document scans are stored in secure, private directories. Admins access documents via temporary, expiring URLs.
*   **Digital Data Protection Act Compliance:** Features align with DPDP guidelines, providing clear consent terms, data minimization, and secure nominee handling.
*   **Data Erasure Protocols:** Suspended or closed accounts undergo anonymization, removing contact details and PII while preserving historical waste weights and audit trails for ledger integrity.

---

## 26. Functional Requirements

### 26.1 Authentication Module
*   **FR-1.1:** The system must validate referral codes during signup, rejecting expired or fully-utilized codes.
*   **FR-1.2:** The system must verify mobile registration using a $6$-digit SMS OTP code within $5\text{ minutes}$.
*   **FR-1.3:** The system must secure user logins using Argon2id password verification and return JWT access tokens.
*   **FR-1.4:** The system must handle password resets via secure email/SMS links verified by OTPs.

### 26.2 Profile Module
*   **FR-2.1:** The system must track profile completeness across biographical, bank, nominee, and document fields.
*   **FR-2.2:** The system must lock user dashboards until profile completeness reaches $100\%$ and the platform rules are accepted.
*   **FR-2.3:** The system must support document uploads (passbooks, Aadhaar) in PDF, PNG, or JPEG (max $5\text{MB}$).
*   **FR-2.4:** The system must mask sensitive fields (Aadhaar, bank accounts) on user profile screens.

### 26.3 Teams Module
*   **FR-3.1:** The system must allow approved leaders to create a team by defining a unique name and geographic region.
*   **FR-3.2:** The system must assign newly registered members to their respective leader's team.
*   **FR-3.3:** The system must expose a read-only member roster to the team leader.
*   **FR-3.4:** The system must prevent leaders from creating secondary teams or transferring team ownership.

### 26.4 Referrals Module
*   **FR-4.1:** The system must allow Admins to generate unique `LEADER_REFERRAL` codes.
*   **FR-4.2:** The system must allow active Leaders to generate `TEAM_REFERRAL` codes.
*   **FR-4.3:** The system must track usage counts for all generated referral codes.
*   **FR-4.4:** The system must support manual deactivation of referral codes by the creator.

### 26.5 Levels Module
*   **FR-5.1:** The system must track linear progress through Team Levels 1–6 based on verified team size.
*   **FR-5.2:** The system must track linear progress through Personal Levels 7–11 based on verified waste weights.
*   **FR-5.3:** The system must calculate level-up eligibility dynamically, blocking attempts to skip levels.
*   **FR-5.4:** The system must reset the active waste weight balance to $0\text{ KG}$ upon completing a personal level.

### 26.6 Waste Module
*   **FR-6.1:** The system must support waste logging by uploading weights, photos, and center selections.
*   **FR-6.2:** The system must route newly logged waste records to the Admin verification queue.
*   **FR-6.3:** The system must log every verification state transition in `waste_status_history`.
*   **FR-6.4:** The system must update the user's active level progress immediately upon waste record approval.

### 26.7 Collection Centers Module
*   **FR-7.1:** The system must allow users to search active collection centers by district or pincode.
*   **FR-7.2:** The system must display geocoded maps, addresses, and phone numbers for verified centers.
*   **FR-7.3:** The system must allow Admins to add, edit, and temporarily disable collection centers.

### 26.8 Claims Module
*   **FR-8.1:** The system must enable claim submissions once the progression engine marks a level as complete.
*   **FR-8.2:** The system must route new claims to the Admin reward queue.
*   **FR-8.3:** The system must prevent duplicate claim submissions for the same level.
*   **FR-8.4:** The system must allow users to track claim states in real-time.

### 26.9 Payments Module
*   **FR-9.1:** The system must route approved claims to the Admin Payment Queue.
*   **FR-9.2:** The system must require bank transaction reference codes before marking claims as paid.
*   **FR-9.3:** The system must notify users when payment states are updated to paid.
*   **FR-9.4:** The system must support marking payments as failed, returning the claim to the queue for review.

### 26.10 Notifications Module
*   **FR-10.1:** The system must send in-app alerts for registration, levels, waste, claims, and payment events.
*   **FR-10.2:** The system must support broad, role-based, or team-specific notification broadcasts by Admins.
*   **FR-10.3:** The system must track read/unread states for all in-app notifications.

### 26.11 Admin Module
*   **FR-11.1:** The system must provide queues for reviewing leader applications and document uploads.
*   **FR-11.2:** The system must provide interfaces for waste record verification and photo audits.
*   **FR-11.3:** The system must provide tools for auditing claims and marking payments.
*   **FR-11.4:** The system must prevent Admins from modifying raw database tables directly.

### 26.12 Developer Module
*   **FR-12.1:** The system must display diagnostic metrics, including CPU load, memory usage, and active database connection pools.
*   **FR-12.2:** The system must support real-time application log exploration.
*   **FR-12.3:** The system must support manual database backup and recovery triggers.
*   **FR-12.4:** The system must support toggle controls for platform modules.

### 26.13 Audit Module
*   **FR-13.1:** The system must log all database-mutating operations asynchronously.
*   **FR-13.2:** The system must capture the user, role, action, targeted entity, IP, and device context for every log.
*   **FR-13.3:** The system must block update and delete queries targeting the audit log table.

### 26.14 Analytics Module
*   **FR-14.1:** The system must aggregate analytics data asynchronously, storing results in dedicated snapshot tables.
*   **FR-14.2:** The system must display charts tracking growth trends, waste collections, and payout metrics.

---

## 27. Non-Functional Requirements

### 27.1 Performance
*   **NFR-1.1:** Standard API endpoints must respond in less than $200\text{ms}$ under normal load conditions.
*   **NFR-1.2:** Dashboard pages must load static files and assets in less than $1.5\text{ seconds}$ on $3\text{G}$ mobile connections.

### 27.2 Scalability
*   **NFR-2.1:** The database schema must support at least $500,000$ active users and $10\text{ million}$ audit/waste records without performance degradation.
*   **NFR-2.2:** The API gateway must support horizontal scaling, allowing instances to run stateless behind a load balancer.

### 27.3 Availability
*   **NFR-3.1:** The platform must target $99.9\%$ uptime, excluding scheduled off-peak maintenance.

### 27.4 Reliability
*   **NFR-4.1:** The database must run on high-availability clusters with automatic failover support.
*   **NFR-4.2:** Automated background processes must recover from connection losses and retry failed notifications.

### 27.5 Maintainability
*   **NFR-5.1:** Code must be strictly typed, modular, and split into clear feature-based directories.
*   **NFR-5.2:** Test coverage for core business logic and database migrations must exceed $85\%$.

### 27.6 Security
*   **NFR-6.1:** Sensitive citizen PII must be encrypted at rest using AES-256 algorithms.
*   **NFR-6.2:** All API queries must enforce token checks, blocking unauthorized requests at the router layer.

### 27.7 Auditability
*   **NFR-7.1:** The database must write mutating actions to a read-only audit log.
*   **NFR-7.2:** Audit logs must retain data for $7\text{ years}$ to meet compliance requirements.

### 27.8 Usability
*   **NFR-8.1:** The user interface must be mobile-friendly and accessible across low-end mobile web browsers.
*   **NFR-8.2:** The UI must follow high-contrast, clear guidelines to ensure accessibility.

### 27.9 Portability
*   **NFR-9.1:** Backend services must run in Docker containers to simplify hosting migrations.
*   **NFR-9.2:** The storage engine must use abstract interfaces, allowing migrations from local directories to S3 via configuration changes.

### 27.10 Recoverability
*   **NFR-10.1:** Backups must support Point-in-Time Recovery (PITR) to minimize data loss.
*   **NFR-10.2:** Systems must recover and resume services in less than $2\text{ hours}$ in the event of a critical host outage.

---

## 28. Risks & Mitigation Strategies

### 28.1 Business Risks
*   **Inadequate Volunteer Signups:**
    *   *Impact:* Slow platform growth and low waste collection volumes.
    *   *Mitigation:* Leaders generate multi-use team referrals, and gamified progress rewards incentivize recruitment.

### 28.2 Operational Risks
*   **Verification Bottlenecks:**
    *   *Impact:* Delayed waste reviews lead to user frustration.
    *   *Mitigation:* Queue dashboards prioritize oldest reviews first, and automated alerts keep Admins updated on queue backlogs.

### 28.3 Technical Risks
*   **Server Outages During Peak Hours:**
    *   *Impact:* Citizen dashboards become inaccessible.
    *   *Mitigation:* Run stateless API instances behind load balancers with automated scaling rules.

### 28.4 Security Risks
*   **Attempts to Exploit Payment Flows:**
    *   *Impact:* Financial loss due to double-claiming or unverified payouts.
    *   *Mitigation:* A level-up only makes a user eligible for rewards; payouts require manual Admin approvals, Aadhaar verification, and unique bank transaction logging.

### 28.5 Scalability Risks
*   **Database Lockups During Peak Traffic:**
    *   *Impact:* Increased latency and transaction failures.
    *   *Mitigation:* Dashboard aggregates read from precalculated snapshot tables (`analytics_snapshots`), and database indexes optimize frequent queries.

### 28.6 Compliance Risks
*   **Improper Storage of Citizen PII:**
    *   *Impact:* Regulatory penalties under DPDP data protection guidelines.
    *   *Mitigation:* Sensitive Aadhaar and bank details are encrypted at rest, and access is restricted to verified administrators.

---

## 29. Assumptions

*   **Continuous Internet Connectivity:** Users have active internet connections when logging waste or reviewing dashboards.
*   **External Verification Operations:** Collection center staff verify physical weights, and Admins confirm match metrics using photo submissions.
*   **Vetted Leaders:** Applicants are reviewed offline to confirm their community capacity before registration codes are issued.
*   **External Payment Settlement:** Rewards are settled using external banking portals, and Admins record payment transactions inside the platform.
*   **Modern Browser Compatibility:** Users use web browsers that support modern JavaScript runtimes and styling engines.

---

## 30. Success Criteria

### 30.1 Technical Success
*   Standard API endpoints maintain response latencies of less than $200\text{ms}$.
*   The platform records zero PII data leaks or unauthorized route access events.
*   Application logs show $100\%$ delivery coverage for the database audit engine.

### 30.2 Operational Success
*   The waste verification queue maintains an average turnaround time of less than $24\text{ hours}$.
*   Approved claims are processed and marked as paid in less than $48\text{ hours}$.
*   The platform records zero duplicate payouts or payment reference conflicts.

### 30.3 Business Success
*   All user registrations map to active, verified referral records.
*   Level progression operates linearly, recording zero skipped levels.
*   Regional team expansion metrics scale in line with local civic project goals.

### 30.4 User Success
*   Dashboards maintain full mobile responsiveness on budget smartphones.
*   Citizen workflows are simple, requiring fewer than $3\text{ steps}$ to submit a waste record.
*   Government-style layout standards deliver high readability and accessible design.

---

## 31. Conclusion

This Foundation Document (`01_FOUNDATION.md`) establishes the complete operational, functional, and technical requirements for the Athiyaman Platform – Digital India Phase 1. By detailing user roles, business rules, registration logic, level progression milestones, waste tracking, payment validations, security standards, and functional requirements, it provides a comprehensive source of truth for engineering teams. All future architectural designs, database schemas, and codebase files must adhere strictly to these principles, ensuring the platform remains highly secure, transparent, traceable, and scalable over its lifecycle.
