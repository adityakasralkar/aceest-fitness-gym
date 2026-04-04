def test_add_metric(client, auth_token):
    client.post(
        "/api/clients/",
        json={"name": "John", "age": 25, "weight": 75, "program": "Fat Loss (FL)"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    response = client.post(
        "/api/metrics/John",
        json={"weight": 74.5, "waist": 85.0, "bodyfat": 18.5},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 201


def test_add_metric_invalid_bodyfat(client, auth_token):
    client.post(
        "/api/clients/",
        json={"name": "John", "age": 25, "weight": 75, "program": "Fat Loss (FL)"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    response = client.post(
        "/api/metrics/John",
        json={"bodyfat": 150},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 400


def test_get_metrics(client, auth_token):
    client.post(
        "/api/clients/",
        json={"name": "John", "age": 25, "weight": 75, "program": "Fat Loss (FL)"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    client.post(
        "/api/metrics/John",
        json={"weight": 74.5},
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    response = client.get("/api/metrics/John", headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 200
    assert len(response.get_json()) == 1
