import datetime
import uuid
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from backend.main import app
from backend.core.database import SessionLocal
from backend.database.models import (
    ReferralCode, User, UserProfile, RulesAcceptance, Team, CollectionCenter,
    WasteRecord, WasteStatusHistory, PersonalLevelProgress, RewardClaim,
    PaymentTransaction, PaymentAuditLog, Notification, NotificationLog,
    Announcement, AuditLog, AnalyticsSnapshot, SystemLog, SystemSetting
)
from backend.utils.security import create_access_token

client = TestClient(app)

def run_integration_tests():
    print("=========================================================")
    print("ATHIYAMAN PLATFORM - AUTOMATED INTEGRATION CHECKER")
    print("=========================================================")
    
    db: Session = SessionLocal()
    test_referral = f"TEST-LEADER-{uuid.uuid4().hex[:6].upper()}"
    test_username = f"testcitizen_{uuid.uuid4().hex[:6]}"
    test_phone = f"9{uuid.uuid4().hex[:9].lower()}"[:10]  # generate a 10 digit number starting with 9
    
    # Ensure only numeric digits
    test_phone = "".join(x for x in test_phone if x.isdigit())
    if len(test_phone) < 10:
        test_phone = test_phone.zfill(10)
    test_phone = test_phone[:10]
    
    test_pwd = "SecurePassword123!"
    
    ref_id = uuid.uuid4()
    user_id = None
    access_token = None
    team_id = None
    gen_ref_id = None
    center_id = None
    created_temp_center = False
    logged_waste_id = None
    api_center_id = None
    claim_id = None
    tx_id = None
    notification_id = None
    announcement_id = None
    setting_key = None
    
    try:
        # 1. Setup - Insert a temporary active Leader referral code
        print(f"\n--- Step 1: Seeding Test Referral Code [{test_referral}] ---")
        ref = ReferralCode(
            id=ref_id,
            code=test_referral,
            referral_type="LEADER",
            generated_by=uuid.UUID("00000000-0000-7000-0000-000000000001"), # System Admin ID
            max_usage=1,
            used_count=0,
            is_active=True,
            expires_at=datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        )
        db.add(ref)
        db.commit()
        print("[SUCCESS] Seeding complete.")

        # 2. Test Signup Endpoint
        print(f"\n--- Step 2: Testing POST /api/v1/auth/signup ---")
        signup_payload = {
            "username": test_username,
            "phone_number": test_phone,
            "password": test_pwd,
            "referral_code": test_referral
        }
        response = client.post("/api/v1/auth/signup", json=signup_payload)
        
        print(f"Status Code: {response.status_code}")
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"
        res_data = response.json()
        user_id = uuid.UUID(res_data["id"])
        print("[SUCCESS] Signup endpoint passed!")

        # 3. Test Login Endpoint
        print(f"\n--- Step 3: Testing POST /api/v1/auth/login ---")
        login_payload = {
            "username": test_username,
            "password": test_pwd
        }
        response = client.post("/api/v1/auth/login", json=login_payload)
        
        print(f"Status Code: {response.status_code}")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        res_tokens = response.json()
        access_token = res_tokens["access_token"]
        print("[SUCCESS] Login endpoint passed!")
        
        headers = {"Authorization": f"Bearer {access_token}"}

        # 4. Test GET Profile Endpoint
        print(f"\n--- Step 4: Testing GET /api/v1/profiles/me (New User Profile) ---")
        response = client.get("/api/v1/profiles/me", headers=headers)
        
        print(f"Status Code: {response.status_code}")
        assert response.status_code == 200
        profile_data = response.json()
        assert profile_data["profile_completion"] == 0
        print("[SUCCESS] GET Profile passed!")

        # 5. Test Rule Acceptance Incomplete Rejections
        print(f"\n--- Step 5: Testing Platform Rules Block on Incomplete Profile ---")
        response = client.post(
            "/api/v1/profiles/me/accept-rules", 
            headers=headers,
            json={"rules_version": "v1.0"}
        )
        print(f"Status Code: {response.status_code}")
        assert response.status_code == 403
        print("[SUCCESS] Rule block on incomplete profile passed!")

        # 6. Test Update Profile Endpoint (Triggering 100% completion)
        print(f"\n--- Step 6: Testing PUT /api/v1/profiles/me (Update to 100% Complete) ---")
        update_payload = {
            "full_name": "Ramesh Kumar",
            "gender": "MALE",
            "dob": "1990-01-01",
            "email": "ramesh@email.com",
            "profession": "Developer",
            "state": "Tamil Nadu",
            "district": "Madurai",
            "pincode": "625001",
            "address": "123, Temple St, Madurai",
            "door_no": "No. 12",
            "post_office": "Madurai GPO",
            "aadhaar": "123456789010",
            "bank_name": "State Bank of India",
            "account_number": "123456789012",
            "ifsc_code": "SBIN0001234",
            "nominee_name": "Sita Kumar",
            "nominee_relationship": "SPOUSE",
            "nominee_phone": "9876543210"
        }
        response = client.put("/api/v1/profiles/me", headers=headers, json=update_payload)
        
        print(f"Status Code: {response.status_code}")
        assert response.status_code == 200
        profile_updated = response.json()
        assert profile_updated["profile_completion"] == 100
        print("[SUCCESS] Update profile successfully unlocked 100% completion!")

        # 7. Test Rule Acceptance Success
        print(f"\n--- Step 7: Testing Platform Rules Accept on 100% Completed Profile ---")
        response = client.post(
            "/api/v1/profiles/me/accept-rules", 
            headers=headers,
            json={"rules_version": "v1.0"}
        )
        print(f"Status Code: {response.status_code}")
        assert response.status_code == 200
        print("[SUCCESS] Platform click-wrap accept rule passed!")

        # 8. Test POST Create Team (Module 3)
        print(f"\n--- Step 8: Testing POST /api/v1/teams/ (Leader Creates Team) ---")
        team_name = f"Warriors_{uuid.uuid4().hex[:4].upper()}"
        team_payload = {
            "team_name": team_name,
            "state": "Tamil Nadu",
            "district": "Madurai",
            "pincode": "625001",
            "door_no": "No. 5",
            "street_name": "Temple Street",
            "post_office": "Madurai GPO",
            "city": "Madurai"
        }
        response = client.post("/api/v1/teams/", headers=headers, json=team_payload)
        
        print(f"Status Code: {response.status_code}")
        assert response.status_code == 201
        team_data = response.json()
        team_id = uuid.UUID(team_data["id"])
        print("[SUCCESS] Create Team endpoint passed!")

        # 9. Test GET my-team
        print(f"\n--- Step 9: Testing GET /api/v1/teams/my-team ---")
        response = client.get("/api/v1/teams/my-team", headers=headers)
        
        print(f"Status Code: {response.status_code}")
        assert response.status_code == 200
        print("[SUCCESS] GET my-team passed!")

        # 10. Test GET my-team/roster
        print(f"\n--- Step 10: Testing GET /api/v1/teams/my-team/roster (Empty Roster) ---")
        response = client.get("/api/v1/teams/my-team/roster", headers=headers)
        
        print(f"Status Code: {response.status_code}")
        assert response.status_code == 200
        print("[SUCCESS] GET empty team roster passed!")

        # 11. Test POST Create Referral Code (Module 4)
        print(f"\n--- Step 11: Testing POST /api/v1/referrals/ (Leader Creates Team Referral) ---")
        ref_payload = {
            "referral_type": "TEAM",
            "level_number": 1
        }
        response = client.post("/api/v1/referrals/", headers=headers, json=ref_payload)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.json()}")
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"
        gen_ref = response.json()
        assert gen_ref["referral_type"] == "TEAM"
        assert gen_ref["max_usage"] == 10, "Level 1 Team referral max usage should be strictly 10"
        assert gen_ref["level_number"] == 1
        gen_ref_code = gen_ref["code"]
        gen_ref_id = uuid.UUID(gen_ref["id"])
        print("[SUCCESS] Generate Team Referral Code passed!")

        # 12. Test GET active referral
        print(f"\n--- Step 12: Testing GET /api/v1/referrals/active (Fetch Active Code) ---")
        response = client.get("/api/v1/referrals/active", headers=headers)
        
        print(f"Status Code: {response.status_code}")
        assert response.status_code == 200
        assert response.json()["code"] == gen_ref_code
        print("[SUCCESS] Fetch active referral code passed!")

        # 13. Test Double Active Referral Block
        print(f"\n--- Step 13: Testing Double Team Code Generation Block ---")
        response = client.post("/api/v1/referrals/", headers=headers, json=ref_payload)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.json()}")
        assert response.status_code == 409
        assert response.json()["detail"]["code"] == "ACTIVE_REFERRAL_EXISTS"
        print("[SUCCESS] Double referral code generation successfully blocked!")

        # 15. Test GET /api/v1/levels/team (Module 5)
        print("\n--- Step 15: Testing GET /api/v1/levels/team ---")
        response = client.get("/api/v1/levels/team", headers=headers)
        print(f"Status Code: {response.status_code}")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        team_progress_list = response.json()
        assert len(team_progress_list) == 6, f"Expected 6 team levels progress entries, got {len(team_progress_list)}"
        # Check Level 1 details
        lvl1 = next(x for x in team_progress_list if x["level_number"] == 1)
        assert lvl1["requirement_value"] == 10
        assert lvl1["reward_amount"] == 100.0
        assert lvl1["completed"] is False
        print("[SUCCESS] GET /levels/team passed!")

        # 16. Test GET /api/v1/levels/personal (Module 5)
        print("\n--- Step 16: Testing GET /api/v1/levels/personal ---")
        response = client.get("/api/v1/levels/personal", headers=headers)
        print(f"Status Code: {response.status_code}")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        personal_progress_list = response.json()
        assert len(personal_progress_list) == 5, f"Expected 5 personal levels progress entries, got {len(personal_progress_list)}"
        # Check Level 7 details
        lvl7 = next(x for x in personal_progress_list if x["level_number"] == 7)
        assert lvl7["requirement_value"] == 10.0
        assert lvl7["reward_amount"] == 10000.0
        assert lvl7["completed"] is False
        print("[SUCCESS] GET /levels/personal passed!")

        # 17. Querying or Seeding Collection Center
        print("\n--- Step 17: Querying or Seeding Collection Center ---")
        existing_center = db.query(CollectionCenter).first()
        if not existing_center:
            print("No collection center found. Seeding a temporary active center...")
            temp_center_id = uuid.uuid4()
            center_obj = CollectionCenter(
                id=temp_center_id,
                center_name="TEST Madurai Center",
                district="Madurai",
                pincode="625001",
                address="123 Scale Rd, Madurai",
                is_active=True
            )
            db.add(center_obj)
            db.commit()
            db.refresh(center_obj)
            center_id = temp_center_id
            created_temp_center = True
            print(f"[SUCCESS] Temporary center seeded with ID: {center_id}")
        else:
            center_id = existing_center.id
            print(f"Using existing collection center: {existing_center.center_name} (ID: {center_id})")

        # 18. Testing Citizen Logging Restriction
        print("\n--- Step 18: Testing Citizen Logging Restriction (POST /api/v1/waste as Citizen) ---")
        waste_payload = {
            "user_id": str(user_id),
            "center_id": str(center_id),
            "weight_kg": 15.0,
            "image_path": "uploads/waste/photo_123.jpg",
            "collection_date": "2026-05-27",
            "location": "Counter 1"
        }
        response = client.post("/api/v1/waste", headers=headers, json=waste_payload)
        print(f"Status Code: {response.status_code}")
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
        print("[SUCCESS] Citizen logging restriction successfully enforced!")

        # 19. Testing Admin Logging Waste for Citizen
        print("\n--- Step 19: Testing POST /api/v1/waste as Admin/Manager ---")
        admin_token = create_access_token(user_id=str(uuid.UUID("00000000-0000-7000-0000-000000000001")), role="ADMIN")
        admin_headers = {"Authorization": f"Bearer {admin_token}"}
        
        response = client.post("/api/v1/waste", headers=admin_headers, json=waste_payload)
        print(f"Status Code: {response.status_code}")
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"
        waste_data = response.json()
        logged_waste_id = uuid.UUID(waste_data["id"])
        assert waste_data["verification_status"] == "APPROVED", "Waste logged by manager should be automatically APPROVED"
        assert waste_data["weight_kg"] == 15.0
        print("[SUCCESS] Waste successfully logged and automatically approved by manager!")

        # 20. Testing GET /api/v1/waste as Citizen
        print("\n--- Step 20: Testing GET /api/v1/waste as Citizen ---")
        response = client.get("/api/v1/waste", headers=headers)
        print(f"Status Code: {response.status_code}")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        waste_roster = response.json()
        assert waste_roster["total"] >= 1, "Should return at least the newly logged record"
        matching = next(x for x in waste_roster["items"] if uuid.UUID(x["id"]) == logged_waste_id)
        assert matching["weight_kg"] == 15.0
        print("[SUCCESS] Citizen query roster passed!")

        # 21. Checking Dynamic progression update (Module 5 integration check)
        print("\n--- Step 21: Checking Dynamic Progression Update on Level 7 ---")
        response = client.get("/api/v1/levels/personal", headers=headers)
        print(f"Status Code: {response.status_code}")
        assert response.status_code == 200
        personal_progress_list = response.json()
        lvl7 = next(x for x in personal_progress_list if x["level_number"] == 7)
        print(f"Level 7 completed: {lvl7['completed']}, waste_kg: {lvl7['waste_kg']}")
        assert lvl7["completed"] is True, "Level 7 should have transitioned to completed dynamically via SQL trigger"
        assert lvl7["waste_kg"] == 15.0
        print("[SUCCESS] Dynamic Progression Milestone updated beautifully via SQL Triggers!")

        # 22. Testing Admin Collection Center Creation (POST /api/v1/admin/centers)
        print("\n--- Step 22: Testing POST /api/v1/admin/centers (Admin creates center) ---")
        api_center_name = f"TEST Madurai East {uuid.uuid4().hex[:4].upper()}"
        center_payload = {
            "center_name": api_center_name,
            "state": "Tamil Nadu",
            "district": "Madurai",
            "pincode": "625020",
            "door_no": "No. 456",
            "street_name": "Main Bypass Road",
            "post_office": "Madurai GP",
            "city": "Madurai",
            "latitude": 9.9252,
            "longitude": 78.1198,
            "phone": "0452-999888"
        }
        response = client.post("/api/v1/admin/centers", headers=admin_headers, json=center_payload)
        print(f"Status Code: {response.status_code}")
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"
        api_center_data = response.json()
        api_center_id = uuid.UUID(api_center_data["id"])
        print(f"[SUCCESS] Admin successfully created center with ID: {api_center_id}")

        # 23. Testing GET /api/v1/centers?pincode=625020 (Citizen Pincode Search)
        print("\n--- Step 23: Testing GET /api/v1/centers (Citizen pincode search) ---")
        response = client.get("/api/v1/centers?pincode=625020", headers=headers)
        print(f"Status Code: {response.status_code}")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        centers_search = response.json()
        assert centers_search["total"] >= 1, "Should return at least the newly created center"
        matching_c = next(x for x in centers_search["items"] if uuid.UUID(x["id"]) == api_center_id)
        assert matching_c["center_name"] == api_center_name
        assert matching_c["latitude"] == 9.9252
        print("[SUCCESS] Citizen collection center pincode search passed!")

        # 24. Testing POST /api/v1/admin/centers/{id}/toggle (Admin toggles visibility)
        print("\n--- Step 24: Testing POST /api/v1/admin/centers/{id}/toggle ---")
        response = client.post(f"/api/v1/admin/centers/{api_center_id}/toggle", headers=admin_headers)
        print(f"Status Code: {response.status_code}")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        toggled_center = response.json()
        assert toggled_center["is_active"] is False, "Center is_active should toggle to False"
        
        # Verify hidden from public search now
        response = client.get("/api/v1/centers?pincode=625020", headers=headers)
        centers_search_after = response.json()
        assert api_center_id not in [uuid.UUID(x["id"]) for x in centers_search_after["items"]], "Disabled center should be hidden from public lookups"
        print("[SUCCESS] Admin collection center visibility toggle and active hiding passed!")

        # 25. Testing Reward Claim Blocked on Unverified Bank Details
        print("\n--- Step 25: Testing Reward Claim Blocked on Unverified Bank Details ---")
        # Bank details are automatically verified upon profile update for demo phase.
        # We manually toggle bank_verified to False to test this boundary constraint!
        prof = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        prof.bank_verified = False
        db.commit()

        claim_payload = {
            "claim_type": "PERSONAL_REWARD",
            "level_number": 7
        }
        response = client.post("/api/v1/rewards/claims", headers=headers, json=claim_payload)
        print(f"Status Code: {response.status_code}")
        assert response.status_code == 403
        assert response.json()["detail"]["code"] == "BANK_NOT_VERIFIED"
        print("[SUCCESS] Claim creation blocked on unverified bank details!")

        # 26. Admin Verifies Bank Details Directly in Database
        print("\n--- Step 26: Admin Verifies Bank Details Directly in Database ---")
        prof = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        prof.bank_verified = True
        db.commit()
        print("[SUCCESS] Target citizen banking details marked as verified.")

        # 27. Re-attempt Claim Creation (Success)
        print("\n--- Step 27: Re-attempt Claim Creation (Success) ---")
        response = client.post("/api/v1/rewards/claims", headers=headers, json=claim_payload)
        print(f"Status Code: {response.status_code}")
        assert response.status_code == 201
        claim_data = response.json()
        claim_id = uuid.UUID(claim_data["claim_id"])
        assert claim_data["amount"] == 10000.00
        assert claim_data["status"] == "PENDING"
        assert claim_data["is_locked"] is True
        print(f"[SUCCESS] Claim created successfully with ID: {claim_id}")

        # 28. Testing Duplicate Claim Block
        print("\n--- Step 28: Testing Duplicate Claim Block ---")
        response = client.post("/api/v1/rewards/claims", headers=headers, json=claim_payload)
        print(f"Status Code: {response.status_code}")
        assert response.status_code == 400
        assert response.json()["detail"]["code"] == "PENDING_CLAIM_EXISTS"
        print("[SUCCESS] Duplicate claim block successfully enforced!")

        # 29. Admin Approves Reward Claim
        print("\n--- Step 29: Admin Approves Reward Claim ---")
        response = client.post(f"/api/v1/admin/claims/{claim_id}/approve", headers=admin_headers)
        print(f"Status Code: {response.status_code}")
        assert response.status_code == 200
        approved_claim = response.json()
        assert approved_claim["status"] == "APPROVED"
        print("[SUCCESS] Admin successfully approved the reward claim.")

        # 30. Verify Pending Payment Transaction Created
        print("\n--- Step 30: Verify Pending Payment Transaction Created ---")
        tx = db.query(PaymentTransaction).filter(PaymentTransaction.claim_id == claim_id).first()
        assert tx is not None
        assert tx.status == "PENDING"
        assert tx.amount == 10000.00
        tx_id = tx.id
        print(f"[SUCCESS] Payment transaction auto-created in PENDING state with ID: {tx_id}")

        # 31. Admin Processes manual Payout
        print("\n--- Step 31: Admin Processes Manual Payout ---")
        payout_payload = {
            "transaction_reference": "TXN-MOCK-902182",
            "paid_at": datetime.datetime.utcnow().isoformat()
        }
        response = client.post(f"/api/v1/admin/payments/{tx_id}/paid", headers=admin_headers, json=payout_payload)
        print(f"Status Code: {response.status_code}")
        assert response.status_code == 200
        payout_data = response.json()
        assert payout_data["status"] == "PAID"
        assert payout_data["transaction_reference"] == "TXN-MOCK-902182"
        print("[SUCCESS] Manual ledger payout processes successfully!")

        # 32. Verify Claim and Payout unlocked
        print("\n--- Step 32: Verify Claim and Transaction marked as PAID ---")
        db.refresh(tx)
        assert tx.status == "PAID"
        claim_db = db.query(RewardClaim).filter(RewardClaim.id == claim_id).first()
        assert claim_db.status == "PAID"
        assert claim_db.is_locked is False
        print("[SUCCESS] Milestone reward fully PAID and unlocked!")

        # 33. Admin Broadcasts Targeted Notification
        print("\n--- Step 33: Admin Broadcasts Targeted Notification ---")
        notif_payload = {
            "title": "TEST Milestones Completed",
            "message": "Congratulations! You have completed a platform milestone.",
            "target_type": "LEADER"
        }
        response = client.post("/api/v1/admin/notifications", headers=admin_headers, json=notif_payload)
        print(f"Status Code: {response.status_code}")
        assert response.status_code == 201
        notif_data = response.json()
        notification_id = uuid.UUID(notif_data["id"])
        print(f"[SUCCESS] Admin successfully broadcasted notification with ID: {notification_id}")

        # 34. Citizen Queries Personal Notifications
        print("\n--- Step 34: Citizen Queries Personal Notifications ---")
        response = client.get("/api/v1/notifications", headers=headers)
        print(f"Status Code: {response.status_code}")
        assert response.status_code == 200
        notif_roster = response.json()
        assert notif_roster["total"] >= 1
        matching_notif = next(x for x in notif_roster["items"] if uuid.UUID(x["notification_id"]) == notification_id)
        notification_log_id = uuid.UUID(matching_notif["id"])
        assert matching_notif["is_read"] is False
        print(f"[SUCCESS] Citizen successfully retrieved notification log with ID: {notification_log_id}")

        # 35. Citizen Marks Notification Log as Read
        print("\n--- Step 35: Citizen Marks Notification Log as Read ---")
        response = client.put(f"/api/v1/notifications/{notification_log_id}/read", headers=headers)
        print(f"Status Code: {response.status_code}")
        assert response.status_code == 200
        log_data = response.json()
        assert log_data["is_read"] is True
        assert log_data["read_at"] is not None
        print("[SUCCESS] Notification read-status updated successfully!")

        # 36. Verify Database Audit Immutability Trigger
        print("\n--- Step 36: Verify Database Audit Immutability Trigger ---")
        from sqlalchemy import text
        audit_entry = AuditLog(
            id=uuid.uuid4(),
            action="TEST_MUTATION",
            entity_type="TEST"
        )
        db.add(audit_entry)
        db.commit()

        # Assert that UPDATE query triggers exception
        try:
            audit_entry.action = "ILLEGAL_UPDATE"
            db.commit()
            raise Exception("DATABASE_ALLOWED_AUDIT_LOG_UPDATE")
        except Exception as e:
            db.rollback()
            print(f"Update Blocked as expected: {e}")
            assert "immutable" in str(e).lower() or "forbidden" in str(e).lower()

        # Assert that DELETE query triggers exception
        try:
            db.delete(audit_entry)
            db.commit()
            raise Exception("DATABASE_ALLOWED_AUDIT_LOG_DELETE")
        except Exception as e:
            db.rollback()
            print(f"Delete Blocked as expected: {e}")
            assert "immutable" in str(e).lower() or "forbidden" in str(e).lower()

        # Clean up the test audit entry temporarily bypassing trigger using superuser control
        db.execute(text("ALTER TABLE audit_logs DISABLE TRIGGER trg_immutable_audit"))
        db.query(AuditLog).filter(AuditLog.id == audit_entry.id).delete()
        db.execute(text("ALTER TABLE audit_logs ENABLE TRIGGER trg_immutable_audit"))
        db.commit()
        print("[SUCCESS] Database audit log immutability successfully verified!")

        # 37. Admin Queries Dashboard Statistics
        print("\n--- Step 37: Admin Queries Dashboard Statistics ---")
        response = client.get("/api/v1/analytics/dashboard", headers=admin_headers)
        print(f"Status Code: {response.status_code}")
        assert response.status_code == 200
        dash_stats = response.json()
        assert dash_stats["total_users"] >= 1
        print(f"[SUCCESS] Precalculated dashboard counters successfully retrieved: {dash_stats}")

        # 38. Developer Queries Server Metrics Telemetry
        print("\n--- Step 38: Developer Queries Server Metrics Telemetry ---")
        dev_token = create_access_token(user_id=str(uuid.UUID("00000000-0000-7000-0000-000000000002")), role="DEVELOPER")
        dev_headers = {"Authorization": f"Bearer {dev_token}"}
        response = client.get("/api/v1/developer/system/status", headers=dev_headers)
        print(f"Status Code: {response.status_code}")
        assert response.status_code == 200
        telemetry = response.json()
        assert telemetry["cpu_usage"] == 12.5
        assert telemetry["memory_usage"] == 42.1
        print(f"[SUCCESS] Developer live telemetry diagnostics verified successfully: {telemetry}")

        print("\n=========================================================")
        print("ALL CORE MODULE 10 & 11 ENDPOINTS PASSED SUCCESSFULLY!")
        print("=========================================================")

    except AssertionError as e:
        print(f"\n[FAIL] Assertion Error occurred during verification: {e}")
    except Exception as e:
        print(f"\n[FAIL] Unexpected error occurred: {e}")
    finally:
        # 14. Cleanup - Remove all test records to keep database clean
        print(f"\n--- Step 14: Cleaning up test records ---")
        try:
            from sqlalchemy import text
            
            # Clean up notifications & logs
            if user_id:
                db.query(NotificationLog).filter(NotificationLog.user_id == user_id).delete()
            if notification_id:
                db.query(NotificationLog).filter(NotificationLog.notification_id == notification_id).delete()
                db.query(Notification).filter(Notification.id == notification_id).delete()

            if user_id:
                # Delete any audit logs and transactions referencing user's claims
                claims = db.query(RewardClaim).filter(RewardClaim.user_id == user_id).all()
                for c in claims:
                    db.query(PaymentAuditLog).filter(PaymentAuditLog.payment_id.in_(
                        db.query(PaymentTransaction.id).filter(PaymentTransaction.claim_id == c.id)
                    )).delete(synchronize_session=False)
                    db.query(PaymentTransaction).filter(PaymentTransaction.claim_id == c.id).delete()
                db.query(RewardClaim).filter(RewardClaim.user_id == user_id).delete()

            if logged_waste_id:
                db.query(WasteStatusHistory).filter(WasteStatusHistory.waste_record_id == logged_waste_id).delete()
                db.query(WasteRecord).filter(WasteRecord.id == logged_waste_id).delete()
            if created_temp_center and center_id:
                db.query(CollectionCenter).filter(CollectionCenter.id == center_id).delete()
            if api_center_id:
                db.query(CollectionCenter).filter(CollectionCenter.id == api_center_id).delete()
            if gen_ref_id:
                db.query(ReferralCode).filter(ReferralCode.id == gen_ref_id).delete()
            if team_id:
                db.query(Team).filter(Team.id == team_id).delete()
            if user_id:
                # Delete dependencies first
                db.query(PersonalLevelProgress).filter(PersonalLevelProgress.user_id == user_id).delete()
                db.query(RulesAcceptance).filter(RulesAcceptance.user_id == user_id).delete()
                db.query(UserProfile).filter(UserProfile.user_id == user_id).delete()
                db.query(User).filter(User.id == user_id).delete()
            db.query(ReferralCode).filter(ReferralCode.id == ref_id).delete()
            db.commit()
            print("[SUCCESS] Cleanup successful. Database is restored to original clean state.")
        except Exception as e:
            db.rollback()
            print(f"[FAIL] Failed to cleanup test records: {e}")
        db.close()

if __name__ == "__main__":
    run_integration_tests()
