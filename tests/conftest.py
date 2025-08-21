import pytest
from rest_framework.test import APIClient

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def authenticated_api_client(api_client):
    api_client.force_authenticate(user=None)
    return api_client

@pytest.fixture
def registration_user(api_client):
    return {"username": "testuser", "password": "testpassword"}

