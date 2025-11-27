# src/memory/memory_store.py

import sqlite3
from pathlib import Path
from datetime import datetime

class MemoryStore:
    """
    Simple wrapper around SQLite to store key-value memories.

    This is our LONG-TERM MEMORY layer.
    """

    def __init__(self, db_path: str = "data/memory.db"):
        self.db_path = db_path
        self._ensure_db()

    def _get_connection(self):
        """
        Create a new SQLite connection.
        """
        return sqlite3.connect(self.db_path)

    def _ensure_db(self):
        """
        Create the table if it does not exist.
        """

        # Make sure folder exists
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)

        conn = self._get_connection()
        cursor = conn.cursor()

        # Basic table: id, key, value, created_at
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT NOT NULL UNIQUE,
                value TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )

        conn.commit()
        conn.close()

    def set_memory(self, key: str, value: str):
        """
        Insert or update a memory (key, value).
        If key already exists, update its value.
        """

        conn = self._get_connection()
        cursor = conn.cursor()

        now = datetime.utcnow().isoformat()

        # Use INSERT OR REPLACE to avoid duplicate key errors
        cursor.execute(
            """
            INSERT OR REPLACE INTO memories (id, key, value, created_at)
            VALUES (
                COALESCE((SELECT id FROM memories WHERE key = ?), NULL),
                ?, ?, ?
            )
            """,
            (key, key, value, now),
        )

        conn.commit()
        conn.close()

    def get_memory(self, key: str) -> str | None:
        """
        Returns the value for a given key, or None if not found.
        """

        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT value FROM memories WHERE key = ?",
            (key,),
        )

        row = cursor.fetchone()
        conn.close()

        if row is None:
            return None
        return row[0]

    def get_all_memories(self) -> list[tuple[str, str]]:
        """
        Returns a list of (key, value) pairs for all memories.
        """

        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT key, value FROM memories")
        rows = cursor.fetchall()
        conn.close()

        return rows
