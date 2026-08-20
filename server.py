from database import get_database


MAX_SERVERS_PER_PROJECT = 3


def get_project_servers(project_id: int):
    with get_database() as db:
        return db.execute(
            """
            SELECT *
            FROM linked_servers
            WHERE project_id = ?
            ORDER BY linked_at ASC
            """,
            (project_id,)
        ).fetchall()


def count_project_servers(project_id: int) -> int:
    with get_database() as db:
        result = db.execute(
            """
            SELECT COUNT(*) AS count
            FROM linked_servers
            WHERE project_id = ?
            """,
            (project_id,)
        ).fetchone()

        return result["count"]


def get_server_by_guild(guild_id: str):
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


def can_add_server(project_id: int) -> bool:
    return (
        count_project_servers(project_id)
        < MAX_SERVERS_PER_PROJECT
    )


def add_server(
    project_id: int,
    guild_id: str,
    guild_name: str,
    linked_at: str
) -> bool:

    if not can_add_server(project_id):
        return False

    with get_database() as db:
        db.execute(
            """
            INSERT INTO linked_servers (
                project_id,
                guild_id,
                guild_name,
                linked_at
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                project_id,
                guild_id,
                guild_name,
                linked_at
            )
        )

    return True


def remove_server(guild_id: str) -> bool:
    with get_database() as db:
        cursor = db.execute(
            """
            DELETE FROM linked_servers
            WHERE guild_id = ?
            """,
            (guild_id,)
        )

        return cursor.rowcount > 0
