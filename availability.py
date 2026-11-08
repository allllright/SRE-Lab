
def calculate_availability(
    successful_checks: int,
    total_checks: int
) -> float:

    if total_checks <= 0:
        raise ValueError("Total checks must be greater than zero")

    if successful_checks < 0:
        raise ValueError("Successful checks must not be negative")

    if successful_checks > total_checks:
        raise ValueError("Successful checks must not exceed total checks")

    return 100 * successful_checks / total_checks
