FINAL DATABASE ARCHITECTURE
Athiyaman Platform - Digital India (Phase 1)

Total Tables
Core Tables: 27

Future Phase Ready:
Skill India
Clean India

Database:
PostgreSQL

Primary Keys:
UUIDv7

ORM:
SQLAlchemy

Migration:
Alembic

MODULE 1 - AUTHENTICATION
users
id UUIDv7 PK

username VARCHAR(50) UNIQUE

phone_number VARCHAR(15) UNIQUE

password_hash TEXT

role ENUM

user_status ENUM

is_verified BOOLEAN

failed_login_attempts INTEGER

locked_until TIMESTAMP

last_login TIMESTAMP

created_at TIMESTAMP

updated_at TIMESTAMP
Role Values
MEMBER
LEADER
ADMIN
DEVELOPER
User Status
PENDING
ACTIVE
SUSPENDED
BLOCKED
DELETED
Indexes
username
phone_number
role
user_status

user_sessions
id UUIDv7 PK

user_id FK users

refresh_token TEXT

ip_address VARCHAR

device_info TEXT

login_time TIMESTAMP

logout_time TIMESTAMP

created_at TIMESTAMP

rules_acceptance
id UUIDv7 PK

user_id FK users

rules_version VARCHAR

accepted_at TIMESTAMP

ip_address VARCHAR

MODULE 2 - PROFILE MANAGEMENT
user_profiles
id UUIDv7 PK

user_id FK users

profile_photo TEXT

full_name VARCHAR(255)

gender VARCHAR(20)

dob DATE

email VARCHAR(255)

aadhaar_encrypted TEXT

aadhaar_hash VARCHAR(128)

aadhaar_verified BOOLEAN

state VARCHAR(100)

district VARCHAR(100)

pincode VARCHAR(10)

address TEXT

bank_name VARCHAR(255)

account_number_encrypted TEXT

account_number_masked VARCHAR(50)

ifsc_code VARCHAR(20)

bank_verified BOOLEAN

nominee_name VARCHAR(255)

nominee_relationship VARCHAR(100)

nominee_phone VARCHAR(20)

profile_completion INTEGER

created_at TIMESTAMP

updated_at TIMESTAMP

user_documents
id UUIDv7 PK

user_id FK users

document_type ENUM

file_path TEXT

verification_status ENUM

verified_by FK users

verified_at TIMESTAMP

rejection_reason TEXT

uploaded_at TIMESTAMP
Document Types
AADHAAR
BANK_PROOF
PROFILE_PHOTO
NOMINEE_PROOF
Verification Status
PENDING
APPROVED
REJECTED

Constraint

UNIQUE(user_id, document_type)
MODULE 3 - LEADER APPLICATION
leader_applications
id UUIDv7 PK

full_name VARCHAR

phone VARCHAR

email VARCHAR

aadhaar_encrypted TEXT

aadhaar_hash VARCHAR

district VARCHAR

pincode VARCHAR

address TEXT

reason TEXT

status ENUM

reviewed_by FK users

reviewed_at TIMESTAMP

created_at TIMESTAMP

MODULE 4 - TEAM MANAGEMENT
teams
id UUIDv7 PK

team_code VARCHAR UNIQUE

team_name VARCHAR UNIQUE

leader_id FK users

district VARCHAR

area VARCHAR

pincode VARCHAR

description TEXT

member_count INTEGER DEFAULT 0

current_level INTEGER

status ENUM

created_at TIMESTAMP
Status
ACTIVE
INACTIVE
SUSPENDED

Level Allowed Values

1
2
3
4
5
6

team_members
id UUIDv7 PK

team_id FK teams

member_id FK users

joined_level INTEGER

joined_at TIMESTAMP
Unique
UNIQUE(member_id)
MODULE 5 - REFERRALS
referral_codes
id UUIDv7 PK
code VARCHAR UNIQUE
referral_type ENUM
team_id FK teams
level_number INTEGER
generated_by FK users
max_usage INTEGER
used_count INTEGER DEFAULT 0
is_active BOOLEAN DEFAULT TRUE
expires_at TIMESTAMP
created_at TIMESTAMP
Referral Types
LEADER
TEAM

MODULE 6 - LEVEL SYSTEM
levels
id INTEGER PK

level_number INTEGER

reward_amount DECIMAL

requirement_type ENUM

requirement_value INTEGER

team_level_progress
id UUIDv7 PK

team_id FK teams

level_number INTEGER

current_progress INTEGER

completed BOOLEAN

completed_at TIMESTAMP

Constraint

UNIQUE(team_id, level_number)

personal_level_progress
id UUIDv7 PK

user_id FK users

level_number INTEGER

waste_kg DECIMAL

completed BOOLEAN

completed_at TIMESTAMP

Constraint

UNIQUE(user_id, level_number)

Allowed Levels
7
8
9
10
11
MODULE 7 - COLLECTION CENTERS
collection_centers
id UUIDv7 PK

center_name VARCHAR

district VARCHAR

pincode VARCHAR

address TEXT

latitude DECIMAL

longitude DECIMAL

phone VARCHAR

is_active BOOLEAN

created_at TIMESTAMP

MODULE 8 - WASTE MANAGEMENT
waste_records
id UUIDv7 PK

user_id FK users

center_id FK collection_centers

image_path TEXT

weight_kg DECIMAL

collection_date DATE

location TEXT

verification_status ENUM

verified_by FK users

verified_at TIMESTAMP

rejection_reason TEXT

payment_status ENUM

amount_paid DECIMAL

created_at TIMESTAMP
Verification Status
PENDING
APPROVED
REJECTED
Payment Status
PENDING
APPROVED
PROCESSING
PAID
FAILED

waste_status_history
id UUIDv7 PK

waste_record_id FK waste_records

status VARCHAR

comments TEXT

updated_by FK users

updated_at TIMESTAMP

MODULE 9 - CLAIMS
reward_claims
id UUIDv7 PK

user_id FK users

claim_type ENUM

level_number INTEGER

amount DECIMAL

status ENUM

is_locked BOOLEAN

reviewed_by FK users

reviewed_at TIMESTAMP

rejection_reason TEXT

requested_at TIMESTAMP
Claim Types
TEAM
PERSONAL
Status
PENDING
APPROVED
REJECTED
PROCESSING
PAID

Constraint

UNIQUE(user_id, level_number, claim_type)

Claim Validation

TEAM Claim

Allowed Levels:
1
2
3
4
5
6

PERSONAL Claim

Allowed Levels:
7
8
9
10
11

MODULE 10 - PAYMENTS
payment_batches
id UUIDv7 PK

batch_name VARCHAR

total_transactions INTEGER

total_amount DECIMAL

status ENUM

created_by FK users

created_at TIMESTAMP

payment_transactions
id UUIDv7 PK

claim_id FK reward_claims

user_id FK users

amount DECIMAL

transaction_reference VARCHAR

status ENUM

paid_at TIMESTAMP

Constraint

UNIQUE(claim_id)

payment_batch_items
id UUIDv7 PK

batch_id FK payment_batches

payment_transaction_id FK payment_transactions

created_at TIMESTAMP

payment_audit_logs
id UUIDv7 PK

payment_id FK payment_transactions

action VARCHAR

performed_by FK users

old_status VARCHAR

new_status VARCHAR

remarks TEXT

created_at TIMESTAMP

MODULE 11 - NOTIFICATIONS
notifications
id UUIDv7 PK

title VARCHAR

message TEXT

target_type ENUM

created_by FK users

created_at TIMESTAMP

notification_logs
id UUIDv7 PK

notification_id FK notifications

user_id FK users

delivered BOOLEAN

delivered_at TIMESTAMP

is_read BOOLEAN

read_at TIMESTAMP

announcements
id UUIDv7 PK

title VARCHAR

message TEXT

start_date DATE

end_date DATE

created_by FK users

is_active BOOLEAN

MODULE 12 - AUDIT
audit_logs
id UUIDv7 PK

user_id FK users

role VARCHAR

action VARCHAR

entity_type VARCHAR

entity_id UUID

old_values JSONB

new_values JSONB

ip_address VARCHAR

device TEXT

created_at TIMESTAMP
Important:
INSERT ONLY

NO UPDATE

NO DELETE

system_logs
id UUIDv7 PK

log_level VARCHAR

source VARCHAR

message TEXT

created_at TIMESTAMP

MODULE 13 - ANALYTICS
analytics_snapshots
id UUIDv7 PK

metric_name VARCHAR

metric_value DECIMAL

snapshot_date DATE

snapshot_type VARCHAR [Values: DAILY WEEKLY MONTHLY]


MODULE 14 - SYSTEM
system_settings
id UUIDv7 PK

setting_key VARCHAR UNIQUE

setting_value TEXT

updated_by FK users

updated_at TIMESTAMP
Examples
REFERRAL_EXPIRY_HOURS

OTP_EXPIRY_MINUTES

MAX_LOGIN_ATTEMPTS

CLAIM_LOCK_DAYS

PAYMENT_BATCH_SIZE

EMAIL_ENABLED

SOFT DELETE STRATEGY
Add to:
users
teams
collection_centers
Fields:
deleted_at TIMESTAMP

deleted_by UUID
Never physically delete production data.

FINAL TABLE COUNT
Authentication:
3

Profile:
2

Leader Application:
1

Team:
2

Referral:
1

Levels:
3

Collection Centers:
1

Waste:
2

Claims:
1

Payments:
4

Notifications:
3

Audit:
2

Analytics:
1

System:
1
Total:
27 Tables
This is the database design I would freeze and use as the official Athiyaman Digital India Phase 1 production database architecture before creating SQLAlchemy models and Alembic migrations. It aligns with the architecture document, supports your business workflows, and leaves room for Skill India and Clean India without redesigning the core database.

Yes. What we have now is a Physical Database Design (Tables & Fields).
But before coding, you should also have:
1. Business Logic Design
2. Relationship Design
3. Foreign Key Design
4. Constraints Design
5. Data Flow Design
6. Ownership Rules
7. Validation Rules
8. Level Progress Rules
9. Claim Rules
10. Payment Rules
11. Audit Rules
This is actually what makes a database "production-ready".

1. USER RELATIONSHIP MODEL
users
│
├── user_profiles (1:1)
│
├── user_documents (1:N)
│
├── user_sessions (1:N)
│
├── rules_acceptance (1:N)
│
├── team_members (1:N)
│
├── waste_records (1:N)
│
├── reward_claims (1:N)
│
├── payment_transactions (1:N)
│
├── notification_logs (1:N)
│
└── audit_logs (1:N)
Rule:
One User
=
One Profile

One User
=
Many Sessions

One User
=
Many Waste Records

One User
=
Many Claims

2. TEAM RELATIONSHIP MODEL
teams
│
├── leader_id → users
│
├── team_members
│
├── referral_codes
│
└── team_level_progress
Rule:
One Leader
=
One Team
Constraint

UNIQUE(leader_id)
Meaning:
Leader cannot create multiple teams.

3. TEAM MEMBER RULES
One User
can join
Only One Team
Constraint:
UNIQUE(member_id)
inside:
team_members
Meaning:
A member cannot join 2 teams.
3. Leader Ownership Rules
One Leader
can join
Only One Team
Constraint:
UNIQUE(leader_id)
inside:
teams

Meaning:
A leader can leads only one team

4. REFERRAL BUSINESS LOGIC
Leader Referral
Admin
↓
Generate Referral
↓
Leader Registration
↓
Referral Consumed
Constraint:
used_count <= max_usage

Team Referral
Leader
↓
Generate Referral
↓
Members Join Team
Level 1
Need 10 Members
Referral Max Usage = 10
↓
Referral Expires
↓
Level 1 Complete
Level 2
Need 90 Members
Referral Max Usage = 90
↓
Referral Expires
↓
Level 2 Complete
Level 3
Need 720 Members
Referral Max Usage = 720
↓
Referral Expires
↓
Level 3 Complete
Level 4
Need 5040 Members
Referral Max Usage = 5040
↓
Referral Expires
↓
Level 4 Complete
Level 5
Need 30240 Members
Referral Max Usage = 30240
↓
Referral Expires
↓
Level 5 Complete
Level 6
Need 50000 Members
Referral Max Usage = 50000
↓
Referral Expires
↓
Level 6 Complete
Referral Usage Rules
Leader Referral
Max Usage = 1
After registration
Referral becomes inactive.
Level 1 Referral
Max Usage = 10
Level 2 Referral
Max Usage = 90
Level 3 Referral
Max Usage = 720
Level 4 Referral
Max Usage = 5040
Level 5 Referral
Max Usage = 30240
Level 6 Referral
Max Usage = 50000
When
used_count >= max_usage
↓
is_active = FALSE
Team Referral Eligibility
Leader cannot generate
Level 2 Referral
until
Level 1 Completed
Leader cannot generate
Level 3 Referral
until
Level 2 Completed
Leader cannot generate
Level 4 Referral
until
Level 3 Completed
Continue until Level 6
5. LEVEL ENGINE LOGIC
Team Levels
Level 1
10 Members

Level 2
90 Members

Level 3
720 Members

Level 4
5040 Members

Level 5
30240 Members

Level 6
50000 Members
Source:
teams.member_count
NOT
COUNT(*)
because of performance.

Personal Levels
Level 7
10 KG Approved Waste

Level 8
10 KG Approved Waste

Level 9
10 KG Approved Waste

Level 10
10 KG Approved Waste

Level 11
10 KG Approved Waste
Source:
waste_records
WHERE verification_status='APPROVED'

6. WASTE BUSINESS LOGIC
Relationship:
User
↓
Waste Records
↓
Collection Center
Rule:
Only Approved Waste
counts toward level progression.
Rejected Waste:
Ignored
Pending Waste:
Ignored

7. CLAIM ENGINE LOGIC
Rule:
One Level
=
One Claim
Constraint:
UNIQUE(user_id, level_number, claim_type)
inside:
reward_claims

Claim Flow
Level Completed
↓
Claim Created
↓
Pending
↓
Admin Review
↓
Approved
↓
Payment Queue
↓
Paid

Claim Lock
Rule:
User cannot create another claim
while current claim is pending.
Field:
is_locked BOOLEANClaim Creation Rule
Team Levels

1 → 6

Claim Type = TEAM


Personal Levels

7 → 11

Claim Type = PERSONAL

8. PAYMENT BUSINESS LOGIC
Relationship:
reward_claims
↓
payment_transactions
↓
payment_batches

End of Day Flow
Admin Login
↓
View Eligible Payments
↓
Create Batch
↓
Approve Batch
↓
Payment Provider
↓
Paid

Batch Relationship
payment_batches
    ↓
payment_batch_items
    ↓
payment_transactions
One Batch:
1 → Many Transactions

9. COLLECTION CENTER RULES
Relationship:
collection_centers
↓
waste_records
Rule:
Waste should be linked to
nearest collection center.

10. DOCUMENT VERIFICATION RULES
Relationship:
user_profiles
↓
user_documents
Required Documents:
Aadhaar

Bank Proof

Profile Photo
Optional:
Nominee Proof

11. AUDIT LOG RULES
Relationship:
Every Module
↓
audit_logs
Examples:
Login

Logout

Profile Update

Team Creation

Referral Generation

Claim Creation

Claim Approval

Payment Approval

Immutable Constraint
audit_logs
Rules:
INSERT = Allowed

UPDATE = Forbidden

DELETE = Forbidden

12. NOTIFICATION RULES
Relationship:
notifications
↓
notification_logs
↓
users
One Notification:
Can be sent to:

All Users

Leaders

Members

Admins

Developers

Specific User

13. SYSTEM SETTINGS RULES
Purpose:
No hardcoded values.
Examples:
OTP Expiry

Referral Expiry

Payment Batch Size

Max Login Attempts

Email Enable
Admin can change:
system_settings
without modifying code.

14. CRITICAL CONSTRAINTS
users
UNIQUE(username)

UNIQUE(phone_number)

teams
UNIQUE(team_name)

UNIQUE(team_code)

UNIQUE(leader_id)

team_members
UNIQUE(member_id)

referral_codes
UNIQUE(code)

reward_claims
UNIQUE(user_id, level_number, claim_type)

system_settings
UNIQUE(setting_key)

FINAL DATABASE PACKAGE
The complete database documentation should contain:
1. Database Overview

2. Business Logic

3. Entity Descriptions

4. Table Definitions

5. Relationships

6. ER Diagram

7. Foreign Keys

8. Constraints

9. Indexes

10. Enum Definitions

11. Validation Rules

12. Audit Rules

13. Security Rules

14. Level Engine Rules

15. Referral Rules

16. Claim Rules

17. Payment Rules

18. Data Retention Rules

19. Backup Strategy

20. Future Expansion Strategy
At that point, your database documentation is no longer just a schema—it becomes a complete Database Design Specification that backend developers can implement directly without guessing any business rules.
You're very close. I would say your database design is around 95-98% complete.
Before freezing it as the final Athiyaman Digital India Phase 1 database, I would add a few enterprise-level items.

1. ENUM MASTER DEFINITIONS
Don't leave enums undefined.
Create a section:
UserRole
---------
MEMBER
LEADER
ADMIN
DEVELOPER

UserStatus
-----------
PENDING
ACTIVE
SUSPENDED
BLOCKED
DELETED

ReferralType
-------------
LEADER
TEAM

ClaimStatus
------------
PENDING
APPROVED
REJECTED
PROCESSING
PAID

WasteStatus
------------
PENDING
APPROVED
REJECTED

PaymentStatus
--------------
PENDING
APPROVED
PROCESSING
PAID
FAILED
This prevents future confusion.

2. INDEX STRATEGY
Very important.
For each table define indexes.
Example:
users
INDEX(username)
INDEX(phone_number)
INDEX(role)
INDEX(user_status)
teams
INDEX(team_code)
INDEX(team_name)
INDEX(leader_id)
waste_records
INDEX(user_id)
INDEX(center_id)
INDEX(verification_status)
INDEX(collection_date)
payment_transactions
INDEX(user_id)
INDEX(status)
INDEX(claim_id)
Without this, performance will degrade later.

3. CASCADE RULES
Define every FK behavior.
Example:
user_profiles
user_id
ON DELETE CASCADE
team_members
team_id
ON DELETE RESTRICT

member_id
ON DELETE RESTRICT
audit_logs
user_id
ON DELETE SET NULL
This is usually forgotten.

4. AUDIT COVERAGE MATRIX
Define exactly what gets logged.
Example:
Login
Logout
Password Change
Profile Update
Team Creation
Referral Generation
Waste Submission
Waste Approval
Claim Creation
Claim Approval
Payment Approval
Notification Creation
Settings Change
This becomes your audit policy.

5. DATA RETENTION POLICY
Add:
Audit Logs
Retain Forever

Payment Records
Retain Forever

Claims
Retain Forever

Notifications
Retain 5 Years

User Sessions
Retain 1 Year

Analytics Snapshots
Retain 3 Years

6. REPORTING VIEWS
Future admin analytics will become easier.
Create logical views:
vw_team_summary

vw_payment_summary

vw_waste_summary

vw_level_summary

vw_member_summary
Not tables.
Database views.

7. FUTURE MODULE PLACEHOLDERS
Because you already planned:
Phase 2
Skill India

Phase 3
Clean India
Add section:
Reserved Expansion Domains
skill_courses

skill_certifications

skill_assessments

clean_campaigns

clean_events

clean_volunteers
No tables now.
Just reserve namespace.

8. SECURITY CLASSIFICATION
For compliance.
Example:
PUBLIC
--------
Announcements

INTERNAL
--------
Teams
Levels

CONFIDENTIAL
------------
Profiles
Documents

HIGHLY SENSITIVE
----------------
Aadhaar
Bank Details
Payments
Very useful later.

9. BACKUP CLASSIFICATION
Add:
Critical

users
profiles
payments
claims

High

teams
waste

Medium

notifications
analytics

10. DATABASE VERSION
Freeze the schema officially.
Example:
Database Version:
1.0.0

Project:
Athiyaman Platform

Module:
Digital India Phase 1

Status:
Approved For Development

Date:
YYYY-MM-DD

Final Verdict
After adding:
✓ ENUM Definitions

✓ Index Strategy

✓ FK Cascade Rules

✓ Audit Coverage Matrix

✓ Data Retention Policy

✓ Reporting Views

✓ Future Expansion Domains

✓ Security Classification

✓ Backup Classification

✓ Database Versioning
your database documentation becomes a complete professional Database Design Specification.
At that point I would consider the database architecture 100% finalized and safe to start:
PostgreSQL Schema
↓
SQLAlchemy Models
↓
Alembic Migrations
↓
FastAPI Development
without expecting major database redesign later.