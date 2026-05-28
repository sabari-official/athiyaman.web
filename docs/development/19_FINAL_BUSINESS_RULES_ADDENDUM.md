=========================================================
ATHIYAMAN PLATFORM
DIGITAL INDIA (PHASE 1)

FINAL BUSINESS RULES ADDENDUM

Version: 1.0
Status: APPROVED

Purpose:
This document contains final business rules,
edge cases, security rules, operational rules,
and implementation decisions that were finalized
after the core architecture documents.

This document is authoritative and supplements
all previous project documents.
=========================================================
1. TEAM LEVEL OWNERSHIP
Levels:
1, 2, 3, 4, 5, 6

Owner:
Team

Progress Source:
teams.member_count

Visible To:
All Team Members

Reward Owner:
Leader

Members can view progress.
Members do not own the reward.

2. PERSONAL LEVEL OWNERSHIP
Levels:
7, 8, 9, 10, 11

Owner:
Individual User

Progress Source:
Approved Waste Records

Visible To:
Individual User

Reward Owner:
Individual User

3. LEVEL COMPLETION RULE
Levels must be completed sequentially.
Cannot skip levels.
Cannot claim future levels.
Previous level must be completed before next level becomes active.

4. LEVEL REVERSAL RULE
Completed Levels Never Reverse.
Example:
Level 2 Completed (Current Members = 95)
Later Members Leave (Current Members = 89)
Result: Level 2 remains completed.

5. LEADER REFERRAL RULES
Created By: Admin
Purpose: Leader Registration
Usage Limit: 1
Auto Expire: After Successful Registration
Only One Leader Account may be created from a Leader Referral.

6. TEAM REFERRAL RULES
Created By: Leader
Purpose: Member Registration
Usage Limits:
Level 1 = 10
Level 2 = 90
Level 3 = 720
Level 4 = 5040
Level 5 = 30240
Level 6 = 50000

7. REFERRAL ACTIVATION RULE
Only One Active Team Referral may exist at a time.
New Referral cannot be generated until current referral expires or reaches maximum usage.

8. REFERRAL EXPIRATION RULE
When used_count >= max_usage, Referral Automatically Expires (is_active = FALSE).

9. REFERRAL GENERATION ELIGIBILITY
Level 1 Referral: Available Immediately After Team Creation
Level 2 Referral: Available Only After Level 1 Completion
Level 3 Referral: Available Only After Level 2 Completion
Level 4 Referral: Available Only After Level 3 Completion
Level 5 Referral: Available Only After Level 4 Completion
Level 6 Referral: Available Only After Level 5 Completion

10. CLAIM LOCK RULE
When Claim Created -> Current Level Locked -> User Cannot Create Another Claim -> Admin Review Required -> Approve / Reject -> Level Unlocked

11. WASTE DURING CLAIM LOCK
Waste Submitted During Claim Lock Must Not Be Lost.
Waste is stored in Pending Progress Queue.
After Claim Resolution, Progress Applied To Next Eligible Level.

12. WASTE APPROVAL RULE
Only Approved Waste Contributes To Progress.

13. WASTE REJECTION RULE
Rejected Waste Does Not Count Toward Personal Levels, Reward Eligibility, or Analytics Totals.

14. PAYMENT FAILURE RULE
If Payment Fails -> Payment Status = FAILED -> Claim Status Remains APPROVED -> Admin Can Retry Payment -> No New Claim Required

15. PAYMENT PROVIDER RULE
All Payment Logic must use Payment Provider Interface.
Methods:
create_batch()
approve_payment()
mark_paid()
mark_failed()
Initial Provider: Manual Bank Upload
Future Providers: RazorpayX, Bank APIs, Other Providers

16. TEAM LEADER SUSPENSION RULE
When Leader Suspended -> Team Becomes Read Only -> Members Can View Data -> Cannot Generate Referrals -> Cannot Create Claims -> Cannot Receive Payments -> Until Admin Action

17. DOCUMENT REJECTION RULE
Rejected Documents Can Be Reuploaded.
Previous Version Must Be Preserved For Audit History.

18. COLLECTION CENTER RULE
Disabled Collection Center Cannot Accept New Waste Records.
Existing Waste Records Remain Preserved.

19. MEMBER COUNTER RULE
teams.member_count Is Source Of Truth For Team Progress.
Do Not Calculate Team Size Using COUNT Queries For Dashboards.
Maintain Using: Database Trigger

20. AADHAAR SECURITY RULE
Store: aadhaar_hash, aadhaar_encrypted
Never Store: Plain Aadhaar Number
Display: XXXX-XXXX-1234

21. BANK SECURITY RULE
Store: Encrypted Account Number
Display: XXXXXX1234
Store Plain: IFSC

22. FILE STORAGE STRUCTURE
uploads/
  profile_photos/
  aadhaar/
  bank_documents/
  nominee_documents/
  waste_images/
  temp/
  quarantine/

23. AUDIT IMMUTABILITY RULE
audit_logs:
INSERT = Allowed
UPDATE = Forbidden
DELETE = Forbidden
Audit logs are permanent.

24. DATA RETENTION POLICY
Audit Logs: Forever
Payments: Forever
Claims: Forever
Notifications: 1 Year
Sessions: 90 Days
System Logs: 180 Days

25. ENVIRONMENT STRATEGY
Each Environment (LOCAL, DEVELOPMENT, STAGING, PRODUCTION) Must Have:
Separate Database, Separate Secrets, Separate Storage, Separate Email Configuration, Separate Payment Configuration

26. BACKGROUND JOBS
Background Processing Stack: Celery + Redis
Used For: Email, Notifications, Reports, Payment Processing, Scheduled Jobs

27. FINAL PROJECT DECISIONS
Backend: FastAPI
Database: PostgreSQL 17
ORM: SQLAlchemy
Migration: Alembic
Authentication: JWT
Password Hash: Argon2
Primary Keys: UUIDv7
File Storage: Local Storage
Hosting: Linux + DirectAdmin
Frontend: React + TypeScript + Tailwind
