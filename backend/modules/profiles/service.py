from sqlalchemy.orm import Session
from uuid import UUID
import datetime

from backend.database.models import UserProfile, RulesAcceptance, User
from backend.modules.profiles.repository import UserProfileRepository
from backend.modules.profiles.schema import ProfileUpdateRequest
from backend.utils.security import aadhaar_security, bank_security
from backend.utils.verhoeff import validate_aadhaar

class ProfileService:
    """
    ProfileService enforces data masking, AES-256 symmetric encryption,
    uniqueness validations on Aadhaar numbers, dynamic completeness indicators,
    and platform click-wrap acceptances.
    """
    def __init__(self, db: Session):
        self.db = db
        self.profile_repo = UserProfileRepository(db)

    def get_profile(self, user_id: UUID) -> UserProfile:
        """Fetch citizen profile record. Creates a blank profile if missing."""
        profile = self.profile_repo.get_by_user_id(user_id)
        if not profile:
            profile = UserProfile(
                user_id=user_id,
                full_name="Citizen",
                profile_completion=0
            )
            self.db.add(profile)
            self.db.commit()
            self.db.refresh(profile)
        return profile

    def update_profile(self, user_id: UUID, payload: ProfileUpdateRequest) -> UserProfile:
        """
        Applies citizen profile updates in an atomic database transaction.
        Enforces:
        - Cryptographic hashing to prevent duplicate Aadhaar submissions.
        - AES-256 symmetric encryption on banking routing Details.
        - Masked exposure layers.
        - Dynamic completeness metrics calculation.
        """
        profile = self.get_profile(user_id)
        update_dict = payload.model_dump(exclude_unset=True)

        # 1. Enforce unique Aadhaar constraints
        if "aadhaar" in update_dict and update_dict["aadhaar"]:
            raw_aadhaar = update_dict.pop("aadhaar")
            if not validate_aadhaar(raw_aadhaar):
                raise ValueError("INVALID_AADHAAR")
                
            aadhaar_hash = aadhaar_security.generate_sha256_hash(raw_aadhaar)
            
            # Check duplicate registry
            existing_profile = self.profile_repo.get_by_aadhaar_hash(aadhaar_hash)
            if existing_profile and existing_profile.user_id != user_id:
                raise ValueError("AADHAAR_ALREADY_USED")
                
            masked = "XXXX-XXXX-" + raw_aadhaar[-4:] if len(raw_aadhaar) >= 4 else "XXXX-XXXX-XXXX"
            profile.masked_aadhaar = masked
            profile.aadhaar_hash = aadhaar_hash
            profile.aadhaar_verified = True  # Automatically verified for Phase 1 demo

        # 2. Enforce AES bank account encryption and masking
        if "account_number" in update_dict and update_dict["account_number"]:
            raw_acc = update_dict.pop("account_number")
            profile.account_number_encrypted = bank_security.encrypt_data(raw_acc)
            
            # Display masking: XXXXXX + last 4 digits
            masked = "XXXXXX"
            if len(raw_acc) >= 4:
                masked = "XXXXXX" + raw_acc[-4:]
            profile.account_number_masked = masked
            profile.bank_verified = True  # Verified for Phase 1 demo

        # 3. Apply other properties dynamically
        for field, value in update_dict.items():
            if hasattr(profile, field):
                setattr(profile, field, value)

        # 4. Calculate dynamic completeness metrics
        completion = self._calculate_completion(profile)
        profile.profile_completion = completion

        self.db.commit()
        self.db.refresh(profile)
        return profile

    def accept_platform_rules(self, user_id: UUID, version: str, ip_address: str) -> bool:
        """
        Accepts the platform click-wrap legal rules.
        Strictly blocks acceptance actions until profile completion matches exactly 100%.
        """
        profile = self.get_profile(user_id)
        if profile.profile_completion != 100:
            raise ValueError("PROFILE_INCOMPLETE_RULES")

        # Create acceptance log
        acceptance = RulesAcceptance(
            user_id=user_id,
            rules_version=version,
            ip_address=ip_address
        )
        self.db.add(acceptance)
        
        # Mark user as verified
        user = self.db.query(User).filter(User.id == user_id).first()
        if user:
            user.is_verified = True
            
        self.db.commit()
        return True

    def _calculate_completion(self, profile: UserProfile) -> int:
        """
        Granular formula to calculate profile completion.
        Allocates points for each completed category out of 100 max:
        - Basic Bio (Full Name, Gender, DOB, Email): 5 pts each (Total 20)
        - Contact Address (State, District, Pincode, Door No, Post Office): 4 pts each (Total 20)
        - Aadhaar Security (Encrypted Details & Hash): 20 pts (Total 20)
        - Bank Verification (Name, Masked Account, IFSC): 5 + 10 + 5 pts (Total 20)
        - Nominee Setup (Name, Relationship, Phone): 6 + 7 + 7 pts (Total 20)
        """
        score = 0
        
        # 1. Basic Bio
        if profile.full_name and profile.full_name != "Citizen": score += 4
        if profile.gender: score += 4
        if profile.dob: score += 4
        if profile.email: score += 4
        if profile.profession: score += 4
        
        # 2. Contact Address
        if profile.state: score += 4
        if profile.district: score += 4
        if profile.pincode: score += 4
        if profile.door_no: score += 4
        if profile.post_office: score += 4
        
        # 3. Aadhaar Verification
        if profile.masked_aadhaar and profile.aadhaar_hash: score += 20
        
        # 4. Bank Details
        if profile.bank_name: score += 5
        if profile.account_number_encrypted: score += 10
        if profile.ifsc_code: score += 5
        
        # 5. Nominee Setup
        if profile.nominee_name: score += 6
        if profile.nominee_relationship: score += 7
        if profile.nominee_phone: score += 7
        
        return score
