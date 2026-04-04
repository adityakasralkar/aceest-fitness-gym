def test_get_clients_empty(client, auth_token):
    response = client.get("/api/clients/", headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 200
    assert response.get_json() == []


def test_create_client(client, auth_token):
    response = client.post(
        "/api/clients/",
        json={"name": "John", "age": 25, "weight": 75, "program": "Fat Loss (FL)"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "John"
    assert data["calories"] == 1650


def test_create_client_missing_field(client, auth_token):
    response = client.post(
        "/api/clients/", json={"name": "John"}, headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 400


def test_get_client_by_name(client, auth_token):
    client.post(
        "/api/clients/",
        json={"name": "Jane", "age": 28, "weight": 60, "program": "Beginner (BG)"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    response = client.get("/api/clients/Jane", headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 200
    assert response.get_json()["name"] == "Jane"


def test_get_client_not_found(client, auth_token):
    response = client.get("/api/clients/Nobody", headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 404


def test_delete_client(client, auth_token):
    client.post(
        "/api/clients/",
        json={"name": "DeleteMe", "age": 30, "weight": 70, "program": "Beginner (BG)"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    response = client.delete(
        "/api/clients/DeleteMe", headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200


def test_duplicate_client(client, auth_token):
    client.post(
        "/api/clients/",
        json={"name": "John", "age": 25, "weight": 75, "program": "Fat Loss (FL)"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    response = client.post(
        "/api/clients/",
        json={"name": "John", "age": 25, "weight": 75, "program": "Fat Loss (FL)"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 409


def test_unauthenticated_access(client):
    response = client.get("/api/clients/")
    assert response.status_code == 401
