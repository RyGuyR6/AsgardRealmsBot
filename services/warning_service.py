from pathlib import Path
import sqlite3

DB = Path("data/moderation.db")


def connection():
    DB.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB)


def initialize():
    with connection() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS warnings(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guild_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            moderator_id INTEGER NOT NULL,
            reason TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)


def add_warning(guild_id: int, user_id: int, moderator_id: int, reason: str):
    with connection() as conn:
        conn.execute(
            """
            INSERT INTO warnings
            (guild_id,user_id,moderator_id,reason)
            VALUES(?,?,?,?)
            """,
            (guild_id, user_id, moderator_id, reason),
        )


def get_warnings(user_id: int):
    with connection() as conn:
        return conn.execute(
            """
            SELECT id, moderator_id, reason, created_at
            FROM warnings
            WHERE user_id=?
            ORDER BY created_at DESC
            """,
            (user_id,),
        ).fetchall()


def clear_warnings(user_id: int):
    with connection() as conn:
        conn.execute(
            "DELETE FROM warnings WHERE user_id=?",
            (user_id,),
        )


def warning_count(user_id: int):
    with connection() as conn:
        return conn.execute(
            "SELECT COUNT(*) FROM warnings WHERE user_id=?",
            (user_id,),
        ).fetchone()[0]
