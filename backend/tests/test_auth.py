def test_register_success(client):
    response = client.post(
        "/api/auth/register",
        json={"username": "testuser", "password": "password123", "role": "Trainer"},
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["user"]["username"] == "testuser"
    assert "access_token" in data
    assert "refresh_token" in data


def test_register_duplicate(client):
    client.post("/api/auth/register", json={"username": "testuser", "password": "password123"})
    response = client.post(
        "/api/auth/register", json={"username": "testuser", "password": "password123"}
    )
    assert response.status_code == 409


def test_register_short_password(client):
    response = client.post("/api/auth/register", json={"username": "testuser", "password": "123"})
    assert response.status_code == 400


def test_register_short_username(client):
    response = client.post("/api/auth/register", json={"username": "ab", "password": "password123"})
    assert response.status_code == 400


def test_login_success(client):
    client.post("/api/auth/register", json={"username": "loginuser", "password": "password123"})
    response = client.post(
        "/api/auth/login", json={"username": "loginuser", "password": "password123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.get_json()


def test_login_invalid_credentials(client):
    response = client.post("/api/auth/login", json={"username": "nobody", "password": "wrongpass"})
    assert response.status_code == 401


def test_me_authenticated(client, auth_token):
    client.post("/api/auth/register", json={"username": "testuser", "password": "password123"})
    response = client.get("/api/auth/me", headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 200


def test_me_unauthenticated(client):
    response = client.get("/api/auth/me")
    assert response.status_code == 401
