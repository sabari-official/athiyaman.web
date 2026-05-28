03_CASCADE_RULES.md
=========================================================
ATHIYAMAN PLATFORM
DIGITAL INDIA (PHASE 1)

FOREIGN KEY CASCADE RULES

Version: 1.1
Status: Approved
=========================================================
PURPOSE
This document defines the behavior of all Foreign Keys when records are:
Deleted
Updated
Archived
Soft Deleted
Goals:
Data Integrity

Audit Preservation

Payment Preservation

Historical Tracking

No Accidental Data Loss

CASCADE RULE TYPES
CASCADE
ON DELETE CASCADE
Meaning:
Parent Deleted

↓

Child Deleted Automatically

RESTRICT
ON DELETE RESTRICT
Meaning:
Parent Cannot Be Deleted

Until Child Records Removed

SET NULL
ON DELETE SET NULL
Meaning:
Parent Deleted

↓

Reference Becomes NULL

↓

History Preserved

DELETION STRATEGY
Athiyaman uses:
SOFT DELETE
for most critical records.
Never physically delete:
Users

Teams

Claims

Payments

Waste Records

Audit Logs

MODULE 1 — AUTHENTICATION
users → user_profiles
user_profiles.user_id

ON DELETE CASCADE
ON UPDATE CASCADE
Reason:
Profile belongs to User

users → user_sessions
user_sessions.user_id

ON DELETE CASCADE
ON UPDATE CASCADE
Reason:
Sessions have no value
without user.

users → rules_acceptance
rules_acceptance.user_id

ON DELETE CASCADE
ON UPDATE CASCADE

MODULE 2 — DOCUMENTS
users → user_documents
user_documents.user_id

ON DELETE CASCADE
ON UPDATE CASCADE

users → user_documents.verified_by
verified_by

ON DELETE SET NULL
ON UPDATE CASCADE
Reason:
Keep verification history
even if admin account removed.

MODULE 3 — LEADER APPLICATIONS
users → leader_applications.reviewed_by
reviewed_by

ON DELETE SET NULL
ON UPDATE CASCADE

MODULE 4 — TEAM MANAGEMENT
teams → team_members
team_members.team_id

ON DELETE RESTRICT
ON UPDATE CASCADE
Reason:
Cannot remove team
while members exist.

users → team_members
member_id

ON DELETE RESTRICT
ON UPDATE CASCADE
Reason:
Member history preserved.

users → teams.leader_id
leader_id

ON DELETE RESTRICT
ON UPDATE CASCADE
Reason:
Cannot delete team leader
while owning team.

MODULE 5 — REFERRALS
teams → referral_codes
team_id

ON DELETE RESTRICT
ON UPDATE CASCADE
Reason:
Referral history must remain.

users → referral_codes.generated_by
generated_by

ON DELETE SET NULL
ON UPDATE CASCADE

MODULE 6 — LEVELS
teams → team_level_progress
team_id

ON DELETE RESTRICT
ON UPDATE CASCADE

users → personal_level_progress
user_id

ON DELETE RESTRICT
ON UPDATE CASCADE

MODULE 7 — COLLECTION CENTERS
collection_centers → waste_records
center_id

ON DELETE RESTRICT
ON UPDATE CASCADE
Reason:
Waste history must remain.

MODULE 8 — WASTE MANAGEMENT
users → waste_records
user_id

ON DELETE RESTRICT
ON UPDATE CASCADE

users → waste_records.verified_by
verified_by

ON DELETE SET NULL
ON UPDATE CASCADE

waste_records → waste_status_history
waste_record_id

ON DELETE CASCADE
ON UPDATE CASCADE
Reason:
Status history belongs
to waste record.

users → waste_status_history.updated_by
updated_by

ON DELETE SET NULL
ON UPDATE CASCADE

MODULE 9 — CLAIMS
users → reward_claims
user_id

ON DELETE RESTRICT
ON UPDATE CASCADE
Reason:
Claims are financial records.

users → reward_claims.reviewed_by
reviewed_by

ON DELETE SET NULL
ON UPDATE CASCADE

MODULE 10 — PAYMENTS
reward_claims → payment_transactions
claim_id

ON DELETE RESTRICT
ON UPDATE CASCADE
Reason:
Payment history
must never disappear.

users → payment_transactions
user_id

ON DELETE RESTRICT
ON UPDATE CASCADE

payment_batches → payment_batch_items
batch_id

ON DELETE CASCADE
ON UPDATE CASCADE
Reason:
Batch item belongs to batch.

payment_transactions → payment_batch_items
payment_transaction_id

ON DELETE RESTRICT
ON UPDATE CASCADE

payment_transactions → payment_audit_logs
payment_id

ON DELETE RESTRICT
ON UPDATE CASCADE

users → payment_audit_logs.performed_by
performed_by

ON DELETE SET NULL
ON UPDATE CASCADE

MODULE 11 — NOTIFICATIONS
notifications → notification_logs
notification_id

ON DELETE CASCADE
ON UPDATE CASCADE

users → notification_logs
user_id

ON DELETE CASCADE
ON UPDATE CASCADE

users → notifications.created_by
created_by

ON DELETE SET NULL
ON UPDATE CASCADE

users → announcements.created_by
created_by

ON DELETE SET NULL
ON UPDATE CASCADE

MODULE 12 — AUDIT
users → audit_logs
user_id

ON DELETE SET NULL
ON UPDATE CASCADE
Reason:
Audit history
must remain forever.

IMMUTABLE AUDIT RULE
audit_logs
INSERT     Allowed

UPDATE     Forbidden

DELETE     Forbidden

MODULE 13 — ANALYTICS
Analytics snapshots have:
No Foreign Keys
No cascade rules required.

MODULE 14 — SYSTEM
users → system_settings.updated_by
updated_by

ON DELETE SET NULL
ON UPDATE CASCADE

CASCADE PRIORITY MATRIX
CASCADE
user_profiles

user_sessions

rules_acceptance

user_documents

waste_status_history

notification_logs

payment_batch_items

RESTRICT
teams

team_members

waste_records

reward_claims

payment_transactions

collection_centers

SET NULL
audit_logs

payment_audit_logs

leader_applications

notifications

announcements

verification_records

IMPORTANT DATABASE POLICY
Never Physically Delete

Users

Teams

Claims

Payments

Waste Records

Audit Logs
Use:
deleted_at TIMESTAMP

deleted_by UUID
instead.

IMPLEMENTATION ORDER
1. Create Tables

2. Create Foreign Keys

3. Apply Cascade Rules

4. Create Indexes

5. Create Constraints

6. Test Deletion Scenarios

