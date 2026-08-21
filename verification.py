import os

import discord

from database import get_login_context


class VerifyView(discord.ui.View):
    def __init__(self, authorization_url: str):
        super().__init__(timeout=None)
        self.add_item(discord.ui.Button(label="Authorize Discord", style=discord.ButtonStyle.link, emoji="✅", url=authorization_url))


async def send_verification_embed(interaction: discord.Interaction):
    guild = interaction.guild
    if guild is None:
        await interaction.response.send_message("❌ This command can only be used inside a server.", ephemeral=True)
        return
    linked = get_login_context(str(guild.id))
    if not linked or not linked["project_key"]:
        await interaction.response.send_message("🔒 **ComVerify isn't set up yet.**\n\nUse `/login` with your dashboard project key first.", ephemeral=True)
        return
    dashboard_server_id = linked["dashboard_server_id"]
    if not dashboard_server_id:
        await interaction.response.send_message("⚠️ This server was linked with an older bot version. Run `/login` again with the project key to enable member authorization.", ephemeral=True)
        return

    base_url = os.getenv("COMVERIFY_API_URL", "https://comverifydas-yjyffaj4.manus.space").rstrip("/")
    authorization_url = f"{base_url}/api/oauth/discord/verify/start?server_id={dashboard_server_id}"
    embed = discord.Embed(
        title="Authorize with Discord",
        description="Click the button below to authorize ComVerify. Your Discord account will be added to this connected server and recorded for member synchronization and backups.",
        color=discord.Color.green(),
    )
    embed.set_footer(text="ComVerify • Member authorization")
    await interaction.response.send_message(embed=embed, view=VerifyView(authorization_url))
