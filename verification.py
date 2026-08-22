import os

import discord

from api import ComVerifyAPI
from database import get_login_context


class VerifyView(discord.ui.View):
    def __init__(self, authorization_url: str, settings: dict | None = None):
        super().__init__(timeout=None)
        settings = settings or {}
        label = settings.get("buttonText") or "Authorize Discord"
        emoji = settings.get("buttonEmoji") or "✅"
        self.add_item(discord.ui.Button(label=label[:80], style=discord.ButtonStyle.link, emoji=emoji, url=authorization_url))


def build_verification_embed(settings: dict, authorization_url: str):
    raw_colour = str(settings.get("embedColour") or "#3fe28b").lstrip("#")
    try:
        colour = discord.Color(int(raw_colour, 16))
    except ValueError:
        colour = discord.Color.green()
    embed = discord.Embed(
        title=settings.get("embedTitle") or "Authorize with Discord",
        description=settings.get("embedDescription") or "Click the button below to authorize ComVerify. Your Discord account will be added to this connected server and recorded for member synchronization and backups.",
        color=colour,
    )
    embed.set_footer(text="ComVerify • Member authorization")
    return embed, VerifyView(authorization_url, settings)


async def send_verification_embed(interaction: discord.Interaction):
    guild = interaction.guild
    if guild is None:
        await interaction.response.send_message("❌ This command can only be used inside a server.", ephemeral=True)
        return

    # A dashboard request can take longer than Discord's 3-second acknowledgement window.
    await interaction.response.defer()
    linked = get_login_context(str(guild.id))
    if not linked or not linked["project_key"]:
        await interaction.followup.send("🔒 **ComVerify isn't set up yet.**\n\nUse `/login` with your dashboard project key first.", ephemeral=True)
        return
    dashboard_server_id = linked["dashboard_server_id"]
    if not dashboard_server_id:
        await interaction.followup.send("⚠️ This server was linked with an older bot version. Run `/login` again with the project key to enable member authorization.", ephemeral=True)
        return

    settings = {}
    try:
        status, result = await ComVerifyAPI().get_settings(linked["project_key"], str(guild.id))
        if status == 200 and result.get("success"):
            settings = result.get("settings") or {}
    except Exception as error:
        print(f"Verification settings API error: {error}")

    base_url = os.getenv("COMVERIFY_API_URL", "https://comverifydas-yjyffaj4.manus.space").rstrip("/")
    authorization_url = f"{base_url}/api/oauth/discord/verify/start?server_id={dashboard_server_id}"
    embed, view = build_verification_embed(settings, authorization_url)
    await interaction.followup.send(embed=embed, view=view)
