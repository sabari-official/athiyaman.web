# Interactive Terminal testing instructions — Athiyaman Platform

This document provides step-by-step guidance on how to run, interact with, and test all backend modules using our newly built **Interactive Testing Console (`cli_app.py`)**.

---

## 🚀 Getting Started

Launch the console by executing the following command in your terminal/PowerShell inside the `d:\Athiyaman` directory:

```powershell
python cli_app.py
```

---

## 👤 Scenario A: The Citizen Journey

### Step 1: Generate Referral Code (Admin Prerequisite)
Because Athiyaman uses a strict closed-loop invite system, citizens cannot sign up without a valid referral code.
1. Select option `1` (**Citizen Workspace**).
2. Choose option `2` (**Login Citizen**) and log in as the system administrator:
   - Username: `admin`
   - Password: `admin123`
3. Choose option `7` (**Generate invite Referral Codes**).
   - Type: `LEADER`
   - Level: `1`
4. Copy the generated referral code (e.g., `REF-LEAD-XXXX-XXXX`).

### Step 2: Interactive Citizen Onboarding
1. Still in the Citizen Workspace, choose option `1` (**Interactive Citizen Signup**).
2. Input a username starting with `testcitizen_` or `testleader_` (e.g., `testcitizen_ramesh`).
3. Set a 10-digit phone number, secure password, and **paste the referral code you generated in Step 1**.
4. Choose option `2` (**Login Citizen**) to log in with your newly created credentials. The session will automatically save in memory!

### Step 3: 100% Profile Completeness & Click-Wrap Rules Accept
1. Select option `3` (**View Profile Details**). You will see a `0%` completion score.
2. Choose option `4` (**Onboard Profile details to 100%**). This automatically uploads complete, encrypted, and masked bio/bank details, giving you a perfect `100%` completion score.
3. Choose option `5` (**Accept click-wrap platform rules**). This marks your profile as fully verified (`User.is_verified = True`), unlocking access to active dashboard operations.

### Step 4: Check Level Progression defaults
1. Choose option `8` (**View personal and team level progress details**).
2. Observe that the citizen has Levels 7 through 11 in an `INCOMPLETE` state, with `0.0/10.0 KG` logged waste progress.

---

## ♻️ Scenario B: Manager Waste Logging & SQL Triggers Progression

Let's log physical waste deposits to test the automatic sequential level-progression engines:

1. Return to the Main Menu and choose option `2` (**Waste Manager Workspace**).
2. Select option `1` (**Log Citizen Waste Deposit**).
3. Input the **Target Citizen User ID** (copy the User ID from the Citizen's Profile details printed earlier).
4. Leave the **Collection Center ID** blank to default to the active authorized Chennai Collection Center.
5. Set the **Verified Weight** to `15.0` KG (greater than the Level 7 requirement of `10.0` KG).
6. Press enter to log. Under the hood, the backend processes a double-stage commit transaction (`PENDING` -> `APPROVED`), immediately firing the PostgreSQL trigger `trg_personal_level_completion`!
7. Return to the Citizen Workspace, choose option `8` (**View personal and team level progress details**), and verify that **Level 7 has dynamically updated to completed = TRUE** with `15.0 KG` verified deposits!

---

## 💰 Scenario C: Reward Claim Submission & Administrative Review

### Step 1: Submit Claim
1. In the Citizen Workspace menu, select option `9` (**Claim Completed Level reward payouts**).
2. Input `PERSONAL` as the claim type.
3. Input `7` as the completed level number.
4. The system validates complete profiles, banking details, rules acceptance, milestone completions, locks the claim (`is_locked = True`), and spawns a `PENDING` claim with reward amount `INR 10000.00`.
5. Exit back to the Main Menu.

### Step 2: Admin Auditing & Manual Payout Ledger
1. Select option `3` (**Administrator Control Workspace**).
2. Choose option `1` (**Audit pending Reward Claims queue**). You will see your citizen's pending Level 7 claim.
3. Type `approve` and press enter to approve the claim. This automatically generates a corresponding pending `PaymentTransaction` record in the database.
4. Choose option `2` (**Disburse payments and UTR ledger**). You will see the pending transaction.
5. Type `yes` to disburse payment and enter a mock commercial bank reference number (e.g. `UTR-MOCK-90218201`).
6. The system transitions the payment to `PAID`, sets the claim to `PAID`, and unlocks the milestone lock (`is_locked = False`).

---

## 🛡️ Scenario D: Telemetry, System Logs, & Feature Flags

Explore Developer and Admin telemetry:
1. Return to the Main Menu and select option `4` (**Developer Monitoring Workspace**).
2. Select option `1` (**Check live System telemetry status**) to query CPU, RAM, active DB pools, and latencies.
3. Choose option `2` (**Explore active system logs**) to review developer diagnostics logging.
4. Choose option `3` (**Toggle platform Feature Flag**) to dynamically toggle a settings key (e.g., set `MAINTENANCE_MODE` to `TRUE`).

---

## 🧹 Scenario E: Database Deep Cleanup (Pristine Restore)

After completing all manual testing, return to the Main Menu and select option `5` (**Restore Database Pristine state**). Confirm by typing `yes` when prompted.

This deep cleanup utility:
- Temporarily disables immutability triggers.
- Cascades deletion of all created payment transactions, audit logs, reward claims, waste deposits, invitation codes, teams, rules acceptance, and profiles linked to test accounts starting with `testcitizen_` and `testleader_`.
- Deletes the test user accounts themselves.
- Re-enables the immutability trigger constraints.
- Restores the database completely to its original seeding state, leaving absolutely zero trash records behind!
