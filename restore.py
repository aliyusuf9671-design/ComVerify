import discord

from api import ComVerifyAPI
from database import get_login_context


async def restore_command(interaction: discord.Interaction, backup_id: str | None = None):
    guild = interaction.guild
    if guild is None:
        await interaction.response.send_message("❌ This command can only be used inside a server.", ephemeral=True)
        return
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ You need Administrator permissions to restore a backup.", ephemeral=True)
        return
    context = get_login_context(str(guild.id))
    if not context or not context["project_key"]:
        await interaction.response.send_message("🔒 **ComVerify isn't set up yet.**\n\nUse `/login` with your ComVerify project key first.", ephemeral=True)
        return

    api = ComVerifyAPI()
    if backup_id is None:
        status, result = await api.list_backups(context["project_key"], str(guild.id))
        if status != 200 or not result.get("backups"):
            await interaction.response.send_message("❌ No stored backups are available for this server.", ephemeral=True)
            return
        backup_id = str(result["backups"][0]["id"])

    await interaction.response.defer(ephemeral=True)
    status, result = await api.fetch_backup(context["project_key"], str(guild.id), backup_id)
    if status != 200 or not result.get("success"):
        await interaction.followup.send(f"❌ Backup could not be loaded: {result.get('error', f'HTTP {status}')}", ephemeral=True)
        return

    snapshot = result.get("snapshot") or {}
    created_roles = 0
    created_channels = 0
    for role_data in snapshot.get("roles", []):
        if not discord.utils.get(guild.roles, name=role_data.get("name")):
            try:
                await guild.create_role(name=role_data.get("name", "Restored role"), permissions=discord.Permissions(role_data.get("permissions", 0)), hoist=bool(role_data.get("hoist")), mentionable=bool(role_data.get("mentionable")), reason=f"ComVerify restore #{backup_id}")
                created_roles += 1
            except discord.HTTPException:
                continue
    existing_channels = {channel.name for channel in guild.channels}
    for channel_data in snapshot.get("channels", []):
        name = channel_data.get("name")
        if not name or name in existing_channels:
            continue
        try:
            if channel_data.get("type") == "voice":
                await guild.create_voice_channel(name, reason=f"ComVerify restore #{backup_id}")
            else:
                await guild.create_text_channel(name, reason=f"ComVerify restore #{backup_id}")
            created_channels += 1
        except discord.HTTPException:
            continue

    complete_status, complete_result = await api.complete_restore(context["project_key"], str(guild.id), backup_id)
    if complete_status != 200 or not complete_result.get("success"):
        await interaction.followup.send("⚠️ The structure was restored, but the dashboard could not mark the backup as restored.", ephemeral=True)
        return
    await interaction.followup.send(f"✅ **Restore complete.** Backup `#{backup_id}` recreated `{created_roles}` roles and `{created_channels}` channels that were missing. Existing server items were preserved.", ephemeral=True)
