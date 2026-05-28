import pytest
from fastapi import status

class TestLevelEndpoints:
    """Test suite for level progression endpoints"""

    def test_get_team_progression_unauthorized(self, client):
        """Test getting team progression without authentication"""
        response = client.get("/levels/team")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_personal_progression_unauthorized(self, client):
        """Test getting personal progression without authentication"""
        response = client.get("/levels/personal")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_team_progression_no_team(self, client, authenticated_headers):
        """Test getting team progression when user has no team"""
        response = client.get(
            "/levels/team",
            headers=authenticated_headers
        )
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_404_NOT_FOUND,
            status.HTTP_400_BAD_REQUEST
        ]

    def test_get_personal_progression_format(self, client, authenticated_headers):
        """Test personal progression response format"""
        response = client.get(
            "/levels/personal",
            headers=authenticated_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        # Should return list of levels
        if isinstance(data, list):
            for level in data:
                assert "level_number" in level or "level_id" in level
