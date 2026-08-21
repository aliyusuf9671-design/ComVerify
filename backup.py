import discord

from api import ComVerifyAPI
from database import get_linked_server, get_project, is_server_linked


async def backup_command(interaction: discord.Interaction):
    guild = interaction.guild
    if guild is None:
        await interaction.response.send_message("❌ This command can only be used inside a server.", ephemeral=True)
        return
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ You need Administrator permissions to create a backup.", ephemeral=True)
        return
    linked = get_linked_server(str(guild.id))
    project = get_project(linked["project_id"]) if linked else None
    if not is_server_linked(str(guild.id)) or not linked or not project or not project["project_key"]:
        await interaction.response.send_message("🔒 **ComVerify isn't set up yet.**\n\nUse `/login` with your ComVerify project key first.", ephemeral=True)
        return

    snapshot = {
        "guild_id": str(guild.id),
        "guild_name": guild.name,
        "channels": [{"name": channel.name, "type": str(channel.type), "position": channel.position, "category": channel.category.name if channel.category else None} for channel in guild.channels],
        "roles": [{"name": role.name, "position": role.position, "permissions": role.permissions.value, "hoist": role.hoist, "mentionable": role.mentionable} for role in guild.roles if not role.is_default() and not role.managed],
    }
    await interaction.response.defer(ephemeral=True)
    status, result = await ComVerifyAPI().create_backup(project["project_key"], str(guild.id), snapshot)
    if status not in (200, 201) or not result.get("success"):
        await interaction.followup.send(f"❌ Backup could not be stored: {result.get('error', f'HTTP {status}')}", ephemeral=True)
        return
    embed = discord.Embed(title="Backup Stored", description=f"Saved the current structure of **{guild.name}** to the ComVerify dashboard.", color=discord.Color.green())
    embed.add_field(name="Backup ID", value=str(result["backup_id"]), inline=True)
    embed.add_field(name="Channels", value=str(len(snapshot["channels"])), inline=True)
    embed.add_field(name="Roles", value=str(len(snapshot["roles"])), inline=True)
    embed.set_footer(text="ComVerify • Backup system")
    await interaction.followup.send(embed=embed, ephemeral=True)
