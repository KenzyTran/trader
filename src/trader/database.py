import json
import sqlite3
import uuid
from datetime import datetime, timezone
from typing import Any

from .config import settings


def connect() -> sqlite3.Connection:
    connection = sqlite3.connect(settings.database_path)
    connection.execute("CREATE TABLE IF NOT EXISTS accounts (name TEXT PRIMARY KEY, account TEXT NOT NULL)")
    connection.execute("""CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, datetime DATETIME DEFAULT CURRENT_TIMESTAMP,
        type TEXT, message TEXT)""")
    return connection


def dynamodb_table():
    import boto3

    return boto3.resource("dynamodb", region_name=settings.aws_region).Table(settings.dynamodb_table)


def write_account(name: str, account: dict[str, Any]) -> None:
    if settings.storage_backend == "dynamodb":
        dynamodb_table().put_item(
            Item={"pk": f"ACCOUNT#{name.lower()}", "sk": "STATE", "account": json.dumps(account)}
        )
        return
    with connect() as connection:
        connection.execute(
            "INSERT INTO accounts VALUES (?, ?) ON CONFLICT(name) DO UPDATE SET account=excluded.account",
            (name.lower(), json.dumps(account)),
        )


def read_account(name: str) -> dict[str, Any] | None:
    if settings.storage_backend == "dynamodb":
        item = dynamodb_table().get_item(
            Key={"pk": f"ACCOUNT#{name.lower()}", "sk": "STATE"}, ConsistentRead=True
        ).get("Item")
        return json.loads(item["account"]) if item else None
    with connect() as connection:
        row = connection.execute("SELECT account FROM accounts WHERE name=?", (name.lower(),)).fetchone()
    return json.loads(row[0]) if row else None


def write_log(name: str, kind: str, message: str) -> None:
    if settings.storage_backend == "dynamodb":
        now = datetime.now(timezone.utc).isoformat()
        dynamodb_table().put_item(
            Item={
                "pk": f"ACCOUNT#{name.lower()}",
                "sk": f"LOG#{now}#{uuid.uuid4().hex}",
                "datetime": now,
                "type": kind,
                "message": message,
            }
        )
        return
    with connect() as connection:
        connection.execute("INSERT INTO logs(name, type, message) VALUES (?, ?, ?)", (name.lower(), kind, message))


def read_logs(name: str, limit: int = 13) -> list[tuple[str, str, str]]:
    if settings.storage_backend == "dynamodb":
        from boto3.dynamodb.conditions import Key

        items = dynamodb_table().query(
            KeyConditionExpression=Key("pk").eq(f"ACCOUNT#{name.lower()}") & Key("sk").begins_with("LOG#"),
            ScanIndexForward=False,
            Limit=limit,
        ).get("Items", [])
        return list(
            reversed([(item["datetime"], item["type"], item["message"]) for item in items])
        )
    with connect() as connection:
        rows = connection.execute(
            "SELECT datetime, type, message FROM logs WHERE name=? ORDER BY id DESC LIMIT ?",
            (name.lower(), limit),
        ).fetchall()
    return list(reversed(rows))
