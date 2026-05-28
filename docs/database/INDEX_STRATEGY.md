02_INDEX_STRATEGY.md
=========================================================
ATHIYAMAN PLATFORM
DIGITAL INDIA (PHASE 1)

DATABASE INDEX STRATEGY

Version: 1.1
Status: Approved
=========================================================
PURPOSE
Indexes improve:
Query Performance
Login Speed
Dashboard Loading
Search Operations
Reporting
Payment Processing
Team Statistics
Without indexes, performance will degrade significantly as data grows.

INDEX TYPES USED
PRIMARY KEY INDEX
Automatically created.
Example:
users.id
teams.id
waste_records.id

UNIQUE INDEX
Used for uniqueness validation.
Example:
username
phone_number
team_code
team_name

SEARCH INDEX
Used for filtering and searching.
Example:
district
status
created_at

COMPOSITE INDEX
Multiple columns.
Example:
(user_id, level_number)

MODULE 1 — AUTHENTICATION
users
Primary Index
PRIMARY KEY(id)
Unique Indexes
UNIQUE(username)

UNIQUE(phone_number)
Search Indexes
INDEX(role)

INDEX(user_status)

INDEX(created_at)

user_sessions
Search Indexes
INDEX(user_id)

INDEX(login_time)

INDEX(created_at)

rules_acceptance
Search Indexes
INDEX(user_id)

INDEX(accepted_at)

MODULE 2 — PROFILE MANAGEMENT
user_profiles
Unique Index
UNIQUE(user_id)
Search Indexes
INDEX(full_name)

INDEX(district)

INDEX(state)

INDEX(pincode)
Security Index
INDEX(aadhaar_hash)
Used for duplicate detection.

user_documents
Unique Index
UNIQUE(user_id, document_type)
Search Indexes
INDEX(user_id)

INDEX(document_type)

INDEX(verification_status)

MODULE 3 — LEADER APPLICATIONS
leader_applications
Search Indexes
INDEX(status)

INDEX(phone)

INDEX(email)

INDEX(created_at)

INDEX(district)
Security Index
INDEX(aadhaar_hash)

MODULE 4 — TEAM MANAGEMENT
teams
Unique Indexes
UNIQUE(team_code)

UNIQUE(team_name)

UNIQUE(leader_id)
Search Indexes
INDEX(current_level)

INDEX(status)

INDEX(district)

INDEX(member_count)

INDEX(created_at)

team_members
Unique Index
UNIQUE(member_id)
Search Indexes
INDEX(team_id)

INDEX(joined_level)

INDEX(joined_at)

MODULE 5 — REFERRALS
referral_codes
Unique Index
UNIQUE(code)
Search Indexes
INDEX(team_id)

INDEX(referral_type)

INDEX(level_number)

INDEX(is_active)

INDEX(expires_at)

INDEX(created_at)
Composite Index
(team_id, level_number)

MODULE 6 — LEVEL SYSTEM
levels
Unique Index
UNIQUE(level_number)

team_level_progress
Unique Constraint
UNIQUE(team_id, level_number)
Search Indexes
INDEX(team_id)

INDEX(level_number)

INDEX(completed)

personal_level_progress
Unique Constraint
UNIQUE(user_id, level_number)
Search Indexes
INDEX(user_id)

INDEX(level_number)

INDEX(completed)

MODULE 7 — COLLECTION CENTERS
collection_centers
Search Indexes
INDEX(district)

INDEX(pincode)

INDEX(is_active)
Geographic Index
Future:
(latitude, longitude)

MODULE 8 — WASTE MANAGEMENT
waste_records
Search Indexes
INDEX(user_id)

INDEX(center_id)

INDEX(collection_date)

INDEX(created_at)

INDEX(verification_status)

INDEX(payment_status)
Composite Index
(user_id, verification_status)

(user_id, collection_date)

waste_status_history
Search Indexes
INDEX(waste_record_id)

INDEX(updated_by)

INDEX(updated_at)

MODULE 9 — CLAIMS
reward_claims
Unique Constraint
UNIQUE(user_id, level_number, claim_type)
Search Indexes
INDEX(user_id)

INDEX(status)

INDEX(claim_type)

INDEX(requested_at)
Composite Index
(user_id, status)

(claim_type, status)

MODULE 10 — PAYMENTS
payment_batches
Search Indexes
INDEX(status)

INDEX(created_at)

INDEX(created_by)

payment_transactions
Unique Constraint
UNIQUE(claim_id)
Search Indexes
INDEX(user_id)

INDEX(status)

INDEX(paid_at)
Composite Index
(user_id, status)

payment_batch_items
Search Indexes
INDEX(batch_id)

INDEX(payment_transaction_id)

payment_audit_logs
Search Indexes
INDEX(payment_id)

INDEX(performed_by)

INDEX(created_at)

MODULE 11 — NOTIFICATIONS
notifications
Search Indexes
INDEX(target_type)

INDEX(created_by)

INDEX(created_at)

notification_logs
Search Indexes
INDEX(user_id)

INDEX(notification_id)

INDEX(is_read)

INDEX(delivered)
Composite Index
(user_id, is_read)

announcements
Search Indexes
INDEX(is_active)

INDEX(start_date)

INDEX(end_date)

MODULE 12 — AUDIT
audit_logs
Search Indexes
INDEX(user_id)

INDEX(role)

INDEX(action)

INDEX(entity_type)

INDEX(created_at)
Composite Indexes
(user_id, created_at)

(entity_type, created_at)

system_logs
Search Indexes
INDEX(log_level)

INDEX(source)

INDEX(created_at)

MODULE 13 — ANALYTICS
analytics_snapshots
Search Indexes
INDEX(metric_name)

INDEX(snapshot_date)

INDEX(snapshot_type)
Composite Index
(metric_name, snapshot_date)

MODULE 14 — SYSTEM
system_settings
Unique Constraint
UNIQUE(setting_key)

HIGH PRIORITY INDEXES
These are critical.
users.username

users.phone_number

teams.team_code

teams.team_name

referral_codes.code

waste_records.user_id

reward_claims.user_id

payment_transactions.user_id

audit_logs.user_id

INDEX IMPLEMENTATION ORDER
1. Primary Keys

2. Unique Constraints

3. Foreign Keys

4. Search Indexes

5. Composite Indexes

6. Analytics Indexes

PERFORMANCE BENEFITS
Login Search
< 10ms

Profile Load
< 20ms

Dashboard Load
< 100ms

Payment Search
< 50ms

Referral Validation
< 10ms

Audit Search
< 100ms
Target estimates for properly indexed PostgreSQL.


