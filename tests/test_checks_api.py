import importlib

import pytest
from fastapi.testclient import TestClient

main_module = importlib.import_module("app.main")


@pytest.fixture
def client(tmp_path, monkeypatch):
    # Use an isolated database for each test.
    test_db = tmp_path / "test_checks.db"

    monkeypatch.setattr(main_module, "DB_PATH", test_db)

    with TestClient(main_module.app) as test_client:
        yield test_client


def test_create_health_check(client):
    response = client.post(
        "/checks",
        json={
            "service": "payment-api",
            "success": True,
        },
    )

    assert response.status_code == 201
    assert response.json()["service"] == "payment-api"


def test_availability_from_database(client):
    client.post(
        "/checks",
        json={"service": "payment-api", "success": True},
    )

    client.post(
        "/checks",
        json={"service": "payment-api", "success": True},
    )

    client.post(
        "/checks",
        json={"service": "payment-api", "success": False},
    )

    response = client.get("/services/payment-api/availability")

    assert response.status_code == 200

    assert response.json() == {
        "service": "payment-api",
        "successful_checks": 2,
        "total_checks": 3,
        "availability": 200 / 3,
    }


def test_unknown_service(client):
    response = client.get("/services/unknown/availability")

    assert response.status_code == 404


def test_invalid_service_name(client):
    response = client.post(
        "/checks",
        json={"service": "   ", "success": True},
    )

    assert response.status_code == 422
