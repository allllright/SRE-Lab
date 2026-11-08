import pytest

from app.services.availability import calculate_availability

@pytest.mark.parametrize(
    "successful_checks, total_checks",
    [
        (0, 0),
        (-5, 100),
        (120, 100),
    ],
)
def test_invalid_availability(successful_checks, total_checks):
    with pytest.raises(ValueError):
        calculate_availability(successful_checks, total_checks)

def test_availability_normal_case():
    result = calculate_availability(995, 1000)

    assert result == 99.5