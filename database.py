"""SQLite helpers for the SVEAR Compliance Agent."""

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple

from config import DATABASE_PATH


def get_connection(db_path: Path = DATABASE_PATH) -> sqlite3.Connection:
    """Open a SQLite connection."""
    return sqlite3.connect(db_path)


def init_db() -> None:
    """Create the document log table when it does not already exist."""
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS document_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                document_type TEXT NOT NULL,
                date_generated TEXT NOT NULL,
                meeting_date TEXT NOT NULL,
                file_path TEXT NOT NULL,
                email_status TEXT NOT NULL
            )
            """
        )
        conn.commit()


def add_document_log(
    document_type: str,
    meeting_date: str,
    file_path: str,
    email_status: str = "Not sent",
) -> int:
    """Insert a document generation record and return the inserted row id."""
    init_db()
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO document_log
            (document_type, date_generated, meeting_date, file_path, email_status)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                document_type,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                meeting_date,
                file_path,
                email_status,
            ),
        )
        conn.commit()
        return int(cursor.lastrowid)


def update_email_status(log_id: int, email_status: str) -> None:
    """Update email status for one log record."""
    init_db()
    with get_connection() as conn:
        conn.execute(
            "UPDATE document_log SET email_status = ? WHERE id = ?",
            (email_status, log_id),
        )
        conn.commit()


def fetch_document_logs(limit: Optional[int] = 50) -> List[Tuple]:
    """Fetch recent document log rows for display in Streamlit."""
    init_db()
    query = (
        "SELECT id, document_type, date_generated, meeting_date, file_path, email_status "
        "FROM document_log ORDER BY id DESC"
    )
    params = ()
    if limit:
        query += " LIMIT ?"
        params = (limit,)

    with get_connection() as conn:
        return conn.execute(query, params).fetchall()
