import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_availability_success():
    response = client.get(
        "/availability",
        params={"successful": 995, "total": 1000},
    )

    assert response.status_code == 200
    assert response.json() == {"availability": 99.5}


@pytest.mark.parametrize(
    "successful,total",
    [
        (0, 0),
        (-5, 100),
        (120, 100),
    ],
)
def test_availability_invalid_input(successful, total):
    response = client.get(
        "/availability",
        params={"successful": successful, "total": total},
    )

    assert response.status_code == 400


def test_availability_missing_parameter():
    response = client.get(
        "/availability",
        params={"successful": 995},
    )

    assert response.status_code == 422


def test_availability_invalid_parameter_type():
    response = client.get(
        "/availability",
        params={"successful": "abc", "total": 1000},
    )

    assert response.status_code == 422
