def calculate_availability(
    successful_checks: int,
    total_checks: int,
) -> float:

    if total_checks <= 0:
        raise ValueError("Total checks must be greater than zero")

    if successful_checks < 0:
        raise ValueError("Successful checks cannot be negative")

    if successful_checks > total_checks:
        raise ValueError("Successful checks cannot exceed total checks")

    return 100 * successful_checks / total_checks
