import os
import sqlite3
from contextlib import contextmanager


DATABASE_PATH = os.getenv(
    "DATABASE_PATH",
    "comverify.db"
)


@contextmanager
def get_database():
    connection = sqlite3.connect(
        DATABASE_PATH
    )

    try:
        connection.row_factory = sqlite3.Row
        yield connection
        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def initialize_database():
    with get_database() as db:

        db.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_name TEXT NOT NULL,
                project_key_hash TEXT NOT NULL UNIQUE,
                owner_discord_id TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)

        db.execute("""
            CREATE TABLE IF NOT EXISTS linked_servers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER NOT NULL,
                guild_id TEXT NOT NULL UNIQUE,
                guild_name TEXT,
                linked_at TEXT NOT NULL,

                FOREIGN KEY (project_id)
                    REFERENCES projects(id)
                    ON DELETE CASCADE
            )
        """)

        db.execute("""
            CREATE TABLE IF NOT EXISTS verified_members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER NOT NULL,
                guild_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                username TEXT,
                verified_at TEXT NOT NULL,

                FOREIGN KEY (project_id)
                    REFERENCES projects(id)
                    ON DELETE CASCADE
            )
        """)

        db.execute("""
            CREATE TABLE IF NOT EXISTS backups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER NOT NULL,
                guild_id TEXT NOT NULL,
                backup_name TEXT NOT NULL,
                created_at TEXT NOT NULL,

                FOREIGN KEY (project_id)
                    REFERENCES projects(id)
                    ON DELETE CASCADE
            )
        """)


def get_linked_server(guild_id: str):
    with get_database() as db:
        result = db.execute(
            """
            SELECT *
            FROM linked_servers
            WHERE guild_id = ?
            """,
            (guild_id,)
        ).fetchone()

        return result


def is_server_linked(guild_id: str) -> bool:
    return get_linked_server(guild_id) is not None
