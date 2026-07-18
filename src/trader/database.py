import json
import sqlite3
from typing import Any

from .config import settings


def connect() -> sqlite3.Connection:
    connection = sqlite3.connect(settings.database_path)
    connection.execute("CREATE TABLE IF NOT EXISTS accounts (name TEXT PRIMARY KEY, account TEXT NOT NULL)")
    connection.execute("""CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, datetime DATETIME DEFAULT CURRENT_TIMESTAMP,
        type TEXT, message TEXT)""")
    return connection


def write_account(name: str, account: dict[str, Any]) -> None:
    with connect() as connection:
        connection.execute(
            "INSERT INTO accounts VALUES (?, ?) ON CONFLICT(name) DO UPDATE SET account=excluded.account",
            (name.lower(), json.dumps(account)),
        )


def read_account(name: str) -> dict[str, Any] | None:
    with connect() as connection:
        row = connection.execute("SELECT account FROM accounts WHERE name=?", (name.lower(),)).fetchone()
    return json.loads(row[0]) if row else None


def write_log(name: str, kind: str, message: str) -> None:
    with connect() as connection:
        connection.execute("INSERT INTO logs(name, type, message) VALUES (?, ?, ?)", (name.lower(), kind, message))


def read_logs(name: str, limit: int = 13) -> list[tuple[str, str, str]]:
    with connect() as connection:
        rows = connection.execute(
            "SELECT datetime, type, message FROM logs WHERE name=? ORDER BY id DESC LIMIT ?",
            (name.lower(), limit),
        ).fetchall()
    return list(reversed(rows))
