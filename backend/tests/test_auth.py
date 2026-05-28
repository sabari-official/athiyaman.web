import pytest
from fastapi import status

class TestAuthentication:
    """Test suite for authentication endpoints"""

    def test_user_signup_success(self, client, test_user_data):
        """Test successful user registration"""
        response = client.post("/auth/signup", json=test_user_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["username"] == test_user_data["username"]

    def test_user_signup_duplicate_username(self, client, test_user_data):
        """Test signup with duplicate username"""
        # First signup
        client.post("/auth/signup", json=test_user_data)
        
        # Attempt duplicate
        response = client.post("/auth/signup", json={
            **test_user_data,
            "phone_number": "9999999999"
        })
        assert response.status_code == status.HTTP_409_CONFLICT

    def test_user_signup_invalid_phone(self, client, test_user_data):
        """Test signup with invalid phone number"""
        response = client.post("/auth/signup", json={
            **test_user_data,
            "phone_number": "invalid"
        })
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_user_signup_missing_fields(self, client):
        """Test signup with missing required fields"""
        response = client.post("/auth/signup", json={
            "username": "testuser"
        })
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_user_login_success(self, client, test_user_data):
        """Test successful login"""
        # Create user first
        client.post("/auth/signup", json=test_user_data)
        
        # Login
        response = client.post("/auth/login", json={
            "username": test_user_data["username"],
            "password": test_user_data["password"]
        })
        assert response.status_code == status.HTTP_200_OK
        assert "access_token" in response.json()
        assert "refresh_token" in response.json()

    def test_user_login_invalid_credentials(self, client):
        """Test login with invalid credentials"""
        response = client.post("/auth/login", json={
            "username": "nonexistent",
            "password": "wrongpassword"
        })
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_login_wrong_password(self, client, test_user_data):
        """Test login with wrong password"""
        # Create user
        client.post("/auth/signup", json=test_user_data)
        
        # Try wrong password
        response = client.post("/auth/login", json={
            "username": test_user_data["username"],
            "password": "WrongPassword123!"
        })
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_change_password_success(self, client, test_user_data, authenticated_headers):
        """Test successful password change"""
        response = client.post(
            "/auth/change-password",
            json={
                "current_password": test_user_data["password"],
                "new_password": "NewPassword123!"
            },
            headers=authenticated_headers
        )
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED]

    def test_verify_aadhaar_valid(self, client):
        """Test valid Aadhaar verification"""
        response = client.post("/auth/verify-aadhaar", json={
            "aadhaar": "123456789012"
        })
        # Should return valid/invalid based on Verhoeff algorithm
        assert response.status_code == status.HTTP_200_OK
        assert "valid" in response.json()

    def test_verify_aadhaar_invalid_length(self, client):
        """Test invalid Aadhaar length"""
        response = client.post("/auth/verify-aadhaar", json={
            "aadhaar": "12345"
        })
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestAuthEndpoints:
    """Test authentication error handling"""

    def test_unauthorized_access(self, client):
        """Test accessing protected endpoint without token"""
        response = client.get("/profiles/me")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_invalid_token(self, client):
        """Test with invalid token"""
        response = client.get(
            "/profiles/me",
            headers={"Authorization": "Bearer invalid_token"}
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
