import discord


VALID_STATUSES = {
    "online": discord.Status.online,
    "idle": discord.Status.idle,
    "dnd": discord.Status.dnd,
    "invisible": discord.Status.invisible,
}


async def set_bot_status(
    interaction: discord.Interaction,
    status: str
):
    if interaction.guild is None:
        await interaction.response.send_message(
            "❌ This command can only be used inside a server.",
            ephemeral=True
        )
        return

    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(
            "❌ You need Administrator permissions "
            "to change ComVerify's status.",
            ephemeral=True
        )
        return

    status = status.lower()

    if status not in VALID_STATUSES:
        await interaction.response.send_message(
            "❌ Invalid status.\n\n"
            "Available options: `online`, `idle`, "
            "`dnd`, `invisible`.",
            ephemeral=True
        )
        return

    await interaction.response.send_message(
        "⚠️ Discord bot presence is global rather than "
        "per-server, so ComVerify can't safely give "
        "each server a different online/idle/DND state "
        "using the normal bot API.",
        ephemeral=True
    )
