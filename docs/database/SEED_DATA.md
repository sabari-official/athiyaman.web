04_SEED_DATA.md
=========================================================
ATHIYAMAN PLATFORM
DIGITAL INDIA (PHASE 1)

SEED DATA SPECIFICATION

Version: 1.1
Status: Approved
=========================================================
PURPOSE
Seed Data provides the minimum required records needed for:
Initial System Startup
Authentication Testing
RBAC Testing
Dashboard Testing
Level Engine Testing
Payment Testing
Development Environment
This data should be inserted automatically during initial deployment.

SEEDING ORDER
1. ENUMS

2. SYSTEM SETTINGS

3. LEVELS

4. ADMIN ACCOUNT

5. DEVELOPER ACCOUNT

6. COLLECTION CENTERS

7. ANNOUNCEMENTS

8. ANALYTICS SNAPSHOTS

MODULE 1 — SYSTEM SETTINGS
Table:
system_settings

Authentication Settings
SETTING_KEY                      VALUE

OTP_EXPIRY_MINUTES               5

MAX_LOGIN_ATTEMPTS               5

ACCOUNT_LOCK_DURATION_MINUTES    30

JWT_ACCESS_TOKEN_MINUTES         30

JWT_REFRESH_TOKEN_DAYS           30

Referral Settings
REFERRAL_EXPIRY_HOURS            72

LEADER_REFERRAL_MAX_USAGE        1

Claim Settings
CLAIM_LOCK_DAYS                  30

AUTO_CLOSE_FAILED_CLAIMS         TRUE

Payment Settings
PAYMENT_BATCH_SIZE               5000

PAYMENT_PROVIDER                 RAZORPAYX

PAYMENT_APPROVAL_REQUIRED        TRUE

Notification Settings
EMAIL_ENABLED                    TRUE

INAPP_ENABLED                    TRUE

ANNOUNCEMENT_ENABLED             TRUE

Security Settings
AADHAAR_ENCRYPTION_ENABLED       TRUE

BANK_ENCRYPTION_ENABLED          TRUE

RATE_LIMIT_ENABLED               TRUE

MODULE 2 — LEVEL MASTER DATA
Table:
levels

Team Levels
Level 1
level_number       1

reward_amount      100

requirement_type   MEMBER_COUNT

requirement_value  10

Level 2
level_number       2

reward_amount      1000

requirement_type   MEMBER_COUNT

requirement_value  90

Level 3
level_number       3

reward_amount      2000

requirement_type   MEMBER_COUNT

requirement_value  720

Level 4
level_number       4

reward_amount      3000

requirement_type   MEMBER_COUNT

requirement_value  5040

Level 5
level_number       5

reward_amount      4000

requirement_type   MEMBER_COUNT

requirement_value  30240

Level 6
level_number       6

reward_amount      5000

requirement_type   MEMBER_COUNT

requirement_value  50000

Personal Levels
Level 7
level_number       7

reward_amount      10000

requirement_type   APPROVED_WASTE_KG

requirement_value  10

Level 8
level_number       8

reward_amount      20000

requirement_type   APPROVED_WASTE_KG

requirement_value  10

Level 9
level_number       9

reward_amount      30000

requirement_type   APPROVED_WASTE_KG

requirement_value  10

Level 10
level_number       10

reward_amount      40000

requirement_type   APPROVED_WASTE_KG

requirement_value  10

Level 11
level_number       11

reward_amount      50000

requirement_type   APPROVED_WASTE_KG

requirement_value  10

MODULE 3 — DEFAULT ADMIN ACCOUNT
Table:
users

Admin User
username      admin

role          ADMIN

user_status   ACTIVE

is_verified   TRUE

Admin Profile
full_name     System Administrator

profile_completion 100

MODULE 4 — DEFAULT DEVELOPER ACCOUNT
Table:
users

Developer User
username      developer

role          DEVELOPER

user_status   ACTIVE

is_verified   TRUE

Developer Profile
full_name     System Developer

profile_completion 100

MODULE 5 — COLLECTION CENTER TEST DATA
Table:
collection_centers
Purpose:
Development

Maps Testing

Search Testing

Distance Calculation Testing

Sample Center 1
center_name

Athiyaman Collection Center - Chennai

district

Chennai

pincode

600001

phone

9999999991

is_active

TRUE

Sample Center 2
center_name

Athiyaman Collection Center - Madurai

district

Madurai

pincode

625001

phone

9999999992

is_active

TRUE

Sample Center 3
center_name

Athiyaman Collection Center - Coimbatore

district

Coimbatore

pincode

641001

phone

9999999993

is_active

TRUE

MODULE 6 — ANNOUNCEMENTS
Table:
announcements

Welcome Announcement
title

Welcome To Athiyaman Platform

message

Welcome to Digital India Phase 1

is_active

TRUE

MODULE 7 — ANALYTICS SNAPSHOTS
Table:
analytics_snapshots
Initial Values:
TOTAL_USERS          0

TOTAL_TEAMS          0

TOTAL_MEMBERS        0

TOTAL_WASTE_KG       0

TOTAL_PAYMENTS       0

TOTAL_CLAIMS         0
Snapshot Type:
DAILY

DEVELOPMENT TEST DATA
Environment:
LOCAL DEVELOPMENT ONLY
Create:
1 Admin

1 Developer

1 Leader

10 Members

1 Team

5 Waste Records

1 Reward Claim

1 Payment Batch
Purpose:
API Testing

Frontend Testing

Integration Testing

PRODUCTION SEED DATA
Production should contain:
System Settings

Levels

Admin User

Developer User
Only.
Do NOT create:
Fake Teams

Fake Members

Fake Waste

Fake Payments
in production.

SEED VALIDATION CHECKLIST
✓ All ENUMs Created

✓ All Settings Inserted

✓ Levels 1-11 Inserted

✓ Admin Created

✓ Developer Created

✓ Collection Centers Created

✓ Announcement Created

✓ Analytics Snapshots Created
