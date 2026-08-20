from datetime import datetime, timezone

import discord

from database import get_database


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def record_verified_member(
    project_id: int,
    guild_id: str,
    member: discord.Member
) -> None:
    with get_database() as db:

        db.execute(
            """
            INSERT INTO verified_members (
                project_id,
                guild_id,
                user_id,
                username,
                verified_at
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                project_id,
                guild_id,
                str(member.id),
                str(member),
                utc_now()
            )
        )


def get_verified_members(
    guild_id: str
):
    with get_database() as db:

        return db.execute(
            """
            SELECT *
            FROM verified_members
            WHERE guild_id = ?
            ORDER BY verified_at DESC
            """,
            (guild_id,)
        ).fetchall()


def get_verified_member(
    guild_id: str,
    user_id: str
):
    with get_database() as db:

        return db.execute(
            """
            SELECT *
            FROM verified_members
            WHERE guild_id = ?
            AND user_id = ?
            LIMIT 1
            """,
            (
                guild_id,
                user_id
            )
        ).fetchone()


def count_verified_members(
    guild_id: str
) -> int:
    with get_database() as db:

        result = db.execute(
            """
            SELECT COUNT(*) AS count
            FROM verified_members
            WHERE guild_id = ?
            """,
            (guild_id,)
        ).fetchone()

        return result["count"]
