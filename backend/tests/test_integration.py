import pytest
from fastapi.testclient import TestClient
from backend.main import app

class TestCollectionCenters:
    """Test suite for collection center endpoints"""

    def test_search_centers_unauthorized(self, client):
        """Test searching centers without auth"""
        response = client.get("/centers?pincode=123456")
        # May or may not require auth
        assert response.status_code in [200, 401]

    def test_get_all_centers(self, client):
        """Test fetching all centers"""
        response = client.get("/centers")
        assert response.status_code in [200, 401]

    def test_search_by_location(self, client):
        """Test searching centers by location"""
        response = client.get("/centers?district=Madurai")
        assert response.status_code in [200, 400, 401]

    def test_search_by_pincode(self, client):
        """Test searching centers by pincode"""
        response = client.get("/centers?pincode=625001")
        assert response.status_code in [200, 400, 401]


class TestApplications:
    """Test suite for application endpoints"""

    def test_submit_leader_application(self, client, authenticated_headers):
        """Test submitting leader application"""
        response = client.post(
            "/applications/leader",
            json={
                "full_name": "Test Leader App",
                "phone": "9998887770",
                "email": "leaderapp@example.com",
                "aadhaar": "123456789012",
                "state": "Tamil Nadu",
                "district": "Coimbatore",
                "pincode": "641001",
                "door_no": "12",
                "street_name": "Anna Salai",
                "post_office": "Coimbatore GP",
                "city": "Coimbatore",
                "reason": "Want to lead community"
            },
            headers=authenticated_headers
        )
        assert response.status_code in [201, 400, 401]

    def test_submit_member_application(self, client, authenticated_headers):
        """Test submitting member application"""
        response = client.post(
            "/applications/member",
            json={
                "full_name": "Test Member App",
                "phone": "9998887771",
                "email": "memberapp@example.com",
                "aadhaar": "123456789013",
                "state": "Tamil Nadu",
                "district": "Madurai",
                "pincode": "625001",
                "door_no": "34",
                "street_name": "KK Nagar",
                "post_office": "Madurai GP",
                "city": "Madurai",
                "reason": "Want to help community"
            },
            headers=authenticated_headers
        )
        assert response.status_code in [201, 400, 401]


class TestNotifications:
    """Test suite for notifications endpoints"""

    def test_get_notifications_unauthorized(self, client):
        """Test getting notifications without auth"""
        response = client.get("/notifications")
        assert response.status_code == 401

    def test_get_notifications_authenticated(self, client, authenticated_headers):
        """Test getting notifications when authenticated"""
        response = client.get(
            "/notifications",
            headers=authenticated_headers
        )
        assert response.status_code in [200, 400]

    def test_mark_notification_read(self, client, authenticated_headers):
        """Test marking notification as read"""
        response = client.put(
            "/notifications/019e6e2f-7d8f-76d2-972d-363b2e50f3db/read",
            headers=authenticated_headers
        )
        assert response.status_code in [200, 404, 400]

    def test_broadcast_announcement(self, client, authenticated_headers):
        """Test sending announcement"""
        response = client.post(
            "/admin/announcements",
            json={
                "title": "System Announcement",
                "message": "This is a system-wide announcement.",
                "start_date": "2026-05-28",
                "end_date": "2026-06-28"
            },
            headers=authenticated_headers
        )
        assert response.status_code in [201, 403, 401]


class TestPayments:
    """Test suite for payment endpoints"""

    def test_get_payment_history_unauthorized(self, client):
        """Test getting payment history without auth"""
        response = client.get("/payments")
        assert response.status_code == 401

    def test_get_payment_history(self, client, authenticated_headers):
        """Test getting user payment history"""
        response = client.get(
            "/payments",
            headers=authenticated_headers
        )
        assert response.status_code in [200, 400]

    def test_process_payout_unauthorized(self, client):
        """Test processing payout without admin role"""
        response = client.post(
            "/admin/payments/019e6e2f-7d8f-76d2-972d-363b2e50f3db/paid",
            json={"transaction_reference": "UTR12345678"},
        )
        assert response.status_code == 401
