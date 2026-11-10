from app.db import add_check, get_check_counts, init_db


def test_database_persistence(tmp_path):
    db_path = tmp_path / "checks.db"

    init_db(db_path)

    add_check(db_path, "payment-api", True)
    add_check(db_path, "payment-api", True)
    add_check(db_path, "payment-api", False)

    successful, total = get_check_counts(db_path, "payment-api")

    assert successful == 2
    assert total == 3

    assert db_path.exists()


def test_service_isolation(tmp_path):
    db_path = tmp_path / "checks.db"

    init_db(db_path)

    add_check(db_path, "payment-api", True)
    add_check(db_path, "order-api", False)

    assert get_check_counts(db_path, "payment-api") == (1, 1)
    assert get_check_counts(db_path, "order-api") == (0, 1)


def test_unknown_service(tmp_path):
    db_path = tmp_path / "checks.db"

    init_db(db_path)

    assert get_check_counts(db_path, "unknown") == (0, 0)
