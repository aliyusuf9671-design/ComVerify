from datetime import datetime, timezone

import discord

from config import load_config
from database import get_database


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def record_verified_user(
    guild_id: str,
    user: discord.User,
    project_id: int
) -> None:
    with get_database() as db:
        db.execute(
            """
            INSERT OR IGNORE INTO verified_members (
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
                str(user.id),
                str(user),
                utc_now()
            )
        )


async def handle_verification(
    guild: discord.Guild,
    user: discord.User,
    project_id: int
):
    config = load_config(
        str(guild.id)
    )

    record_verified_user(
        guild_id=str(guild.id),
        user=user,
        project_id=project_id
    )

    return {
        "guild_id": str(guild.id),
        "user_id": str(user.id),
        "verified_at": utc_now(),
        "verification": config.get(
            "verification",
            {}
        )
    }
