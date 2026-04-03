import pytest
from app import db
from app.models.database import User


def test_register_success(client):
    response = client.post("/api/auth/register", json={
        "username": "testuser",
        "password": "testpass123",
        "role": "Trainer"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["user"]["username"] == "testuser"
    assert data["user"]["role"] == "Trainer"


def test_register_missing_data(client):
    response = client.post("/api/auth/register", json={})
    assert response.status_code == 400
    assert "No data provided" in response.get_json()["error"]


def test_register_missing_fields(client):
    response = client.post("/api/auth/register", json={"username": "test"})
    assert response.status_code == 400
    assert "password is required" in response.get_json()["error"]


def test_register_short_password(client):
    response = client.post("/api/auth/register", json={
        "username": "testuser",
        "password": "123"
    })
    assert response.status_code == 400
    assert "Password must be at least 6 characters" in response.get_json()["error"]


def test_register_short_username(client):
    response = client.post("/api/auth/register", json={
        "username": "ab",
        "password": "testpass123"
    })
    assert response.status_code == 400
    assert "Username must be at least 3 characters" in response.get_json()["error"]


def test_register_duplicate_username(client):
    # First registration
    client.post("/api/auth/register", json={
        "username": "duplicate",
        "password": "testpass123"
    })
    # Second registration with same username
    response = client.post("/api/auth/register", json={
        "username": "duplicate",
        "password": "testpass123"
    })
    assert response.status_code == 409
    assert "Username already exists" in response.get_json()["error"]


def test_login_success(client):
    # Register first
    client.post("/api/auth/register", json={
        "username": "loginuser",
        "password": "loginpass123"
    })
    # Login
    response = client.post("/api/auth/login", json={
        "username": "loginuser",
        "password": "loginpass123"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["user"]["username"] == "loginuser"


def test_login_invalid_credentials(client):
    response = client.post("/api/auth/login", json={
        "username": "nonexistent",
        "password": "wrongpass"
    })
    assert response.status_code == 401
    assert "Invalid credentials" in response.get_json()["error"]


def test_login_missing_data(client):
    response = client.post("/api/auth/login", json={})
    assert response.status_code == 400
    assert "No data provided" in response.get_json()["error"]


def test_refresh_token(client):
    # Register and login to get tokens
    client.post("/api/auth/register", json={
        "username": "refreshuser",
        "password": "refreshpass123"
    })
    login_response = client.post("/api/auth/login", json={
        "username": "refreshuser",
        "password": "refreshpass123"
    })
    refresh_token = login_response.get_json()["refresh_token"]

    # Refresh
    response = client.post("/api/auth/refresh",
                          headers={"Authorization": f"Bearer {refresh_token}"})
    assert response.status_code == 200
    data = response.get_json()
    assert "access_token" in data


def test_me_endpoint(client):
    # Register and login to get access token
    client.post("/api/auth/register", json={
        "username": "meuser",
        "password": "mepass123"
    })
    login_response = client.post("/api/auth/login", json={
        "username": "meuser",
        "password": "mepass123"
    })
    access_token = login_response.get_json()["access_token"]

    # Get me
    response = client.get("/api/auth/me",
                         headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["username"] == "meuser"


def test_me_unauthorized(client):
    response = client.get("/api/auth/me")
    assert response.status_code == 401


def test_logout(client):
    # Register and login to get access token
    client.post("/api/auth/register", json={
        "username": "logoutuser",
        "password": "logoutpass123"
    })
    login_response = client.post("/api/auth/login", json={
        "username": "logoutuser",
        "password": "logoutpass123"
    })
    access_token = login_response.get_json()["access_token"]

    # Logout
    response = client.post("/api/auth/logout",
                          headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert "Logged out successfully" in response.get_json()["message"]