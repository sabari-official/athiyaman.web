import pytest
from fastapi import status

class TestWasteEndpoints:
    """Test suite for waste collection endpoints"""

    def test_get_waste_history_unauthorized(self, client):
        """Test waste history without authentication"""
        response = client.get("/waste")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_waste_submission_missing_fields(self, client, admin_authenticated_headers):
        """Test waste submission with missing fields"""
        response = client.post(
            "/waste",
            json={"weight_kg": 10},
            headers=admin_authenticated_headers
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_waste_submission_invalid_weight(self, client, admin_authenticated_headers):
        """Test waste submission with invalid weight"""
        response = client.post(
            "/waste",
            json={
                "user_id": "00000000-0000-7000-0000-00000000000a",
                "center_id": "00000000-0000-7000-0000-00000000030a",
                "weight_kg": -5.0,
                "image_path": "/uploads/scale_photo.png",
                "collection_date": "2026-05-28",
                "location": "Counter 1"
            },
            headers=admin_authenticated_headers
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_waste_submission_excessive_weight(self, client, admin_authenticated_headers):
        """Test waste submission exceeding maximum weight"""
        response = client.post(
            "/waste",
            json={
                "user_id": "00000000-0000-7000-0000-00000000000a",
                "center_id": "00000000-0000-7000-0000-00000000030a",
                "weight_kg": 100.0,
                "image_path": "/uploads/scale_photo.png",
                "collection_date": "2026-05-28",
                "location": "Counter 1"
            },
            headers=admin_authenticated_headers
        )
        assert response.status_code in [
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_422_UNPROCESSABLE_ENTITY
        ]

    def test_waste_pagination(self, client, authenticated_headers):
        """Test waste history pagination"""
        response = client.get(
            "/waste?page=1&limit=20",
            headers=authenticated_headers
        )
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_401_UNAUTHORIZED
        ]

    def test_waste_status_filter(self, client, authenticated_headers):
        """Test waste history with status filter"""
        response = client.get(
            "/waste?status_filter=APPROVED",
            headers=authenticated_headers
        )
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_401_UNAUTHORIZED
        ]


class TestWasteVerification:
    """Test waste verification workflows"""

    def test_reject_waste_record_unauthorized(self, client):
        """Test rejecting waste without authorization"""
        response = client.post(
            "/admin/waste/00000000-0000-0000-0000-000000000000/reject",
            json={"comments": "Invalid waste"}
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_reject_waste_nonexistent(self, client, authenticated_headers):
        """Test rejecting nonexistent waste record"""
        response = client.post(
            "/admin/waste/00000000-0000-0000-0000-000000000000/reject",
            json={"comments": "Invalid waste"},
            headers=authenticated_headers
        )
        assert response.status_code in [
            status.HTTP_404_NOT_FOUND,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_403_FORBIDDEN
        ]
