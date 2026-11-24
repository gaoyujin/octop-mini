from fastapi.testclient import TestClient

from mini.api.main import app


def test_health_ok() -> None:
    with TestClient(app) as client:
        response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is True
    assert body["db_bound"] is True
    assert body["schema_version"] == 1
    assert "mini_home" in body