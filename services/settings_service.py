from pathlib import Path
import sqlite3

DB = Path("data/settings.db")


def connect():
    DB.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB)


def initialize():
    with connect() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS guild_settings (
            guild_id INTEGER PRIMARY KEY,

            welcome_channel INTEGER,
            leave_channel INTEGER,

            modlog_channel INTEGER,

            ticket_category INTEGER,
            ticket_log_channel INTEGER,

            verification_role INTEGER,
            autorole INTEGER,

            ai_enabled INTEGER DEFAULT 0,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)


def ensure_guild(guild_id: int):
    with connect() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO guild_settings(guild_id) VALUES(?)",
            (guild_id,),
        )


def get(guild_id: int):

    ensure_guild(guild_id)

    with connect() as conn:

        conn.row_factory = sqlite3.Row

        return conn.execute(
            """
            SELECT *
            FROM guild_settings
            WHERE guild_id=?
            """,
            (guild_id,),
        ).fetchone()


def set_value(guild_id: int, column: str, value):

    ensure_guild(guild_id)

    with connect() as conn:

        conn.execute(
            f"UPDATE guild_settings SET {column}=? WHERE guild_id=?",
            (value, guild_id),
        )
