def test_health_returns_service_metadata(client, monkeypatch):
    monkeypatch.setenv("APP_VERSION", "test-version")
    monkeypatch.setenv("DEPLOYMENT_VARIANT", "test-variant")

    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {
        "status": "ok",
        "service": "aceest-fitness-gym",
        "environment": "testing",
        "version": "test-version",
        "deployment_variant": "test-variant",
    }
