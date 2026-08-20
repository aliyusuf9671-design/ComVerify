import discord

from database import is_server_linked


async def backup_command(interaction: discord.Interaction):
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
            "to create a backup.",
            ephemeral=True
        )
        return

    if not is_server_linked(str(guild.id)):
        await interaction.response.send_message(
            "🔒 **ComVerify isn't set up yet.**\n\n"
            "Use `/login` with your ComVerify project key "
            "first.",
            ephemeral=True
        )
        return

    # Collect basic server information.
    channels = []

    for channel in guild.channels:
        channels.append({
            "id": str(channel.id),
            "name": channel.name,
            "type": str(channel.type),
            "position": channel.position
        })

    roles = []

    for role in guild.roles:
        roles.append({
            "id": str(role.id),
            "name": role.name,
            "position": role.position,
            "permissions": role.permissions.value,
            "hoist": role.hoist,
            "mentionable": role.mentionable
        })

    backup_data = {
        "guild_id": str(guild.id),
        "guild_name": guild.name,
        "channels": channels,
        "roles": roles
    }

    # Temporary output while we're developing.
    # Later this will be stored properly in the
    # ComVerify backend/database.
    print(
        f"Backup collected for {guild.name}: "
        f"{len(channels)} channels, "
        f"{len(roles)} roles."
    )

    embed = discord.Embed(
        title="Backup Ready",
        description=(
            f"Collected the current structure of "
            f"**{guild.name}**."
        ),
        color=discord.Color.green()
    )

    embed.add_field(
        name="Channels",
        value=str(len(channels)),
        inline=True
    )

    embed.add_field(
        name="Roles",
        value=str(len(roles)),
        inline=True
    )

    embed.set_footer(
        text="ComVerify • Backup system"
    )

    await interaction.response.send_message(
        embed=embed,
        ephemeral=True
    )
