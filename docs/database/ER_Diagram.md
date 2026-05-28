05_ER_DIAGRAM.md
=========================================================
ATHIYAMAN PLATFORM
DIGITAL INDIA (PHASE 1)

ENTITY RELATIONSHIP DIAGRAM (ERD)

Version: 1.1
Status: Approved
=========================================================
PURPOSE
This document defines the complete relationship structure between all database entities.
Used For:
PostgreSQL Schema Development
SQLAlchemy Relationship Mapping
Alembic Migrations
API Development
Future Maintenance

COMPLETE ENTITY RELATIONSHIP MAP
users
│
├── user_profiles
│
├── user_documents
│
├── user_sessions
│
├── rules_acceptance
│
├── leader_applications (reviewed_by)
│
├── teams (leader_id)
│
├── team_members
│
├── referral_codes (generated_by)
│
├── personal_level_progress
│
├── waste_records
│
├── reward_claims
│
├── payment_transactions
│
├── notifications
│
├── notification_logs
│
├── audit_logs
│
└── system_logs

MODULE 1 — USER MANAGEMENT
users → user_profiles
Relationship:
One User
↓

One Profile
Type:
1 : 1
Foreign Key:
user_profiles.user_id
→ users.id

users → user_documents
Relationship:
One User
↓

Many Documents
Type:
1 : M
Foreign Key:
user_documents.user_id
→ users.id
Document Types:
AADHAAR

BANK_PROOF

PROFILE_PHOTO

NOMINEE_PROOF

users → user_sessions
Relationship:
One User
↓

Many Sessions
Type:
1 : M
Foreign Key:
user_sessions.user_id
→ users.id

users → rules_acceptance
Relationship:
One User
↓

One Rules Acceptance Record
Type:
1 : 1
Foreign Key:
rules_acceptance.user_id
→ users.id

MODULE 2 — LEADER APPLICATIONS
users → leader_applications
Relationship:
One Admin

↓

Many Reviews
Type:
1 : M
Foreign Key:
leader_applications.reviewed_by
→ users.id

MODULE 3 — TEAM MANAGEMENT
users → teams
Relationship:
One Leader

↓

One Team
Type:
1 : 1
Constraint:
UNIQUE(leader_id)
Foreign Key:
teams.leader_id
→ users.id

teams → team_members
Relationship:
One Team

↓

Many Members
Type:
1 : M
Foreign Key:
team_members.team_id
→ teams.id

users → team_members
Relationship:
One User

↓

One Team Membership
Type:
1 : 1
Constraint:
UNIQUE(member_id)
Foreign Key:
team_members.member_id
→ users.id

MODULE 4 — REFERRALS
teams → referral_codes
Relationship:
One Team

↓

Many Referral Codes
Type:
1 : M
Foreign Key:
referral_codes.team_id
→ teams.id

users → referral_codes
Relationship:
One User

↓

Many Generated Referrals
Type:
1 : M
Foreign Key:
referral_codes.generated_by
→ users.id

MODULE 5 — LEVEL SYSTEM
levels → team_level_progress
Relationship:
One Level

↓

Many Teams
Type:
1 : M
Foreign Key:
team_level_progress.level_number
→ levels.level_number

teams → team_level_progress
Relationship:
One Team

↓

Levels 1-6 Progress
Type:
1 : M
Foreign Key:
team_level_progress.team_id
→ teams.id

levels → personal_level_progress
Relationship:
One Level

↓

Many Users
Type:
1 : M
Foreign Key:
personal_level_progress.level_number
→ levels.level_number

users → personal_level_progress
Relationship:
One User

↓

Levels 7-11 Progress
Type:
1 : M
Foreign Key:
personal_level_progress.user_id
→ users.id

MODULE 6 — COLLECTION CENTERS
collection_centers → waste_records
Relationship:
One Collection Center

↓

Many Waste Records
Type:
1 : M
Foreign Key:
waste_records.center_id
→ collection_centers.id

MODULE 7 — WASTE MANAGEMENT
users → waste_records
Relationship:
One User

↓

Many Waste Records
Type:
1 : M
Foreign Key:
waste_records.user_id
→ users.id

waste_records → waste_status_history
Relationship:
One Waste Record

↓

Many Status Changes
Type:
1 : M
Foreign Key:
waste_status_history.waste_record_id
→ waste_records.id

MODULE 8 — CLAIMS
users → reward_claims
Relationship:
One User

↓

Many Claims
Type:
1 : M
Foreign Key:
reward_claims.user_id
→ users.id

MODULE 9 — PAYMENTS
reward_claims → payment_transactions
Relationship:
One Claim

↓

One Payment
Type:
1 : 1
Constraint:
UNIQUE(claim_id)
Foreign Key:
payment_transactions.claim_id
→ reward_claims.id

users → payment_transactions
Relationship:
One User

↓

Many Payments
Type:
1 : M
Foreign Key:
payment_transactions.user_id
→ users.id

payment_batches → payment_batch_items
Relationship:
One Batch

↓

Many Payments
Type:
1 : M
Foreign Key:
payment_batch_items.batch_id
→ payment_batches.id

payment_transactions → payment_batch_items
Relationship:
One Payment

↓

One Batch Item
Type:
1 : 1
Foreign Key:
payment_batch_items.payment_transaction_id
→ payment_transactions.id

payment_transactions → payment_audit_logs
Relationship:
One Payment

↓

Many Audit Logs
Type:
1 : M
Foreign Key:
payment_audit_logs.payment_id
→ payment_transactions.id

MODULE 10 — NOTIFICATIONS
notifications → notification_logs
Relationship:
One Notification

↓

Many Deliveries
Type:
1 : M
Foreign Key:
notification_logs.notification_id
→ notifications.id

users → notification_logs
Relationship:
One User

↓

Many Notifications Received
Type:
1 : M
Foreign Key:
notification_logs.user_id
→ users.id

MODULE 11 — AUDIT
users → audit_logs
Relationship:
One User

↓

Many Audit Events
Type:
1 : M
Foreign Key:
audit_logs.user_id
→ users.id

MODULE 12 — ANALYTICS
analytics_snapshots
Relationship:
Independent Table

No Foreign Keys
Purpose:
Historical Metrics Storage

MODULE 13 — SYSTEM SETTINGS
system_settings
Relationship:
Independent Table

Configuration Storage

HIGH LEVEL ER DIAGRAM
users
 │
 ├──── user_profiles
 ├──── user_documents
 ├──── user_sessions
 ├──── rules_acceptance
 │
 ├──── teams
 │        │
 │        ├──── team_members
 │        │
 │        ├──── referral_codes
 │        │
 │        └──── team_level_progress
 │
 ├──── personal_level_progress
 │
 ├──── waste_records
 │        │
 │        └──── waste_status_history
 │
 ├──── reward_claims
 │        │
 │        └──── payment_transactions
 │                  │
 │                  ├──── payment_batch_items
 │                  └──── payment_audit_logs
 │
 ├──── notification_logs
 │
 └──── audit_logs

collection_centers
 │
 └──── waste_records

notifications
 │
 └──── notification_logs

payment_batches
 │
 └──── payment_batch_items

levels
 │
 ├──── team_level_progress
 │
 └──── personal_level_progress

TOTAL DATABASE SUMMARY
Total Tables              : 27

Core Tables               : 8

Transaction Tables        : 9

Tracking Tables           : 6

Configuration Tables      : 4

Primary Keys              : UUIDv7

Relationships             : Fully Defined

Constraints               : Fully Defined

Indexes                   : Fully Defined

Cascade Rules             : Fully Defined

