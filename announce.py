import discord

from database import is_server_linkedimport discord

from database import get_login_context
from members import get_verified_members


async def announce_verified(
    interaction: discord.Interaction,
    message: str
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
            "to send verified-member announcements.",
            ephemeral=True
        )
        return

    if not get_login_context(str(guild.id)):
        await interaction.response.send_message(
            "🔒 **ComVerify isn't set up yet.**\n\n"
            "Use `/login` first.",
            ephemeral=True
        )
        return

    members = get_verified_members(
        str(guild.id)
    )

    if not members:
        await interaction.response.send_message(
            "ℹ️ There are currently no verified "
            "members to announce to.",
            ephemeral=True
        )
        return

    await interaction.response.defer(
        ephemeral=True
    )

    sent = 0
    failed = 0

    for record in members:

        user_id = int(
            record["user_id"]
        )

        try:
            user = await interaction.client.fetch_user(
                user_id
            )

            embed = discord.Embed(
                title=f"Announcement from {guild.name}",
                description=message,
                color=discord.Color.blurple()
            )

            embed.set_footer(
                text="ComVerify"
            )

            await user.send(
                embed=embed
            )

            sent += 1

        except (
            discord.Forbidden,
            discord.NotFound,
            discord.HTTPException
        ):
            failed += 1

    await interaction.followup.send(
        f"📢 **Announcement complete.**\n\n"
        f"Sent: `{sent}`\n"
        f"Failed: `{failed}`",
        ephemeral=True
    )

from members import get_verified_members


async def announce_verified(
    interaction: discord.Interaction,
    message: str
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
            "to send verified-member announcements.",
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

    members = get_verified_members(
        str(guild.id)
    )

    if not members:
        await interaction.response.send_message(
            "ℹ️ There are currently no verified "
            "members to announce to.",
            ephemeral=True
        )
        return

    await interaction.response.defer(
        ephemeral=True
    )

    sent = 0
    failed = 0

    for record in members:

        user_id = int(
            record["user_id"]
        )

        try:
            user = await interaction.client.fetch_user(
                user_id
            )

            embed = discord.Embed(
                title=f"Announcement from {guild.name}",
                description=message,
                color=discord.Color.blurple()
            )

            embed.set_footer(
                text="ComVerify"
            )

            await user.send(
                embed=embed
            )

            sent += 1

        except (
            discord.Forbidden,
            discord.NotFound,
            discord.HTTPException
        ):
            failed += 1

    await interaction.followup.send(
        f"📢 **Announcement complete.**\n\n"
        f"Sent: `{sent}`\n"
        f"Failed: `{failed}`",
        ephemeral=True
    )
