# Athiyaman Platform - Operations & Workflows Manual
## Phase 1 – Digital India Comprehensive Operational Blueprint

---

## 1. Operations Overview

The Athiyaman Platform’s operational structure is split into four primary domains, each designed to maintain data integrity, security, and administrative transparency.

*   **Platform Operations:** Manages baseline infrastructure services, including JWT session states, API gateway traffic routing, in-app notification routing, geolocated collection maps, and automated data logging.
*   **Administrative Operations:** Handles daily business operations performed by verified administrators. Includes vetting team leader applications, auditing personal documents, verifying waste photo weights, reviewing level progress claims, and recording bank payout references.
*   **Developer Operations:** Tech-admin operations managed by system developers. Includes server diagnostic monitoring, database backup/recovery scripts, error tracking audits, and feature-flag releases.
*   **Business Operations:** Focuses on community-level growth, including team leader recruitment, referral distributions, team expansion targets, physical waste collection, and financial reward payments.
*   **Operational Objectives:**
    *   *Zero Unverified Payouts:* Every rupee paid out is backed by verified personal or team milestones.
    *   *Queue Efficiency:* Vetting queues maintain a turnaround time of under $24\text{ hours}$ to prevent backlogs.
    *   *Complete Traceability:* Every action, update, and decision is logged in an immutable, auditable database table.

---

## 2. Workflow Principles

Every process on the Athiyaman Platform is guided by six core principles:

```
┌────────────────────────────────────────────────────────┐
│             Approval-Based Processing                  │
├────────────────────────────────────────────────────────┤
│             Verification-Based Processing              │
├────────────────────────────────────────────────────────┤
│                 Immutable Auditability                 │
├────────────────────────────────────────────────────────┤
│                 Full Path Traceability                 │
├────────────────────────────────────────────────────────┤
│              Relational Data Integrity                 │
├────────────────────────────────────────────────────────┤
│              Operational Accountability                │
└────────────────────────────────────────────────────────┘
```

*   **Approval-Based Processing:** Access permissions, leader registrations, reward releases, and bank transactions are locked by default. They are released only after manual audit checks and explicit administrator sign-offs.
*   **Verification-Based Processing:** Claims are verified using physical evidence. Waste records require clear photo proofs from scale readouts, geocoded metadata checks, and collection center receipts before approval.
*   **Auditability:** Every state-mutating operation (such as updating bank details or changing claim status) writes a permanent entry to the audit logs, capturing the user, timestamp, IP, and device context.
*   **Traceability:** Data records are linked to their source. Every waste record, payout claim, and referral code tracks its entire lifecycle back to its origin.
*   **Data Integrity:** Enforces database constraints and transaction boundaries to prevent incomplete data states or record orphans during operations.
*   **Accountability:** Admins and developers cannot make arbitrary database modifications. All changes must occur through verified accounts using authorized platform interfaces.

---

## 3. User Lifecycle Workflow

A citizen's journey from a general visitor to an active participant follows a structured progression pathway:

```
                  [ UNREGISTERED VISITOR ]
                             │
                             ▼ (Submits Application)
                  [ LEADER APPLICATION ]
                             │
                             ▼ (Admin Audits Aadhaar & Location)
                    [ ADMIN APPROVAL ]
                             │
                             ▼ (SMS/Email Notification)
               [ LEADER REFERRAL CODE ISSUED ]
                             │
                             ▼ (Sign Up with Code)
                   [ LEADER REGISTRATION ]
                             │
                             ▼ (Submits Bank Details)
                 [ 100% PROFILE COMPLETION ]
                             │
                             ▼ (Accepts Terms click-wrap)
                 [ PLATFORM RULES ACCEPTED ]
                             │
                             ▼ (Dashboard Access Granted)
                 [ ACTIVE PLATFORM MEMBER ]
```

1.  **Visitor Application:** The visitor learns about platform objectives on the public website and submits a Team Leader application.
2.  **Admin Review:** The administrator vets the applicant's identity documents, home address records, and regional district capacity.
3.  **Approval Decision:** Approving an application triggers registration scripts, generating a single-use `LEADER_REFERRAL` code.
4.  **Referral Issuance:** The registration link and referral code are delivered to the approved applicant via official email/SMS.
5.  **Account Registration:** The applicant enters their credentials, validates their mobile number using an OTP, and creates their user profile.
6.  **Profile Completion:** The user submits their personal photo, physical address, encrypted Aadhaar, bank details, and nominee information to reach $100\%$ completeness.
7.  **Rules Acceptance:** The user accepts the platform rules via a click-wrap checkbox.
8.  **Platform Access:** Once profile checks are complete, dashboard locks are released, allowing active platform participation.

---

## 4. Leader Application Workflow

*   **Submission Process:** Visitors access the `Become Team Leader` page and submit their *Name*, *Phone*, *Email*, *Aadhaar*, *District*, *Pincode*, *Address*, and *Reason for Joining*.
*   **Vetting Queue Routing:** Newly submitted applications are logged with a `PENDING` status, routing them to the Admin Application Queue.
*   **Approval Flow:** Admins review details, confirm address records, and verify regional district capacity. Clicking `Approve` registers the applicant as an approved user and triggers code generation.
*   **Rejection Flow:** If details are invalid, the Admin clicks `Reject`, enters a rejection reason, and updates the application to `REJECTED`.
*   **Status Indicators:** Applications progress through standard status states:
    ```
    [SUBMITTED] -> [PENDING_REVIEW] -> [APPROVED] OR [REJECTED]
    ```
*   **Notifications:** Approved applicants receive a signup SMS/Email. Rejected applicants receive a notification explaining the rejection.
*   **Audit Trails:** Every application status change writes an entry to the audit log, capturing the admin ID and timestamp.
*   **Failure Scenarios:** Inputs containing duplicate phone numbers, existing emails, or invalid pincodes are blocked at the gateway level, returning error alerts.

---

## 5. Referral Workflow

The referral engine manages registration security using two distinct referral pathways.

### 5.1 Admin Referrals (`LEADER_REFERRAL`)
*   **Creation:** Generated by administrators to register approved team leaders.
*   **Activation:** Activated automatically upon generation.
*   **Usage Constraints:** Restriced to single-use applications.
*   **Expiry Rules:** Expires automatically $48\text{ hours}$ after generation.
*   **Deactivation:** Can be manually disabled by an Admin to block signups.

### 5.2 Leader Referrals (`TEAM_REFERRAL`)
*   **Creation:** Generated by active Team Leaders to recruit local members.
*   **Activation:** Activated automatically upon creation.
*   **Usage Constraints:** Multi-use capacity restricted to the leader's current level requirements (e.g., Level 1 caps referrals at $10\text{ members}$).
*   **Expiry Rules:** Expires automatically when the leader completes their active level or manually deactivates the code.
*   **Deactivation:** Leaders can manually disable codes to pause signups.

### 5.3 Technical Workflows
*   **Referral Lifecycle:**
    ```
    [GENERATED] -> [ACTIVE] -> [MAX_CAPACITY / EXPIRED / MANUALLY_DISABLED]
    ```
*   **Verification:** The registration service queries the database to confirm the referral code exists, is marked active, has usage capacity, and is not expired.
*   **Auditing:** Code generations, activations, uses, and deactivations write entries to the audit logs, tracking the user ID and IP address.
*   **Failure Scenarios:** Expired or fully utilized codes are rejected, returning clear error alerts.

---

## 6. Leader Registration Workflow

*   **Activation Step:** Approved leaders receive a secure signup URL containing their single-use `LEADER_REFERRAL` code.
*   **Credential Creation:** The applicant enters their username, email, phone number, and password on the signup form.
*   **OTP Verification:** The registration service delivers a $6$-digit OTP to the applicant's mobile number. The applicant must submit this code within $5\text{ minutes}$ to verify their contact details.
*   **Account Activation:** Successful OTP verification registers the user in the database with a `LEADER` role, marked as active.
*   **Notification Triggers:** The system sends a welcome email containing getting-started guides and profile completion instructions.
*   **Audit Logging:** Logs the registration event, linking the leader to the admin ID who approved their application.

---

## 7. Member Registration Workflow

*   **Referral Verification:** The visitor accesses the registration portal using a `TEAM_REFERRAL` link shared by a Team Leader. The registration service validates the code's active status and usage count.
*   **Account Registration:** The applicant enters their username, email, contact phone, and password.
*   **OTP Verification:** The registration service sends a $6$-digit verification OTP via SMS. The user must verify their phone number within $5\text{ minutes}$.
*   **Account Activation:** Successful OTP validation registers the user with a `MEMBER` role, linking them to the leader's team.
*   **Notification Triggers:** Sends a welcome alert to the member and a recruitment update notification to the Team Leader.
*   **Audit Logging:** Logs the registration event in the audit trail, linking the member's profile to the referral code used.

---

## 8. Profile Completion Workflow

*   **Required Fields Checklist:** Users must submit their personal details, address details, Aadhaar number, banking details, and nominee information.
*   **Profile Progress Scoring:** The backend calculates a dynamic completeness score as follows:
    *   *Section A: Personal details* $\rightarrow 20\%$
    *   *Section B: Contact details* $\rightarrow 10\%$
    *   *Section C: Address details* $\rightarrow 10\%$
    *   *Section D: Aadhaar details* $\rightarrow 20\%$
    *   *Section E: Bank details* $\rightarrow 30\%$
    *   *Section F: Nominee details* $\rightarrow 10\%$
*   **Document Uploads & Vetting:** Users must upload clear scans of their Aadhaar card and banking passbook (allowed: JPG, JPEG, PNG, PDF; blocked: EXE, BAT, JS, SH, DLL). Upload service validates actual file structure (magic bytes), dynamically strips metadata/EXIF headers, renames files using UUIDv7, stores files outside public directories, NGINX blocks execution, and access is granted only via temporary secure URLs.
*   **Dashboard Lockouts:** Dashboards remain locked until the profile completeness score reaches $100\%$, preventing users from logging waste or claiming rewards.
*   **Notification triggers:** The system sends an email confirmation once the profile score reaches $100\%$.
*   **Restrictions:** Bank accounts and Aadhaar numbers are locked once verified by an Admin. Subsequent edits require a support request, logging a high-priority audit entry.

---

## 9. Rules Acceptance Workflow

*   **Display Requirements:** A full-screen click-wrap window presents the platform's terms of use, privacy policy, and program rules.
*   **Acceptance Capture:** Users must scroll to the bottom of the terms and select the explicit *"I Agree"* checkbox to enable the submission button.
*   **Consent Storage:** Selecting I Agree records consent in the user's database entry, capturing their user ID, IP address, and timestamp.
*   **Dashboard Release:** Successful rules acceptance releases the dashboard locks, granting access to active platform features.
*   **Audit Logging:** Logs the consent event to ensure compliance and traceability.

---

## 10. Team Creation Workflow

*   **Leader Initiation:** Vetted leaders access the team creation screen and enter their team's name, district, neighborhood area, and pincode.
*   **Team Name Validation:** The validation service checks that the name is unique and contains no profanity or special characters.
*   **Team Activation:** Successful validations create the team record, register the team code, assign the leader as the owner, and set the status to `ACTIVE`.
*   **Notification Triggers:** Sends a confirmation email to the leader containing their team details.
*   **Audit Logging:** Logs the team creation event, tracking the leader ID and team code.
*   **Failure Scenarios:** Duplicate team names or invalid pincode entries are blocked, returning error alerts.

---

## 11. Team Membership Workflow

*   **Invitation Routing:** Members sign up using a leader's active `TEAM_REFERRAL` code.
*   **Relational Association:** The signup service verifies the code and creates an entry in `team_members`, linking the member to the leader's team.
*   **Roster Updates:** Adds the member's profile to the leader's team roster and updates the active member count.
*   **Notification Triggers:** Sends a registration alert to the member and a recruitment update notification to the Team Leader.
*   **Audit Logging:** Logs the join event, linking the member's profile to the team's record.

---

## 12. Team Progress Workflow (Levels 1–6)

*   **Growth Tracking:** The system monitors active member counts for the team:
    *   *Level 1:* $10\text{ Members}$
    *   *Level 2:* $90\text{ Members}$
    *   *Level 3:* $720\text{ Members}$
    *   *Level 4:* $5,040\text{ Members}$
    *   *Level 5:* $30,240\text{ Members}$
    *   *Level 6:* $50,000\text{ Members}$
*   **Progress Calculation:** Calculated dynamically as members join and complete their profile verifications.
*   **Milestone Reached:** Reaching a member threshold marks the active level status as `COMPLETED` and unlocks the level reward claim button.
*   **Reward Eligibility:** Leaders become eligible for rewards (₹100 to ₹5,000) based on completed levels.
*   **Notification Triggers:** Sends a milestone congratulations alert to the leader's dashboard.

---

## 13. Personal Progress Workflow (Levels 7–11)

*   **Progress Auditing:** The system tracks individual waste collection progress (Levels 7–11) for all registered users:
    *   *Level 7:* $10\text{ KG}$ Approved Waste
    *   *Level 8:* $10\text{ KG}$ Approved Waste
    *   *Level 9:* $10\text{ KG}$ Approved Waste
    *   *Level 10:* $10\text{ KG}$ Approved Waste
    *   *Level 11:* $10\text{ KG}$ Approved Waste
*   **Progress Calculations:** Weight values are calculated based on approved waste records.
*   **Level Completion:** Reaching the $10\text{ KG}$ approved waste threshold marks the active personal level as `COMPLETED` and resets the active weight balance to $0\text{ KG}$ for the next level.
*   **Reward Eligibility:** Reaching a milestone enables the `Claim Reward` button (₹10,000 to ₹50,000) for the user.
*   **Notification Triggers:** Sends a personal milestone alert to the user's dashboard.

---

## 14. Referral Eligibility Workflow

*   **Referral Capacity Limits:** Referral usage limits are linked to the leader's level milestones.
*   **Milestone Upgrades:** Completing a level prompts the leader to generate a new referral code, updating invite capacities for the next level.
*   **Code Expirations:** The old referral code is marked as expired, and new registrations are routed through the newly generated code.
*   **Audit Logging:** Logs the referral update event, tracking invite capacities and active codes.

---

## 15. Waste Record Workflow

*   **Submission Details:** Users log collections by submitting the weight in KG, uploading a photo scale proof, and selecting the collection center.
*   **Queue Routing:** Submissions are logged as `PENDING_VERIFICATION`, routing them to the Admin Verification Queue.
*   **Vetting Actions:** Admins review the submission details, verify geocoded metadata, and compare the upload with center receipts.
*   **Verification Outcomes:**
    *   *Approve:* Updates the status to `APPROVED`, updates the user's level progress, and triggers notifications.
    *   *Reject:* Requires an admin comment, updates the status to `REJECTED`, and notifies the user of the rejection.
*   **Status Changes:**
    ```
    [SUBMITTED] -> [PENDING_VERIFICATION] -> [APPROVED] OR [REJECTED]
    ```
*   **Audit Trails:** Every status transition is logged in `waste_status_history`, recording the admin ID, comments, and timestamp.

---

## 16. Waste Verification Workflow (Admin Action)

*   **Vetting Queue Operations:** Admins review pending submissions, opening individual detail pages to audit weight readings and center locations.
*   **Comparison Protocols:** Audits compare claimed weights with physical center receipts to ensure record accuracy.
*   **Approval Decisions:** Clicking `Approve` locks the waste record, updates the user's progress weights, and triggers notifications.
*   **Rejection Decisions:** Clicking `Reject` opens a dialog prompting the Admin to enter the reason for rejection, updating the status and notifying the user.
*   **Audit Trails:** State changes are logged in the audit trail, tracking the admin ID and review details.
*   **Failure Recovery:** If database failures occur, the service aborts calculations and rolls back transactions to keep waste progress logs consistent.

---

## 17. Collection Center Workflow

*   **Center Queries:** Users locate authorized centers by searching pincodes or districts on geocoded maps.
*   **Availability Audits:** The search utility returns only centers marked active by administrators.
*   **Visibility Rules:** Disabled centers are hidden from search queries, protecting users from traveling to inactive locations.
*   **Administrative Operations:** Admins can edit address records, update phone details, or temporarily disable centers for maintenance.

---

## 18. Reward Claim Workflow

*   **Eligibility Checks:** Users become eligible for rewards once the level progression service marks a level status as `COMPLETED`.
*   **Manual Claim Submission:** Reaching a milestone enables the "Claim Reward" button. Users submit claims manually to verify their bank details before payouts are processed.
*   **Vetting Checkpoints:** The claims engine validates that the user's profile is complete, documents are verified, and no other active claims exist for the same level.
*   **Claim Rejection Rules:** Admins can reject claims if identity discrepancies or profile changes are flagged, returning the level progress status to `COMPLETED` for review.
*   **Claim Lifecycle:**
    ```
    [INITIATED] -> [PENDING_AUDIT] -> [APPROVED] OR [REJECTED]
    ```
*   **Audit Trail Logs:** Every claim creation, review, and status update is logged in the audit trail.

---

## 19. Claim Review Workflow (Admin Action)

*   **Vetting Queue Operations:** Admins open pending claims to review the applicant's profile details, Aadhaar credentials, and banking information.
*   **Document Audits:** Vets document scans to verify identity and confirm bank details match profile fields.
*   **Approval Steps:** Clicking `Approve` registers the claim status as `APPROVED`, locks the user's banking details to prevent edits, and routes the transaction to the Payment Queue.
*   **Rejection Steps:** Clicking `Reject` requires an admin comment, updates the status to `REJECTED`, and notifies the user to submit a support request.
*   **Audit Trails:** State updates write logs in the audit trail, tracking the admin ID and review comments.

---

## 20. Payment Queue Workflow

*   **Queue Routing:** Claims approved by Admins are assigned a `PENDING_PAYMENT` status, routing them to the Payment Queue.
*   **Ledger Entries:** Transactions are sorted by approval dates, prioritizing oldest claims first to prevent payment delays.
*   **Admin Disbursements:** Admins access the Payment Queue dashboard to review payment details, using external banking portals to process transfers.
*   **Payment Completions:** After processing, the Admin inputs the transaction reference number and clicks `Mark Paid`, updating the status to `PAID` and notifying the user.

---

## 21. Batch Payment Workflow

*   **Batch Operations:** Admins can group pending claims into a single batch list for processing.
*   **Vetting Reviews:** The system verifies the accounts within the batch, confirming that profiles are complete and banking details match database records.
*   **Disbursement Processing:** The Admin processes the batch transfers externally and uploads the matching transaction log file containing reference IDs.
*   **Processing Results:** The batch utility updates all matching records to `PAID`. Failed transfers are flagged, and the system notifies the Admin to review the affected accounts.
*   **Audit Logging:** Logs the batch payment event, tracking the log file name and the admin ID.

---

## 22. Payment Lifecycle Workflow

The payments engine tracks transactions through five status states:

```
[PENDING_PAYMENT] -> [PROCESSING] -> [PAID] OR [FAILED]
```

*   **Pending (`PENDING_PAYMENT`):** Initial state assigned when a reward claim is approved. Indicates the transaction is waiting in the processing queue.
*   **Processing (`PROCESSING`):** Indicates the Admin is reviewing details and processing the transfer externally.
*   **Paid (`PAID`):** Indicates the payout was successful. The record is locked, showing the bank transaction reference, date, and admin ID.
*   **Failed (`FAILED`):** Indicates the transfer failed due to bank rejection. The claim returns to the processing queue.

---

## 23. Payment Failure Workflow

*   **Failure Detection:** If a transfer fails, the Admin marks the transaction as `FAILED` and logs the failure code returned by the bank.
*   **Recovery Actions:** The service returns the claim to the Payment Queue and locks payments for the account until the bank details are corrected.
*   **Notification Triggers:** Sends an urgent SMS/Email alert to the user, advising them to review and update their banking details.
*   **Resolution Audits:** Once the user corrects their bank details, the Admin reviews the account and unlocks the claim for processing.
*   **Audit Trails:** Failed transactions, detail changes, and payouts are logged in the audit trail to maintain complete accountability.

---

## 24. Notification Workflow

*   **Event Generation:** Key actions trigger notification events in the system.
*   **Delivery Workflows:** The system routes notifications to user dashboards, marking items as `UNREAD` by default.
*   **Read State Tracking:** When a user opens an alert, the interface updates the item to `READ` in the database.
*   **Archiving Actions:** Users can archive old notifications, hiding them from the inbox dashboard.
*   **Notification Lifecycle:**
    ```
    [UNREAD] -> [READ] -> [ARCHIVED]
    ```

---

## 25. Announcement Workflow

*   **Announcement Creation:** Admins author announcements, defining target audiences (`All Users`, `Leaders`, `Members`, `Specific Team`) and optional expiration dates.
*   **Publishing Actions:** Clicking `Publish` delivers the announcement to target users, listing the message on their dashboards.
*   **Expiration Management:** Expired announcements are removed automatically from user dashboards, keeping view panels clean.
*   **Audit Logging:** Logs the announcement creation event, tracking target audiences and the admin ID.

---

## 26. Document Verification Workflow

*   **Document Submissions:** Users upload document scans (Aadhaar cards, bank books) to reach $100\%$ profile completeness.
*   **Vetting Queue Operations:** Uploaded documents are logged with a `PENDING_VERIFICATION` status, routing them to the Document Verification Queue.
*   **Vetting Actions:** Admins review the scans side-by-side with profile fields to ensure records match.
*   **Verification Outcomes:**
    *   *Approve:* Updates the status to `VERIFIED`, updating the profile completeness score.
    *   *Reject:* Updates the status to `REJECTED`, requiring a rejection comment and notifying the user.
*   **Audit Trails:** Status changes write entries to the audit logs, tracking the admin ID and review timestamp.

---

## 27. User Management Workflow

*   **Account Vetting:** Admins open user profiles to review history records, team linkages, and collection logs.
*   **Suspension Actions:** Flags for fraud or duplicate signups prompt Admins to click `Suspend User`, blocking the user's dashboard access.
*   **Reactivation Actions:** Resolving verification issues prompts Admins to click `Reactivate User`, restoring dashboard access.
*   **Password Reset Actions:** Admins can trigger password resets for users, generating a temporary password and forcing a password update upon login.
*   **Audit Logging:** Account suspensions, reactivations, and password resets write entries to the audit logs to maintain accountability.

---

## 28. Team Management Workflow

*   **Team Performance Auditing:** Admins monitor team growth metrics, active member registries, and level progress logs.
*   **Team Member Counter Strategy:** Maintain precalculated `member_count` in the `teams` table to support teams with thousands of members. The database must increment `member_count` when a member joins and decrement it when a member leaves. User dashboards must read `member_count` directly, strictly prohibiting expensive SQL `COUNT` queries on `team_members` to protect connection pools.
*   **Suspension Actions:** Systemic fraud flags prompt Admins to click `Suspend Team`, blocking referral invites and team level calculations.
*   **Reactivation Actions:** Resolving team issues prompts Admins to click `Reactivate Team`, restoring team operations.
*   **Audit Logging:** Team suspensions and reactivations write entries to the audit logs, tracking the team code and admin ID.

---

## 29. Collection Center Management Workflow

*   **Center Operations:** Admins add centers by defining the name, address, geocodes, phone, and operational hours.
*   **Edits & Updates:** Admins can modify details, correcting addresses or geocodes.
*   **Visibility Controls:** Admins can enable or disable centers. Disabling a center hides it from search results, protecting users from traveling to inactive locations.
*   **Audit Logging:** Center changes and status updates are logged in the audit trail, tracking center IDs and admin details.

---

## 30. Analytics Workflow

*   **Data Aggregation:** The system aggregates metrics asynchronously during off-peak hours to prevent database lockups.
*   **Snapshot Storage:** Precalculated metrics are stored in `analytics_snapshots` tables.
*   **Dashboard Visualizations:** Dashboard charts fetch precalculated snapshots, rendering platform growth, waste collection, and payment metrics.
*   **Analytical Retention:** Historical snapshots are retained for $7\text{ years}$ to support compliance and performance reporting.

---

## 31. Audit Workflow

*   **Log Captures:** System mutations write entries to the database audit log.
*   **Data Security:** The audit table blocks update and delete queries, protecting logs from modification.
*   **Advanced Search Queries:** Admins and Developers locate entries by filtering logs by *User Account*, *IP Address*, or *Date Range*.
*   **Report Exports:** Admins can export audit log filters as secure PDF or CSV files for review.

---

## 32. Security Incident Workflow

*   **Threat Detection:** Consecutively failed logins ($5\text{ attempts}$ within an hour per IP) trigger security alerts.
*   **Incident Isolation:** The system locks the affected account, blocking access attempts.
*   **Developer Diagnostics:** Developers review incident details on security logs to determine the threat source.
*   **Incident Resolution:**
    *   *Safe:* The Developer unlocks the account, forcing a password update.
    *   *Hostile:* The Developer blocks the offending IP and logs the security incident.

---

## 33. Backup Workflow

*   **Scheduled Backups:** Daily full backups and hourly incremental backups run automatically during off-peak hours.
*   **Manual Backups:** Developers can trigger manual backups before deploying feature updates.
*   **System Restores:** If a system failure occurs, the Developer can restore the database using the Backup Center utility.
*   **Recovery Audits:** Point-in-time recovery validations verify restored database states to ensure data consistency.

---

## 34. Monitoring Workflow

*   **Diagnostics Diagnostics:** System diagnostics capture CPU usage, memory utilization, and active database connection pool stats.
*   **Diagnostics Metrics:** Grafana dashboards track system health, alert developers to bottlenecks, and log API response speeds.
*   **Crash Integrations:** System crashes and coding exceptions are sent to the Developer Portal via Sentry for diagnosis.

---

## 35. Feature Control Workflow

*   **Feature Flag Management:** Developers can toggle system modules on or off using administrative feature flags.
*   **Flag Deployments:** Activating or deactivating modular flags changes interface configurations instantly without requiring code deploys.
*   **Audit Logging:** Logs feature flag changes in the audit trail, tracking the developer ID and active configurations.

---

## 36. Developer Operations Workflow

*   **Infrastructure Audits:** Developers review system diagnostics daily to identify and resolve performance bottlenecks.
*   **Deployment Operations:** Updates are validated on staging environments before deploying containers to production.
*   **Rollback Workflows:** If a production update fails, the DevOps team rolls back the application containers to the latest stable release.

---

## 37. Escalation Procedures

*   **Technical Escalation:** Infrastructure bottlenecks or API crashes are routed to the Lead Developer.
*   **Operational Escalation:** Verification delays or queue bottlenecks are routed to the Administrative Manager.
*   **Security Escalation:** PII leaks or security threats are routed to the Security Officer.
*   **Payment Escalation:** Payment reference errors or banking failures are escalated to the Finance Director.

---

## 38. Operational Reports

*   **Daily Summaries:** Details daily signups, logged waste weights, and processed payouts.
*   **Weekly Summaries:** Tracks growth metrics, active collection center volumes, and payment queues.
*   **Monthly Summaries:** Tracks performance metrics, regional team growth, and budget records.
*   **Audit Exports:** Secure summaries exported by Admins to support regulatory audits.

---

## 39. Audit Requirements

*   **Audited Events:** Includes user logins, role creations, document reviews, waste approvals, and payment transactions.
*   **Access Permissions:** Audit logs are visible only to Admins and Developers through read-only portals.
*   **Data Retention:** Logs are retained for $7\text{ years}$ to meet compliance requirements.

---

## 40. Operational KPIs

*   **User Growth Rates:** Targets standard citizen registration rates across regions.
*   **Team Growth Milestones:** Tracks the number of active teams reaching Levels 1 to 6.
*   **Waste Collection Volumes:** Measures approved weights processed at active centers.
*   **Claim Turnaround Times:** Targets average queue review times of under $24\text{ hours}$.
*   **Payment Processing Latencies:** Measures average processing times from claim approvals to payouts.

---

## 41. Disaster Recovery Operations

*   **Recovery Restores:** Point-in-time recovery validations verify restored database states to ensure data consistency.
*   **Database Validations:** Validation scripts check relational constraints and keys after a restore.
*   **Recovery Audits:** The development team verifies system functions before redirecting DNS traffic back to the primary environment.

---

## 42. Business Continuity

*   **Service Redundancy:** Stateless API servers run across independent host regions to prevent outages.
*   **Operational Continuity:** Vetting queues can be managed by other administrators in the event of local office disruptions.
*   **System Continuities:** Backups are stored in independent cloud storage locations, ensuring recovery options in case of major host outages.

---

## 43. Future Operational Expansion

*   **Phase 2 - Skill India:** The modular backend supports adding physical training courses and trainer roles without altering core profiles.
*   **Phase 3 - Clean India:** Extends regional collection registers to support advanced regional processing and logistics tracking.
*   **Financial Integrations:** Swapping manual banking reference logs for direct UPI or API payouts is supported by abstract payment interfaces.

---

## 44. Conclusion

This Operations & Workflows Manual (`03_ADMIN_OPERATIONS.md`) provides the absolute operational, verification, vetting, auditing, and backup blueprints for the Athiyaman Platform – Digital India Phase 1. By detailing user lifecycle milestones, referral mechanics, verification flows, security procedures, and disaster recovery rules, it serves as a complete reference for operational teams. All daily management tasks, user vetting, and system audits must adhere strictly to these principles, ensuring the platform remains highly secure, transparent, traceable, and scalable over its lifecycle.
