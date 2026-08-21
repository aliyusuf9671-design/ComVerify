import os
import sqlite3
from pathlib import Path


DEFAULT_DATABASE_PATH = Path(__file__).resolve().parent / "comverify.db"
DATABASE_PATH = Path(os.getenv("DATABASE_PATH", str(DEFAULT_DATABASE_PATH))).expanduser().resolve()
DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)


def get_database():
    db = sqlite3.connect(
        DATABASE_PATH
    )

    db.row_factory = sqlite3.Row

    return db


def initialize_database():

    with get_database() as db:

        db.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                owner_id TEXT NOT NULL,
                project_key TEXT,
                created_at TEXT NOT NULL
            )
        """)

        db.execute("""
            CREATE TABLE IF NOT EXISTS linked_servers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                project_id INTEGER NOT NULL,
                dashboard_server_id INTEGER,

                guild_id TEXT NOT NULL UNIQUE,

                guild_name TEXT,

                linked_at TEXT NOT NULL,

                FOREIGN KEY (project_id)
                    REFERENCES projects(id)
                    ON DELETE CASCADE
            )
        """)

        project_columns = {row[1] for row in db.execute("PRAGMA table_info(projects)").fetchall()}
        if "project_key" not in project_columns:
            db.execute("ALTER TABLE projects ADD COLUMN project_key TEXT")

        columns = {row[1] for row in db.execute("PRAGMA table_info(linked_servers)").fetchall()}
        if "dashboard_server_id" not in columns:
            db.execute("ALTER TABLE linked_servers ADD COLUMN dashboard_server_id INTEGER")

        db.execute("""
            CREATE TABLE IF NOT EXISTS verified_members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                project_id INTEGER NOT NULL,

                guild_id TEXT NOT NULL,

                user_id TEXT NOT NULL,

                username TEXT,

                verified_at TEXT NOT NULL,

                UNIQUE(
                    project_id,
                    guild_id,
                    user_id
                ),

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

                created_at TEXT NOT NULL,

                backup_data TEXT NOT NULL,

                FOREIGN KEY (project_id)
                    REFERENCES projects(id)
                    ON DELETE CASCADE
            )
        """)

        db.execute("""
            CREATE TABLE IF NOT EXISTS server_config (
                guild_id TEXT PRIMARY KEY,

                project_id INTEGER NOT NULL,

                config_data TEXT NOT NULL,

                updated_at TEXT NOT NULL,

                FOREIGN KEY (project_id)
                    REFERENCES projects(id)
                    ON DELETE CASCADE
            )
        """)


def is_server_linked(
    guild_id: str
) -> bool:

    with get_database() as db:

        result = db.execute(
            """
            SELECT id
            FROM linked_servers
            WHERE guild_id = ?
            LIMIT 1
            """,
            (guild_id,)
        ).fetchone()

        return result is not None


def get_linked_server(
    guild_id: str
):

    with get_database() as db:

        return db.execute(
            """
            SELECT *
            FROM linked_servers
            WHERE guild_id = ?
            LIMIT 1
            """,
            (guild_id,)
        ).fetchone()


def get_project(
    project_id: int
):

    with get_database() as db:

        return db.execute(
            """
            SELECT *
            FROM projects
            WHERE id = ?
            LIMIT 1
            """,
            (project_id,)
        ).fetchone()


def get_login_context(guild_id: str):
    """Return the single authoritative login record for a Discord guild."""
    with get_database() as db:
        return db.execute(
            """
            SELECT linked_servers.*, projects.name AS project_name,
                   projects.owner_id AS project_owner_id,
                   projects.project_key AS project_key
            FROM linked_servers
            INNER JOIN projects ON projects.id = linked_servers.project_id
            WHERE linked_servers.guild_id = ?
            LIMIT 1
            """,
            (str(guild_id),),
        ).fetchone()


def is_login_ready(guild_id: str) -> bool:
    context = get_login_context(guild_id)
    return bool(context and context["project_key"])
