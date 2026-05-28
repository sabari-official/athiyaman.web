Admin
 │
 ├── Leader Application Approval
 │
 └── Leader Referral
        │
       ▼
     Leader
        │
        ▼
      Team
        │
        ├── Team Referral
        │
        ▼
     Members
        │
        ├── Team Levels (1-6)
        │
        └── Waste Records
                 │
                 ▼
          Personal Levels (7-11)
                 │
                 ▼
            Reward Claims
                 │
                 ▼
          Payment Processing
                 │
                 ▼
                 Paid


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

