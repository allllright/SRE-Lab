import sqlite3
from contextlib import closing
from pathlib import Path


def init_db(db_path: Path) -> None:
    """Create the database table if it does not exist."""
    db_path.parent.mkdir(parents=True, exist_ok=True)

    with closing(sqlite3.connect(db_path)) as conn, conn:
        conn.execute("""
                CREATE TABLE IF NOT EXISTS health_checks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    service TEXT NOT NULL
                        CHECK (length(trim(service)) > 0),
                    success INTEGER NOT NULL
                        CHECK (success IN (0, 1)),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)


def add_check(db_path: Path, service: str, success: bool) -> None:
    """Save one health check result."""
    with closing(sqlite3.connect(db_path)) as conn, conn:
        conn.execute(
            """
                INSERT INTO health_checks (service, success)
                VALUES (?, ?)
                """,
            (service, int(success)),
        )


def get_check_counts(db_path: Path, service: str) -> tuple[int, int]:
    """Return successful checks and total checks for a service."""
    with closing(sqlite3.connect(db_path)) as conn:
        cursor = conn.execute(
            """
            SELECT
                COALESCE(SUM(success), 0),
                COUNT(*)
            FROM health_checks
            WHERE service = ?
            """,
            (service,),
        )

        successful, total = cursor.fetchone()

    return int(successful), int(total)
