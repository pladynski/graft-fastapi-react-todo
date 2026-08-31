"""Todo list service. Public methods are the Graftcode contract."""

from __future__ import annotations

import os
import sqlite3

_DATABASE_PATH = os.getenv("DATABASE_PATH", "todos.sqlite")
_initialized = False


def _connect():
    _ensure_db()
    conn = sqlite3.connect(_DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _ensure_db() -> None:
    global _initialized
    if _initialized:
        return
    directory = os.path.dirname(os.path.abspath(_DATABASE_PATH))
    os.makedirs(directory, exist_ok=True)
    conn = sqlite3.connect(_DATABASE_PATH)
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL DEFAULT '',
                completed INTEGER NOT NULL DEFAULT 0
            )
            """
        )
        conn.commit()
    finally:
        conn.close()
    _initialized = True


def _reset_for_tests(database_path: str) -> None:
    """Re-bind the store to an isolated database. Tests only."""
    global _initialized, _DATABASE_PATH
    _DATABASE_PATH = database_path
    _initialized = False
    if os.path.exists(database_path):
        os.remove(database_path)
    _ensure_db()


def _snapshot(row) -> list[str]:
    return [
        str(row["id"]),
        row["title"],
        row["description"] or "",
        "true" if row["completed"] else "false",
    ]


def _get_row(conn, todo_id: str):
    try:
        numeric_id = int(todo_id)
    except ValueError:
        raise Exception(f"Todo with id '{todo_id}' not found") from None
    row = conn.execute("SELECT id, title, description, completed FROM todos WHERE id = ?", (numeric_id,)).fetchone()
    if row is None:
        raise Exception(f"Todo with id '{todo_id}' not found")
    return row


class TodoService:
    """Stateless todo operations. Public methods are the integration contract.

    Each todo snapshot is a plain string array:
    [id, title, description, completed] where completed is "true" or "false".
    list_todos concatenates those snapshots.
    """

    @staticmethod
    def list_todos() -> list[str]:
        conn = _connect()
        try:
            rows = conn.execute("SELECT id, title, description, completed FROM todos ORDER BY id").fetchall()
            snapshot: list[str] = []
            for row in rows:
                snapshot.extend(_snapshot(row))
            return snapshot
        finally:
            conn.close()

    @staticmethod
    def get_todo(todo_id: str) -> list[str]:
        conn = _connect()
        try:
            return _snapshot(_get_row(conn, todo_id))
        finally:
            conn.close()

    @staticmethod
    def create_todo(title: str, description: str) -> list[str]:
        conn = _connect()
        try:
            cursor = conn.execute(
                "INSERT INTO todos (title, description, completed) VALUES (?, ?, 0)",
                (title, description or ""),
            )
            conn.commit()
            row = conn.execute(
                "SELECT id, title, description, completed FROM todos WHERE id = ?",
                (cursor.lastrowid,),
            ).fetchone()
            return _snapshot(row)
        finally:
            conn.close()

    @staticmethod
    def update_todo(todo_id: str, title: str, description: str) -> list[str]:
        conn = _connect()
        try:
            _get_row(conn, todo_id)
            conn.execute(
                "UPDATE todos SET title = ?, description = ? WHERE id = ?",
                (title, description or "", int(todo_id)),
            )
            conn.commit()
            return _snapshot(_get_row(conn, todo_id))
        finally:
            conn.close()

    @staticmethod
    def toggle_todo(todo_id: str) -> list[str]:
        conn = _connect()
        try:
            row = _get_row(conn, todo_id)
            next_completed = 0 if row["completed"] else 1
            conn.execute("UPDATE todos SET completed = ? WHERE id = ?", (next_completed, int(todo_id)))
            conn.commit()
            return _snapshot(_get_row(conn, todo_id))
        finally:
            conn.close()

    @staticmethod
    def delete_todo(todo_id: str) -> bool:
        conn = _connect()
        try:
            _get_row(conn, todo_id)
            conn.execute("DELETE FROM todos WHERE id = ?", (int(todo_id),))
            conn.commit()
            return True
        finally:
            conn.close()
