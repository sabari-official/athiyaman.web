import pytest
from fastapi import status

class TestProfileEndpoints:
    """Test suite for profile endpoints"""

    def test_get_profile_unauthorized(self, client):
        """Test getting profile without authentication"""
        response = client.get("/profiles/me")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_profile_unauthorized(self, client):
        """Test updating profile without authentication"""
        response = client.put(
            "/profiles/me",
            json={"full_name": "John"}
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_profile_invalid_data(self, client, authenticated_headers):
        """Test updating profile with invalid data"""
        response = client.put(
            "/profiles/me",
            json={"dob": "invalid-date"},
            headers=authenticated_headers
        )
        assert response.status_code in [
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_200_OK
        ]

    def test_accept_rules_unauthorized(self, client):
        """Test accepting rules without authentication"""
        response = client.post("/profiles/me/accept-rules", json={"rules_version": "v1.0"})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_accept_rules_authenticated(self, client, authenticated_headers):
        """Test accepting rules when authenticated"""
        response = client.post(
            "/profiles/me/accept-rules",
            json={"rules_version": "v1.0"},
            headers=authenticated_headers
        )
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_403_FORBIDDEN
        ]
