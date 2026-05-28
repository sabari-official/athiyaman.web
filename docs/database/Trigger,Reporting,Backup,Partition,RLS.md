Excellent. Since you've decided to make the database architecture fully enterprise-ready, here are the 5 additional database documents.

06_TRIGGER_STRATEGY.md
=========================================================
ATHIYAMAN PLATFORM
DIGITAL INDIA (PHASE 1)

TRIGGER STRATEGY

Version: 1.1
Status: Approved
=========================================================
PURPOSE
Automate database operations.
Prevent application mistakes.
Maintain data consistency.

TRIGGER 1
TEAM MEMBER COUNTER
Table:
team_members
Event:
AFTER INSERT
Action:
teams.member_count += 1

Event:
AFTER DELETE
Action:
teams.member_count -= 1

TRIGGER 2
REFERRAL USAGE COUNTER
Table:
team_members
Event:
AFTER INSERT
Action:
referral_codes.used_count += 1

TRIGGER 3
REFERRAL AUTO EXPIRATION
Table:
referral_codes
Condition:
used_count >= max_usage
Action:
is_active = FALSE

TRIGGER 4
TEAM LEVEL COMPLETION
Table:
teams
Event:
member_count updated
Check:
Level 1 = 10

Level 2 = 90

Level 3 = 720

Level 4 = 5040

Level 5 = 30240

Level 6 = 50000
Action:
Auto Complete Team Level

TRIGGER 5
PERSONAL LEVEL COMPLETION
Table:
waste_records
Event:
verification_status = APPROVED
Action:
Update personal_level_progress

TRIGGER 6
PAYMENT AUDIT
Table:
payment_transactions
Event:
Status Change
Action:
Insert payment_audit_logs

TRIGGER 7
AUDIT LOGGING
Critical Tables:
users
teams
waste_records
reward_claims
payment_transactions
Action:
Insert audit_logs

Status:
APPROVED

07_REPORTING_VIEWS.md
=========================================================
ATHIYAMAN PLATFORM
DIGITAL INDIA (PHASE 1)

REPORTING VIEWS

Version: 1.1
Status: Approved
=========================================================
PURPOSE
Fast Admin Dashboard Queries
Avoid expensive joins

VIEW 1
vw_team_summary
Team Name

Leader

Current Level

Member Count

Status

VIEW 2
vw_member_summary
Username

Team

Personal Level

Approved Waste KG

VIEW 3
vw_payment_summary
Total Claims

Total Approved

Total Paid

Total Failed

VIEW 4
vw_claim_summary
Pending Claims

Approved Claims

Rejected Claims

VIEW 5
vw_waste_summary
District

Total Waste

Approved Waste

Rejected Waste

VIEW 6
vw_collection_center_summary
Center Name

Waste Count

Total Weight

VIEW 7
vw_referral_summary
Team

Current Referral

Used Count

Remaining Slots

VIEW 8
vw_dashboard_statistics
Total Users

Total Teams

Total Members

Total Waste

Total Claims

Total Payments

Status:
APPROVED

08_BACKUP_RECOVERY.md
=========================================================
ATHIYAMAN PLATFORM
DIGITAL INDIA (PHASE 1)

BACKUP & RECOVERY PLAN

Version: 1.1
Status: Approved
=========================================================
BACKUP LEVELS

DAILY
Schedule:
02:00 AM
Type:
Incremental Backup
Retention:
30 Days

WEEKLY
Schedule:
Sunday
Type:
Full Backup
Retention:
3 Months

MONTHLY
Schedule:
1st Day
Type:
Archive Backup
Retention:
1 Year

CRITICAL TABLES
users

user_profiles

teams

team_members

waste_records

reward_claims

payment_transactions

audit_logs

RECOVERY TARGET
Maximum Data Loss

< 24 Hours

RESTORE ORDER
1. Database

2. Users

3. Teams

4. Waste

5. Claims

6. Payments

7. Audit Logs

Status:
APPROVED

09_PARTITIONING_STRATEGY.md
=========================================================
ATHIYAMAN PLATFORM
DIGITAL INDIA (PHASE 1)

PARTITIONING STRATEGY

Version: 1.1
Status: Future Ready
=========================================================
PURPOSE
Handle Millions of Records

TABLE 1
waste_records
Partition:
YEAR(collection_date)
Example:
waste_records_2026

waste_records_2027

waste_records_2028

TABLE 2
audit_logs
Partition:
YEAR(created_at)
Example:
audit_logs_2026

audit_logs_2027

TABLE 3
notification_logs
Partition:
MONTH(created_at)

IMPLEMENTATION TRIGGER
When:
waste_records > 1,000,000
Implement partitioning.

Status:
FUTURE IMPLEMENTATION

10_RLS_POLICY.md
=========================================================
ATHIYAMAN PLATFORM
DIGITAL INDIA (PHASE 1)

ROW LEVEL SECURITY POLICY

Version: 1.1
Status: Future Ready
=========================================================
PURPOSE
Database Level Security
Additional protection beyond RBAC.

MEMBER POLICY
Can Access:
Own Profile

Own Waste Records

Own Claims

Own Payments

Own Notifications
Rule:
user_id = current_user_id

LEADER POLICY
Can Access:
Own Team

Own Team Members

Own Team Progress

Team Referrals
Rule:
team_id = leader_team_id

ADMIN POLICY
Can Access:
All Records

DEVELOPER POLICY
Can Access:
System Logs

Audit Logs

Analytics

Monitoring
Cannot Access:
Bank Account Data

Aadhaar Data

IMPLEMENTATION STATUS
Current:
FastAPI RBAC

JWT Authorization
Future:
PostgreSQL RLS

Status:
FUTURE IMPLEMENTATION
