def test_add_progress(client, auth_token):
    client.post("/api/clients/", json={
        "name": "John",
        "age": 25,
        "weight": 75,
        "program": "Fat Loss (FL)"
    }, headers={"Authorization": f"Bearer {auth_token}"})

    response = client.post("/api/progress/John", json={
        "adherence": 85
    }, headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 201
    assert response.get_json()["adherence"] == 85


def test_add_progress_invalid_adherence(client, auth_token):
    client.post("/api/clients/", json={
        "name": "John",
        "age": 25,
        "weight": 75,
        "program": "Fat Loss (FL)"
    }, headers={"Authorization": f"Bearer {auth_token}"})

    response = client.post("/api/progress/John", json={
        "adherence": 150
    }, headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 400


def test_get_progress(client, auth_token):
    client.post("/api/clients/", json={
        "name": "John",
        "age": 25,
        "weight": 75,
        "program": "Fat Loss (FL)"
    }, headers={"Authorization": f"Bearer {auth_token}"})

    client.post("/api/progress/John", json={
        "adherence": 90
    }, headers={"Authorization": f"Bearer {auth_token}"})

    response = client.get("/api/progress/John", headers={
        "Authorization": f"Bearer {auth_token}"
    })
    assert response.status_code == 200
    assert len(response.get_json()) == 1