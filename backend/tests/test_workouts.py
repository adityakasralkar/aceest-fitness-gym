def test_add_workout(client, auth_token):
    client.post(
        "/api/clients/",
        json={"name": "John", "age": 25, "weight": 75, "program": "Fat Loss (FL)"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    response = client.post(
        "/api/workouts/John",
        json={"workout_type": "Strength", "duration_min": 60},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 201
    assert response.get_json()["workout_type"] == "Strength"


def test_add_workout_invalid_type(client, auth_token):
    client.post(
        "/api/clients/",
        json={"name": "John", "age": 25, "weight": 75, "program": "Fat Loss (FL)"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    response = client.post(
        "/api/workouts/John",
        json={"workout_type": "InvalidType", "duration_min": 60},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 400


def test_get_workouts(client, auth_token):
    client.post(
        "/api/clients/",
        json={"name": "John", "age": 25, "weight": 75, "program": "Fat Loss (FL)"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    client.post(
        "/api/workouts/John",
        json={"workout_type": "Cardio", "duration_min": 45},
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    response = client.get("/api/workouts/John", headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 200
    assert len(response.get_json()) == 1


def test_workout_client_not_found(client, auth_token):
    response = client.post(
        "/api/workouts/Nobody",
        json={"workout_type": "Cardio", "duration_min": 45},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 404
