import discord

from database import is_server_linked


async def restore_command(
    interaction: discord.Interaction
):
    guild = interaction.guild

    if guild is None:
        await interaction.response.send_message(
            "❌ This command can only be used inside a server.",
            ephemeral=True
        )
        return

    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(
            "❌ You need Administrator permissions "
            "to restore a backup.",
            ephemeral=True
        )
        return

    if not is_server_linked(str(guild.id)):
        await interaction.response.send_message(
            "🔒 **ComVerify isn't set up yet.**\n\n"
            "Use `/login` first.",
            ephemeral=True
        )
        return

    await interaction.response.send_message(
        "🛠️ **Restore system**\n\n"
        "The server is connected, but the restore "
        "system isn't available yet.\n\n"
        "We'll add backup selection and restoration "
        "in the next stage.",
        ephemeral=True
    )
