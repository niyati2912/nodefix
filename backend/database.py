import sqlite3
from pathlib import Path
from datetime import datetime


BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "nodefix.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():

    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            equipment TEXT NOT NULL,
            problem TEXT NOT NULL,
            priority TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def create_ticket(
    equipment,
    problem,
    priority="HIGH"
):

    connection = get_connection()

    cursor = connection.execute(
        """
        INSERT INTO tickets
        (
            equipment,
            problem,
            priority,
            status,
            created_at
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            equipment,
            problem,
            priority,
            "OPEN",
            datetime.now().isoformat(timespec="seconds")
        )
    )

    connection.commit()

    ticket_id = cursor.lastrowid

    connection.close()

    return ticket_id