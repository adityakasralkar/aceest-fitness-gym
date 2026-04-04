def test_get_membership(client, auth_token):
    client.post("/api/clients/", json={
        "name": "John",
        "age": 25,
        "weight": 75,
        "program": "Fat Loss (FL)"
    }, headers={"Authorization": f"Bearer {auth_token}"})

    response = client.get("/api/membership/John", headers={
        "Authorization": f"Bearer {auth_token}"
    })
    assert response.status_code == 200
    assert response.get_json()["membership_status"] == "Active"


def test_renew_membership(client, auth_token):
    client.post("/api/clients/", json={
        "name": "John",
        "age": 25,
        "weight": 75,
        "program": "Fat Loss (FL)"
    }, headers={"Authorization": f"Bearer {auth_token}"})

    response = client.post("/api/membership/John/renew", json={
        "months": 3
    }, headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 200
    assert "membership_end" in response.get_json()


def test_cancel_membership(client, auth_token):
    client.post("/api/clients/", json={
        "name": "John",
        "age": 25,
        "weight": 75,
        "program": "Fat Loss (FL)"
    }, headers={"Authorization": f"Bearer {auth_token}"})

    response = client.post("/api/membership/John/cancel", headers={
        "Authorization": f"Bearer {auth_token}"
    })
    assert response.status_code == 200
    assert response.get_json()["membership_status"] == "Cancelled"