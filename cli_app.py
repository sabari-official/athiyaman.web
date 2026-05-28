import sys
import os
import datetime
import uuid
from typing import Optional
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from sqlalchemy import text

# Import core FastAPI app
from backend.main import app
from backend.core.database import SessionLocal
from backend.database.models import (
    User, UserProfile, RulesAcceptance, Team, TeamMember, ReferralCode,
    WasteRecord, WasteStatusHistory, PersonalLevelProgress, TeamLevelProgress,
    RewardClaim, PaymentTransaction, PaymentAuditLog, Notification,
    NotificationLog, Announcement, AuditLog, SystemLog, SystemSetting, Level
)
from backend.utils.security import create_access_token

# Initialize HTTP client session
client = TestClient(app)

# Colorized Terminal Escapes for high contrast, premium aesthetics
CLR_HEADER = "\033[95m"
CLR_BLUE = "\033[94m"
CLR_CYAN = "\033[96m"
CLR_SUCCESS = "\033[92m"
CLR_WARNING = "\033[93m"
CLR_FAIL = "\033[91m"
CLR_RESET = "\033[0m"
CLR_BOLD = "\033[1m"

def print_header(title: str):
    print(f"\n{CLR_BOLD}{CLR_HEADER}=== {title} ==={CLR_RESET}")

def print_success(msg: str):
    print(f"{CLR_SUCCESS}[SUCCESS] {msg}{CLR_RESET}")

def print_warning(msg: str):
    print(f"{CLR_WARNING}[WARNING] {msg}{CLR_RESET}")

def print_fail(msg: str):
    print(f"{CLR_FAIL}[FAIL] {msg}{CLR_RESET}")

def print_info(msg: str):
    print(f"{CLR_BLUE}[INFO] {msg}{CLR_RESET}")

class CLIContext:
    """Stores in-memory user authentication state across workspace panels."""
    def __init__(self):
        self.username: Optional[str] = None
        self.role: Optional[str] = None
        self.user_id: Optional[uuid.UUID] = None
        self.access_token: Optional[str] = None

    def get_auth_headers(self) -> dict:
        if self.access_token:
            return {"Authorization": f"Bearer {self.access_token}"}
        return {}

    def get_admin_headers(self) -> dict:
        """Helper to generate a system administrator token on the fly for restricted operations."""
        admin_token = create_access_token(user_id="00000000-0000-7000-0000-000000000001", role="ADMIN")
        return {"Authorization": f"Bearer {admin_token}"}

    def get_developer_headers(self) -> dict:
        """Helper to generate a developer token on the fly for restricted operations."""
        dev_token = create_access_token(user_id="00000000-0000-7000-0000-000000000002", role="DEVELOPER")
        return {"Authorization": f"Bearer {dev_token}"}

    def is_logged_in(self) -> bool:
        return self.access_token is not None

    def clear(self):
        self.username = None
        self.role = None
        self.user_id = None
        self.access_token = None

ctx = CLIContext()

def purge_test_data():
    """Deep purges all test citizens and associated dependencies to keep database pristine."""
    print_header("PURGE AND RESTORE DATABASE")
    print_warning("This will cascade-delete all test users starting with 'testcitizen_' and 'testleader_'!")
    confirm = input("Are you absolutely sure you want to proceed? (yes/no): ").strip().lower()
    if confirm != "yes":
        print_info("Purge cancelled.")
        return

    db: Session = SessionLocal()
    try:
        # Search test users
        test_users = db.query(User).filter(
            (User.username.like("testcitizen_%")) | (User.username.like("testleader_%"))
        ).all()
        
        if not test_users:
            print_success("No stale test accounts found. Database is already clean.")
            return

        print_info(f"Found {len(test_users)} test account(s). Purging all logs and records...")

        # Disable immutable triggers temporarily during cleanups to bypass restrict validations
        db.execute(text("ALTER TABLE audit_logs DISABLE TRIGGER trg_immutable_audit"))
        
        for u in test_users:
            print(f"Purging dependencies for user: {u.username} (ID: {u.id})")
            
            # 1. Delete payment logs
            claims = db.query(RewardClaim).filter(RewardClaim.user_id == u.id).all()
            for c in claims:
                txs = db.query(PaymentTransaction).filter(PaymentTransaction.claim_id == c.id).all()
                for tx in txs:
                    db.query(PaymentAuditLog).filter(PaymentAuditLog.payment_id == tx.id).delete()
                    db.query(PaymentTransaction).filter(PaymentTransaction.id == tx.id).delete()
                db.query(RewardClaim).filter(RewardClaim.id == c.id).delete()

            # 2. Delete waste records
            waste_records = db.query(WasteRecord).filter(WasteRecord.user_id == u.id).all()
            for w in waste_records:
                db.query(WasteStatusHistory).filter(WasteStatusHistory.waste_record_id == w.id).delete()
                db.query(WasteRecord).filter(WasteRecord.id == w.id).delete()

            # 3. Delete notifications
            db.query(NotificationLog).filter(NotificationLog.user_id == u.id).delete()
            db.query(Notification).filter(Notification.created_by == u.id).delete()
            db.query(Announcement).filter(Announcement.created_by == u.id).delete()

            # 4. Delete referral codes
            db.query(ReferralCode).filter(ReferralCode.generated_by == u.id).delete()

            # 5. Delete team memberships
            db.query(TeamMember).filter(TeamMember.member_id == u.id).delete()

            # 6. Delete teams led by user
            teams = db.query(Team).filter(Team.leader_id == u.id).all()
            for t in teams:
                db.query(ReferralCode).filter(ReferralCode.team_id == t.id).delete()
                db.query(TeamMember).filter(TeamMember.team_id == t.id).delete()
                db.query(Team).filter(Team.id == t.id).delete()

            # 7. Delete profiles and progress tracking
            db.query(PersonalLevelProgress).filter(PersonalLevelProgress.user_id == u.id).delete()
            db.query(TeamLevelProgress).filter(TeamLevelProgress.team_id.in_(
                db.query(Team.id).filter(Team.leader_id == u.id)
            )).delete(synchronize_session=False)
            db.query(RulesAcceptance).filter(RulesAcceptance.user_id == u.id).delete()
            db.query(UserProfile).filter(UserProfile.user_id == u.id).delete()
            db.query(AuditLog).filter(AuditLog.user_id == u.id).delete()

        db.commit()

        # Delete users
        for u in test_users:
            db.query(User).filter(User.id == u.id).delete()
        
        db.commit()
        print_success("Database deep cleanup completed successfully. Restored to clean state!")
    except Exception as e:
        db.rollback()
        print_fail(f"Cleanup failed during database cascades: {e}")
    finally:
        try:
            db.execute(text("ALTER TABLE audit_logs ENABLE TRIGGER trg_immutable_audit"))
            db.commit()
        except Exception:
            pass
        db.close()

# ==========================================
# CITIZEN WORKSPACE FLOWS
# ==========================================

def citizen_signup():
    print_header("CITIZEN SIGNUP")
    print_warning("Username must start with 'testcitizen_' or 'testleader_' for auto-purging!")
    username = input("Username (e.g. testcitizen_ramesh): ").strip()
    phone = input("Phone Number (10 digits): ").strip()
    password = input("Password: ").strip()
    referral = input("Referral Code (Optional): ").strip()

    payload = {
        "username": username,
        "phone_number": phone,
        "password": password,
    }
    if referral:
        payload["referral_code"] = referral

    response = client.post("/api/v1/auth/signup", json=payload)
    if response.status_code == 201:
        data = response.json()
        print_success(f"Citizen registered successfully! ID: {data['id']}")
    else:
        print_fail(f"Signup failed: {response.json()}")

def citizen_login():
    print_header("CITIZEN LOGIN")
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    payload = {
        "username": username,
        "password": password
    }
    response = client.post("/api/v1/auth/login", json=payload)
    if response.status_code == 200:
        data = response.json()
        ctx.access_token = data["access_token"]
        ctx.username = username
        
        if data.get("must_change_password"):
            print_warning("Your account requires a mandatory password change.")
            new_password = input("Enter new password: ").strip()
            cp_payload = {
                "current_password": password,
                "new_password": new_password
            }
            cp_response = client.post("/api/v1/auth/change-password", headers=ctx.get_auth_headers(), json=cp_payload)
            if cp_response.status_code == 200:
                print_success("Password changed successfully! You will need to login again.")
                ctx.access_token = None
                ctx.username = None
                return
            else:
                print_fail(f"Failed to change password: {cp_response.json()}")
                ctx.access_token = None
                ctx.username = None
                return
        
        # Query profile to get ID and Role
        profile_res = client.get("/api/v1/profiles/me", headers=ctx.get_auth_headers())
        if profile_res.status_code == 200:
            p_data = profile_res.json()
            ctx.user_id = uuid.UUID(p_data["user_id"])
            
            # Fetch user account role
            db: Session = SessionLocal()
            usr = db.query(User).filter(User.id == ctx.user_id).first()
            ctx.role = usr.role if usr else "MEMBER"
            db.close()
            
        print_success(f"Logged in successfully as {ctx.username} (Role: {ctx.role})!")
    else:
        print_fail(f"Login failed: {response.json()}")

def view_profile():
    if not ctx.is_logged_in():
        print_warning("You must login first.")
        return
    print_header("VIEW PERSONAL PROFILE")
    response = client.get("/api/v1/profiles/me", headers=ctx.get_auth_headers())
    if response.status_code == 200:
        p = response.json()
        print(f"User ID:           {p['user_id']}")
        print(f"Full Name:         {p['full_name']}")
        print(f"Pincode:           {p['pincode']}")
        print(f"District:          {p['district']}")
        print(f"Bank Verified:     {p['bank_verified']}")
        print(f"Profile Completed: {p['profile_completion']}%")
    else:
        print_fail(f"Could not load profile: {response.json()}")

def complete_profile():
    if not ctx.is_logged_in():
        print_warning("You must login first.")
        return
    print_header("UPDATE PROFILE (100% COMPLETION MOCK)")
    payload = {
        "full_name": "Ramesh Kumar",
        "gender": "MALE",
        "dob": "1990-01-01",
        "email": f"test_{ctx.username}@email.com",
        "state": "Tamil Nadu",
        "district": "Madurai",
        "pincode": "625001",
        "door_no": "123",
        "street_name": "Temple St",
        "landmark": "Near Main Tower",
        "post_office": "Madurai GPO",
        "city": "Madurai",
        "aadhaar": "".join(str(uuid.uuid4().int)[:12]),  # Secure random 12 digits
        "bank_name": "State Bank of India",
        "account_number": "123456789012",
        "ifsc_code": "SBIN0001234",
        "nominee_name": "Sita Kumar",
        "nominee_relationship": "SPOUSE",
        "nominee_phone": "9876543210",
        "nominee_door_no": "123",
        "nominee_street_name": "Temple St",
        "nominee_landmark": "Near Main Tower",
        "nominee_post_office": "Madurai GPO",
        "nominee_city": "Madurai",
        "nominee_district": "Madurai",
        "nominee_state": "Tamil Nadu",
        "nominee_pincode": "625001"
    }
    response = client.put("/api/v1/profiles/me", headers=ctx.get_auth_headers(), json=payload)
    if response.status_code == 200:
        p = response.json()
        print_success(f"Profile updated successfully! Completion: {p['profile_completion']}%")
    else:
        print_fail(f"Profile update failed: {response.json()}")

def accept_platform_rules():
    if not ctx.is_logged_in():
        print_warning("You must login first.")
        return
    print_header("ACCEPT platform RULES (CLICK-WRAP)")
    payload = {
        "rules_version": "v1.0"
    }
    response = client.post("/api/v1/profiles/me/accept-rules", headers=ctx.get_auth_headers(), json=payload)
    if response.status_code == 200:
        print_success("Rules accepted successfully! You are now a verified citizen.")
        # Reload context role (Leader applications or role toggles might shift state)
        ctx.role = "LEADER" if ctx.role == "LEADER" else "MEMBER"
    else:
        print_fail(f"Rules acceptance failed: {response.json()}")

def create_team():
    if not ctx.is_logged_in():
        print_warning("You must login first.")
        return
    print_header("CREATE TEAM (Requires LEADER role)")
    team_name = input("Team Name: ").strip()
    state = input("State: ").strip()
    district = input("District: ").strip()
    pincode = input("Pincode: ").strip()
    door_no = input("Door Number (Optional): ").strip()
    street_name = input("Street Name: ").strip()
    post_office = input("Post Office: ").strip()
    city = input("City: ").strip()

    payload = {
        "team_name": team_name,
        "state": state,
        "district": district,
        "pincode": pincode,
        "door_no": door_no if door_no else None,
        "street_name": street_name,
        "post_office": post_office,
        "city": city
    }
    response = client.post("/api/v1/teams/", headers=ctx.get_auth_headers(), json=payload)
    if response.status_code == 201:
        data = response.json()
        print_success(f"Team created successfully! Code: {data['team_code']}")
    else:
        print_fail(f"Team creation failed: {response.json()}")

def generate_referral_code():
    if not ctx.is_logged_in():
        print_warning("You must login first.")
        return
    print_header("GENERATE INVITE REFERRAL CODE")
    print("Types: LEADER (Admin only) or TEAM (Leaders only)")
    ref_type = input("Referral Type (LEADER/TEAM): ").strip().upper()
    level_num = int(input("Milestone Level (1-6): ").strip())

    payload = {
        "referral_type": ref_type,
        "level_number": level_num
    }
    # Enforce admin headers dynamically if user requests Admin-only LEADER code
    headers = ctx.get_admin_headers() if ref_type == "LEADER" else ctx.get_auth_headers()
    
    response = client.post("/api/v1/referrals/", headers=headers, json=payload)
    if response.status_code == 201:
        data = response.json()
        print_success(f"Invite code generated successfully! Code: {data['code']} (Max Usage: {data['max_usage']})")
    else:
        print_fail(f"Code generation failed: {response.json()}")

def view_level_progress():
    if not ctx.is_logged_in():
        print_warning("You must login first.")
        return
    print_header("CHECK SEQUENTIAL PROGRESS DETAILS")
    print_info("Fetching Individual personal level metrics (Levels 7-11)...")
    res_p = client.get("/api/v1/levels/personal", headers=ctx.get_auth_headers())
    if res_p.status_code == 200:
        p_list = res_p.json()
        for lvl in p_list:
            comp_txt = f"{CLR_SUCCESS}COMPLETED{CLR_RESET}" if lvl['completed'] else f"{CLR_WARNING}INCOMPLETE{CLR_RESET}"
            print(f"Level {lvl['level_number']}: Progress: {lvl['waste_kg']}/{lvl['requirement_value']} KG | Status: {comp_txt} | Payout reward: INR {lvl['reward_amount']}")
    
    print_info("Fetching Team progression level metrics (Levels 1-6)...")
    res_t = client.get("/api/v1/levels/team", headers=ctx.get_auth_headers())
    if res_t.status_code == 200:
        t_list = res_t.json()
        for lvl in t_list:
            comp_txt = f"{CLR_SUCCESS}COMPLETED{CLR_RESET}" if lvl['completed'] else f"{CLR_WARNING}INCOMPLETE{CLR_RESET}"
            print(f"Level {lvl['level_number']}: Members: {lvl['current_progress']}/{lvl['requirement_value']} | Status: {comp_txt} | Payout reward: INR {lvl['reward_amount']}")

def submit_reward_claim():
    if not ctx.is_logged_in():
        print_warning("You must login first.")
        return
    print_header("SUBMIT MILESTONE REWARD CLAIM")
    claim_type = input("Claim Type (PERSONAL/TEAM): ").strip().upper()
    level_num = int(input("Completed Milestone Level Number: ").strip())

    payload = {
        "claim_type": claim_type,
        "level_number": level_num
    }
    response = client.post("/api/v1/rewards/claims", headers=ctx.get_auth_headers(), json=payload)
    if response.status_code == 201:
        data = response.json()
        print_success(f"Reward claim submitted successfully!")
        print(f"Claim ID:     {data['claim_id']}")
        print(f"Disbursment: INR {data['amount']}")
        print(f"Audit Status: {data['status']}")
    else:
        print_fail(f"Claim failed: {response.json()}")

def view_notifications():
    if not ctx.is_logged_in():
        print_warning("You must login first.")
        return
    print_header("CITIZEN NOTIFICATIONS INBOX")
    response = client.get("/api/v1/notifications", headers=ctx.get_auth_headers())
    if response.status_code == 200:
        data = response.json()
        print(f"Total Notifications: {data['total']}")
        for index, item in enumerate(data['items'], start=1):
            read_status = f"{CLR_SUCCESS}READ{CLR_RESET}" if item['is_read'] else f"{CLR_WARNING}UNREAD{CLR_RESET}"
            print(f"\n{index}. [{read_status}] Notification Log ID: {item['id']}")
            print(f"   Title:   {item['notification']['title']}")
            print(f"   Message: {item['notification']['message']}")
            print(f"   Target:  {item['notification']['target_type']}")
            if not item['is_read']:
                mark = input("   Mark this notification as read? (yes/no): ").strip().lower()
                if mark == 'yes':
                    client.put(f"/api/v1/notifications/{item['id']}/read", headers=ctx.get_auth_headers())
                    print_success("Marked as read.")
    else:
        print_fail(f"Failed to load notifications: {response.json()}")

def citizen_menu():
    while True:
        print(f"\n{CLR_BOLD}{CLR_BLUE}=== CITIZEN WORKSPACE ==={CLR_RESET}")
        print(f"Current Session: {ctx.username or 'visitor'} | Role: {ctx.role or 'None'}")
        print("1. Interactive Citizen Signup")
        print("2. Login Citizen")
        print("3. View Profile Details")
        print("4. Onboard Profile details to 100%")
        print("5. Accept click-wrap rules (Unlocks verified citizen status)")
        print("6. Register a Team (Requires LEADER role)")
        print("7. Generate invite Referral Codes")
        print("8. View personal and team level progress details")
        print("9. Claim Completed Level reward payouts")
        print("10. View Notifications Inbox")
        print("0. Back to Main Menu")
        choice = input("Select operation (0-10): ").strip()
        
        if choice == "1": citizen_signup()
        elif choice == "2": citizen_login()
        elif choice == "3": view_profile()
        elif choice == "4": complete_profile()
        elif choice == "5": accept_platform_rules()
        elif choice == "6": create_team()
        elif choice == "7": generate_referral_code()
        elif choice == "8": view_level_progress()
        elif choice == "9": submit_reward_claim()
        elif choice == "10": view_notifications()
        elif choice == "0": break
        else: print_warning("Invalid choice.")

# ==========================================
# WASTE MANAGER WORKSPACE FLOWS
# ==========================================

def log_citizen_waste():
    print_header("LOG CITIZEN WASTE DEPOSIT")
    citizen_id_str = input("Target Citizen User ID: ").strip()
    center_id_str = input("Collection Center ID (or blank to use Chennai Center): ").strip()
    weight = float(input("Verified Weight (KG, e.g. 15.0): ").strip())
    location = input("Deposit Counter / Counter 1: ").strip()

    if not center_id_str:
        # Default seed center Chennai
        center_id_str = "00000000-0000-7000-0000-000000000301"

    payload = {
        "user_id": citizen_id_str,
        "center_id": center_id_str,
        "weight_kg": weight,
        "image_path": "uploads/waste/scale_photo_123.jpg",
        "collection_date": str(datetime.date.today()),
        "location": location
    }
    
    # Send using dynamic Administrator headers (as Waste Manager)
    response = client.post("/api/v1/waste", headers=ctx.get_admin_headers(), json=payload)
    if response.status_code == 201:
        data = response.json()
        print_success("Waste deposit logged and automatically verified by Waste Manager!")
        print(f"Record ID:    {data['id']}")
        print(f"Weight:       {data['weight_kg']} KG")
        print(f"Audit Status: {data['verification_status']}")
    else:
        print_fail(f"Failed to log waste: {response.json()}")

def manager_menu():
    while True:
        print(f"\n{CLR_BOLD}{CLR_BLUE}=== WASTE MANAGER WORKSPACE ==={CLR_RESET}")
        print("1. Log Citizen Waste Deposit (Directly updates citizen progress levels via SQL triggers)")
        print("0. Back to Main Menu")
        choice = input("Select operation (0-1): ").strip()
        if choice == "1": log_citizen_waste()
        elif choice == "0": break
        else: print_warning("Invalid choice.")

# ==========================================
# ADMINISTRATOR WORKSPACE FLOWS
# ==========================================

def view_claims_queue():
    print_header("ADMINISTRATIVE REWARD CLAIMS QUEUE")
    response = client.get("/api/v1/admin/claims", headers=ctx.get_admin_headers())
    if response.status_code == 200:
        data = response.json()
        print(f"Total Claims: {data['total']}")
        for index, item in enumerate(data['items'], start=1):
            print(f"\n{index}. Claim ID:   {item['claim_id']}")
            print(f"   Citizen ID: {item['user_id']}")
            print(f"   Level:      {item['level_number']} ({item['claim_type']})")
            print(f"   Amount:    INR {item['amount']}")
            print(f"   Status:     {item['status']}")
            
            if item['status'] == 'PENDING':
                action = input("   Approve or Reject this claim? (approve/reject/skip): ").strip().lower()
                if action == 'approve':
                    client.post(f"/api/v1/admin/claims/{item['claim_id']}/approve", headers=ctx.get_admin_headers())
                    print_success("Claim Approved! Pending Payment Transaction spawned.")
                elif action == 'reject':
                    reason = input("   Rejection Reason: ").strip()
                    payload = {"comments": reason}
                    client.post(f"/api/v1/admin/claims/{item['claim_id']}/reject", headers=ctx.get_admin_headers(), json=payload)
                    print_success("Claim Rejected and lock released.")
    else:
        print_fail(f"Failed to load claims: {response.json()}")

def view_payouts_ledger():
    print_header("ADMINISTRATIVE MANUAL PAYOUTS LEDGER")
    response = client.get("/api/v1/payments", headers=ctx.get_admin_headers())
    if response.status_code == 200:
        data = response.json()
        print(f"Total Transactions: {data['total']}")
        for index, item in enumerate(data['items'], start=1):
            print(f"\n{index}. Transaction ID: {item['transaction_id']}")
            print(f"   Claim ID:       {item['claim_id']}")
            print(f"   Amount:         INR {item['amount']}")
            print(f"   Status:         {item['status']}")
            print(f"   UTR Reference:  {item['transaction_reference'] or 'None'}")
            
            if item['status'] == 'PENDING':
                action = input("   Disburse payment and log manual reference? (yes/no): ").strip().lower()
                if action == 'yes':
                    utr = input("   Enter Unique UTR Bank Reference Number: ").strip()
                    payload = {
                        "transaction_reference": utr,
                        "paid_at": datetime.datetime.utcnow().isoformat()
                    }
                    client.post(f"/api/v1/admin/payments/{item['transaction_id']}/paid", headers=ctx.get_admin_headers(), json=payload)
                    print_success("Payment transaction marked as PAID. Claim fully unlocked!")
    else:
        print_fail(f"Failed to load payouts: {response.json()}")

def view_kpi_dashboard():
    print_header("REAL-TIME KPI dashboard ANALYTICS")
    response = client.get("/api/v1/analytics/dashboard", headers=ctx.get_admin_headers())
    if response.status_code == 200:
        stats = response.json()
        print(f"Total Registered Users:  {stats['total_users']}")
        print(f"Total Registered Teams:  {stats['total_teams']}")
        print(f"Total Team Members:      {stats['total_members']}")
        print(f"Total Approved Waste:    {stats['total_waste']} KG")
        print(f"Total Reward Claims:     {stats['total_claims']}")
        print(f"Total Disbursed Payouts: INR {stats['total_payments']}")
        
        snap = input("\nTrigger a historical precalculated metrics capture snap? (yes/no): ").strip().lower()
        if snap == 'yes':
            client.post("/api/v1/admin/analytics/snapshots", headers=ctx.get_admin_headers())
            print_success("Historical snapshot snaps saved successfully!")
    else:
        print_fail(f"Failed to load KPI stats: {response.json()}")

def view_audit_logs():
    print_header("IMMUTABLE WRITING AUDIT TRAILS EXPLORER")
    response = client.get("/api/v1/admin/audits", headers=ctx.get_admin_headers())
    if response.status_code == 200:
        data = response.json()
        print(f"Total System Logs: {data['total']}")
        for index, item in enumerate(data['items'], start=1):
            print(f"\n{index}. Log ID:      {item['id']}")
            print(f"   Performed By: User ID {item['user_id']} | Role: {item['role']}")
            print(f"   Action Event: {item['action']} on {item['entity_type']} (ID: {item['entity_id']})")
            print(f"   New Values:   {item['new_values']}")
            print(f"   Date:         {item['created_at']}")
    else:
        print_fail(f"Failed to load audit logs: {response.json()}")

def create_platform_announcement():
    print_header("CREATE CLICK-WRAP platform ANNOUNCEMENT")
    title = input("Announcement Title: ").strip()
    msg = input("Announcement Click-Wrap Message Content: ").strip()
    
    payload = {
        "title": title,
        "message": msg,
        "start_date": str(datetime.date.today()),
        "end_date": str(datetime.date.today() + datetime.timedelta(days=30))
    }
    response = client.post("/api/v1/admin/announcements", headers=ctx.get_admin_headers(), json=payload)
    if response.status_code == 201:
        print_success("Click-wrap announcement broadcasted successfully!")
    else:
        print_fail(f"Failed to create announcement: {response.json()}")

def broadcast_targeted_notification():
    print_header("BROADCAST TARGETED ROLE-BASED NOTIFICATION")
    title = input("Notification Title: ").strip()
    msg = input("Notification Message Body: ").strip()
    target = input("Target Scope Role (ALL/MEMBER/LEADER/ADMIN): ").strip().upper()

    payload = {
        "title": title,
        "message": msg,
        "target_type": target
    }
    response = client.post("/api/v1/admin/notifications", headers=ctx.get_admin_headers(), json=payload)
    if response.status_code == 201:
        print_success("Target notification delivered and delivered triggers logged dynamically!")
    else:
        print_fail(f"Failed to broadcast notification: {response.json()}")

def admin_menu():
    while True:
        print(f"\n{CLR_BOLD}{CLR_BLUE}=== ADMINISTRATOR WORKSPACE ==={CLR_RESET}")
        print("1. Audit pending Reward Claims queue (Approve/Reject)")
        print("2. Disburse payments and log bank references (UTR ledger)")
        print("3. View precalculated KPI Analytics dashboard")
        print("4. Explore immutable Audit Trails logs")
        print("5. Create platform Announcement click-wrap broadcast")
        print("6. Broadcast targeted role-scoped notification (Delivered triggers)")
        print("0. Back to Main Menu")
        choice = input("Select operation (0-6): ").strip()
        
        if choice == "1": view_claims_queue()
        elif choice == "2": view_payouts_ledger()
        elif choice == "3": view_kpi_dashboard()
        elif choice == "4": view_audit_logs()
        elif choice == "5": create_platform_announcement()
        elif choice == "6": broadcast_targeted_notification()
        elif choice == "0": break
        else: print_warning("Invalid choice.")

# ==========================================
# DEVELOPER WORKSPACE FLOWS
# ==========================================

def view_developer_telemetry():
    print_header("DEVELOPER SYSTEM telemetry HEALTH")
    response = client.get("/api/v1/developer/system/status", headers=ctx.get_developer_headers())
    if response.status_code == 200:
        telemetry = response.json()
        print(f"System CPU Usage:         {telemetry['cpu_usage']}%")
        print(f"System Memory Usage:      {telemetry['memory_usage']}%")
        print(f"Active DB Connections:    {telemetry['active_db_connections']} pools")
        print(f"API Middleware Latency:   {telemetry['api_latency_ms']} ms")
    else:
        print_fail(f"Failed to load telemetry: {response.json()}")

def explore_system_logs():
    print_header("DEVELOPER SYSTEM LOGS EXPLORER")
    response = client.get("/api/v1/developer/system/logs", headers=ctx.get_developer_headers())
    if response.status_code == 200:
        data = response.json()
        print(f"Total System Logs: {data['total']}")
        for index, item in enumerate(data['items'], start=1):
            print(f"\n{index}. [{item['log_level']}] Source: {item['source']}")
            print(f"   Message: {item['message']}")
            print(f"   Date:    {item['created_at']}")
    else:
        print_fail(f"Failed to load system logs: {response.json()}")

def toggle_feature_flag():
    print_header("TOGGLE platform FEATURE FLAG CONFIG")
    key = input("Feature Setting Key (e.g. MAINTENANCE_MODE): ").strip()
    val = input("Feature Flag Value (e.g. TRUE/FALSE): ").strip()

    payload = {
        "setting_key": key,
        "setting_value": val
    }
    response = client.post("/api/v1/developer/features/toggle", headers=ctx.get_developer_headers(), json=payload)
    if response.status_code == 200:
        data = response.json()
        print_success(f"Feature config updated! Key: {data['setting_key']} -> {data['setting_value']} (Updated At: {data['updated_at']})")
    else:
        print_fail(f"Failed to toggle feature flag: {response.json()}")

def trigger_system_backup():
    print_header("TRIGGER database BACKUP")
    response = client.post("/api/v1/developer/backups/create", headers=ctx.get_developer_headers())
    if response.status_code == 201:
        print_success("Database backup triggered and completed successfully!")
    else:
        print_fail(f"Backup failed: {response.json()}")

def developer_menu():
    while True:
        print(f"\n{CLR_BOLD}{CLR_BLUE}=== DEVELOPER MONITORING CONSOLE ==={CLR_RESET}")
        print("1. Check live System telemetry status (CPU, RAM, Connections)")
        print("2. Explore active diagnostics system logs")
        print("3. Toggle platform Feature Flag configurations")
        print("4. Trigger administrative database Backups")
        print("0. Back to Main Menu")
        choice = input("Select operation (0-4): ").strip()
        
        if choice == "1": view_developer_telemetry()
        elif choice == "2": explore_system_logs()
        elif choice == "3": toggle_feature_flag()
        elif choice == "4": trigger_system_backup()
        elif choice == "0": break
        else: print_warning("Invalid choice.")

# ==========================================
# MAIN APPLICATION RENDERER
# ==========================================

def main_app():
    print(f"\n{CLR_BOLD}{CLR_CYAN}========================================================={CLR_RESET}")
    print(f"{CLR_BOLD}{CLR_CYAN}          ATHIYAMAN PLATFORM - DIGITAL INDIA (PHASE 1)   {CLR_RESET}")
    print(f"{CLR_BOLD}{CLR_CYAN}                 INTERACTIVE TESTING CONSOLE             {CLR_RESET}")
    print(f"{CLR_BOLD}{CLR_CYAN}========================================================={CLR_RESET}")
    
    while True:
        print(f"\n{CLR_BOLD}{CLR_CYAN}=== MAIN simulations SELECTOR ==={CLR_RESET}")
        print("1. Citizen Workspace (Signup, Login, Profiles, Teams, sequential levels, Claims)")
        print("2. Waste Manager Workspace (Weighing scales collections logging)")
        print("3. Administrator Control Workspace (Auditing reward claims, KPI dashboard, broadcast notifications)")
        print("4. Developer Monitoring Workspace (telemetry telemetry, Feature flags, Backup triggers)")
        print("5. Restore Database Pristine state (Purges test sessions inputs and outputs)")
        print("6. Exit Application")
        
        choice = input("Select testing workspace (1-6): ").strip()
        
        if choice == "1": citizen_menu()
        elif choice == "2": manager_menu()
        elif choice == "3": admin_menu()
        elif choice == "4": developer_menu()
        elif choice == "5": purge_test_data()
        elif choice == "6":
            print_success("Thank you for pair testing the Athiyaman Platform. Goodbye!")
            sys.exit(0)
        else:
            print_warning("Invalid workspace selected.")

if __name__ == "__main__":
    main_app()
