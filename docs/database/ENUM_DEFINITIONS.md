01_ENUM_DEFINITIONS.md
This document becomes the single source of truth for all PostgreSQL ENUM types used across the Athiyaman Platform.

ENUM_DEFINITIONS.md
=========================================================
ATHIYAMAN PLATFORM
DIGITAL INDIA (PHASE 1)

ENUM DEFINITIONS

Version: 1.1
Status: Approved
=========================================================
PURPOSE
This document defines all ENUM values used throughout the database and application.
Benefits:
Data consistency
Validation
Cleaner queries
Faster filtering
Reduced data errors
All application logic must use these ENUM values.

1. USER ROLE ENUM
Enum Name:
user_role_enum
Values:
MEMBER
LEADER
ADMIN
DEVELOPER
Usage:
users.role
Description:
Role
Description
MEMBER
Regular team member
LEADER
Team owner and manager
ADMIN
Platform administrator
DEVELOPER
System monitoring and maintenance

2. USER STATUS ENUM
Enum Name:
user_status_enum
Values:
PENDING
ACTIVE
SUSPENDED
BLOCKED
DELETED
Usage:
users.user_status
Description:
Status
Description
PENDING
Account not completed
ACTIVE
Account active
SUSPENDED
Temporarily disabled
BLOCKED
Security block
DELETED
Soft deleted

3. DOCUMENT TYPE ENUM
Enum Name:
document_type_enum
Values:
AADHAAR
BANK_PROOF
PROFILE_PHOTO
NOMINEE_PROOF
Usage:
user_documents.document_type

4. VERIFICATION STATUS ENUM
Enum Name:
verification_status_enum
Values:
PENDING
APPROVED
REJECTED
Usage:
user_documents.verification_status

waste_records.verification_status

5. TEAM STATUS ENUM
Enum Name:
team_status_enum
Values:
ACTIVE
INACTIVE
SUSPENDED
Usage:
teams.status

6. REFERRAL TYPE ENUM
Enum Name:
referral_type_enum
Values:
LEADER
TEAM
Usage:
referral_codes.referral_type
Description:
LEADER
Admin creates referral for Team Leader registration.

TEAM
Leader creates referral for Team Member registration.

7. REQUIREMENT TYPE ENUM
Enum Name:
requirement_type_enum
Values:
MEMBER_COUNT
APPROVED_WASTE_KG
Usage:
levels.requirement_type

8. WASTE PAYMENT STATUS ENUM
Enum Name:
waste_payment_status_enum
Values:
PENDING
APPROVED
PROCESSING
PAID
FAILED
Usage:
waste_records.payment_status

9. CLAIM TYPE ENUM
Enum Name:
claim_type_enum
Values:
TEAM
PERSONAL
Usage:
reward_claims.claim_type
Description:
TEAM
Levels 1-6

PERSONAL
Levels 7-11

10. CLAIM STATUS ENUM
Enum Name:
claim_status_enum
Values:
PENDING
APPROVED
REJECTED
PROCESSING
PAID
Usage:
reward_claims.status

11. PAYMENT BATCH STATUS ENUM
Enum Name:
payment_batch_status_enum
Values:
PENDING
PROCESSING
COMPLETED
FAILED
Usage:
payment_batches.status

12. PAYMENT TRANSACTION STATUS ENUM
Enum Name:
payment_transaction_status_enum
Values:
PENDING
APPROVED
PROCESSING
PAID
FAILED
Usage:
payment_transactions.status

13. NOTIFICATION TARGET ENUM
Enum Name:
notification_target_enum
Values:
ALL
MEMBER
LEADER
ADMIN
DEVELOPER
USER
Usage:
notifications.target_type
Description:
ALL
Entire platform

MEMBER
All members

LEADER
All leaders

ADMIN
Administrators

DEVELOPER
Developers

USER
Specific user

14. LOG LEVEL ENUM
Enum Name:
log_level_enum
Values:
INFO
WARNING
ERROR
CRITICAL
Usage:
system_logs.log_level

15. ANALYTICS SNAPSHOT TYPE ENUM
Enum Name:
analytics_snapshot_type_enum
Values:
DAILY
WEEKLY
MONTHLY
Usage:
analytics_snapshots.snapshot_type

ENUM IMPLEMENTATION ORDER
1. user_role_enum

2. user_status_enum

3. document_type_enum

4. verification_status_enum

5. team_status_enum

6. referral_type_enum

7. requirement_type_enum

8. waste_payment_status_enum

9. claim_type_enum

10. claim_status_enum

11. payment_batch_status_enum

12. payment_transaction_status_enum

13. notification_target_enum

14. log_level_enum

15. analytics_snapshot_type_enum

TOTAL ENUMS
15 ENUM TYPES

