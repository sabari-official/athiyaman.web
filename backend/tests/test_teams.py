import pytest
from fastapi import status

class TestTeamEndpoints:
    """Test suite for team management endpoints"""

    def test_create_team_unauthorized(self, client, test_team_data):
        """Test creating team without authentication"""
        response = client.post("/teams/", json=test_team_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_my_team_unauthorized(self, client):
        """Test getting team without authentication"""
        response = client.get("/teams/my-team")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_team_roster_unauthorized(self, client):
        """Test getting team roster without authentication"""
        response = client.get("/teams/my-team/roster")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_team_missing_fields(self, client, authenticated_headers):
        """Test creating team with missing fields"""
        response = client.post(
            "/teams/",
            json={"team_name": "Team"},
            headers=authenticated_headers
        )
        assert response.status_code in [
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            status.HTTP_400_BAD_REQUEST
        ]

    def test_get_team_roster_pagination(self, client, authenticated_headers):
        """Test team roster pagination"""
        response = client.get(
            "/teams/my-team/roster?page=1&limit=50",
            headers=authenticated_headers
        )
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_404_NOT_FOUND,
            status.HTTP_400_BAD_REQUEST
        ]
