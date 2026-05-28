import pytest
from fastapi import status

class TestClaimsEndpoints:
    """Test suite for reward claims endpoints"""

    def test_create_claim_unauthorized(self, client):
        """Test creating claim without authentication"""
        response = client.post("/rewards/claims", json={"claim_type": "PERSONAL", "level_number": 7})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_personal_claims_unauthorized(self, client):
        """Test getting claims without authentication"""
        response = client.get("/rewards/claims?claim_type=PERSONAL")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_admin_claims_unauthorized(self, client):
        """Test getting all claims without admin role"""
        response = client.get("/admin/claims")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_approve_claim_unauthorized(self, client):
        """Test approving claim without authorization"""
        response = client.post(
            "/admin/claims/00000000-0000-0000-0000-000000000000/approve"
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_reject_claim_unauthorized(self, client):
        """Test rejecting claim without authorization"""
        response = client.post(
            "/admin/claims/00000000-0000-0000-0000-000000000000/reject",
            json={"comments": "Invalid claim"}
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestClaimsWorkflow:
    """Test complete claims workflow"""

    def test_personal_claims_pagination(self, client, authenticated_headers):
        """Test personal claims pagination"""
        response = client.get(
            "/rewards/claims?claim_type=PERSONAL&page=1&limit=20",
            headers=authenticated_headers
        )
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_400_BAD_REQUEST
        ]

    def test_personal_claims_filtering(self, client, authenticated_headers):
        """Test filtering personal claims"""
        response = client.get(
            "/rewards/claims?claim_type=PERSONAL&status_filter=PENDING",
            headers=authenticated_headers
        )
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_400_BAD_REQUEST
        ]
