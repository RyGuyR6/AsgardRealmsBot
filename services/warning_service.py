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

        conn.execute("""
        CREATE TABLE IF NOT EXISTS cases(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guild_id INTEGER NOT NULL,
            action TEXT NOT NULL,
            moderator_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            reason TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)


# ---------------------------------------------------------
# Warning API
# ---------------------------------------------------------

def add_warning(guild_id, user_id, moderator_id, reason):

    with connection() as conn:

        cur = conn.execute(
            """
            INSERT INTO warnings
            (guild_id,user_id,moderator_id,reason)
            VALUES(?,?,?,?)
            """,
            (guild_id, user_id, moderator_id, reason),
        )

        warning_id = cur.lastrowid

        case = conn.execute(
            """
            INSERT INTO cases
            (guild_id,action,moderator_id,user_id,reason)
            VALUES(?,?,?,?,?)
            """,
            (
                guild_id,
                "Warn",
                moderator_id,
                user_id,
                reason,
            ),
        )

        case_id = case.lastrowid

        conn.commit()

        return warning_id, case_id


def get_warnings(user_id):

    with connection() as conn:

        return conn.execute(
            """
            SELECT
                id,
                moderator_id,
                reason,
                created_at
            FROM warnings
            WHERE user_id=?
            ORDER BY id DESC
            """,
            (user_id,),
        ).fetchall()


def get_warning(warning_id):

    with connection() as conn:

        return conn.execute(
            """
            SELECT *
            FROM warnings
            WHERE id=?
            """,
            (warning_id,),
        ).fetchone()


def remove_warning(warning_id):

    with connection() as conn:

        conn.execute(
            """
            DELETE FROM warnings
            WHERE id=?
            """,
            (warning_id,),
        )


def clear_warnings(user_id):

    with connection() as conn:

        conn.execute(
            """
            DELETE FROM warnings
            WHERE user_id=?
            """,
            (user_id,),
        )


def warning_count(user_id):

    with connection() as conn:

        return conn.execute(
            """
            SELECT COUNT(*)
            FROM warnings
            WHERE user_id=?
            """,
            (user_id,),
        ).fetchone()[0]


# ---------------------------------------------------------
# Case API
# ---------------------------------------------------------

def add_case(guild_id, action, moderator_id, user_id, reason):

    with connection() as conn:

        cur = conn.execute(
            """
            INSERT INTO cases
            (guild_id,action,moderator_id,user_id,reason)
            VALUES(?,?,?,?,?)
            """,
            (
                guild_id,
                action,
                moderator_id,
                user_id,
                reason,
            ),
        )

        conn.commit()

        return cur.lastrowid


def get_case(case_id):

    with connection() as conn:

        return conn.execute(
            """
            SELECT *
            FROM cases
            WHERE id=?
            """,
            (case_id,),
        ).fetchone()


def get_cases(user_id):

    with connection() as conn:

        return conn.execute(
            """
            SELECT
                id,
                action,
                moderator_id,
                reason,
                created_at
            FROM cases
            WHERE user_id=?
            ORDER BY id DESC
            """,
            (user_id,),
        ).fetchall()
