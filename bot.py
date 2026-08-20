import os

import discord
from discord import app_commands
from dotenv import load_dotenv


load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise RuntimeError(
        "DISCORD_TOKEN is not set. "
        "Add it to your environment variables."
    )


class ComVerify(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()

        super().__init__(intents=intents)

        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

    async def on_ready(self):
        print(f"ComVerify is online as {self.user}")
        print(f"Connected to {len(self.guilds)} server(s)")


bot = ComVerify()


@bot.tree.command(
    name="ping",
    description="Check if ComVerify is online."
)
async def ping(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)

    await interaction.response.send_message(
        f"🏓 Pong! `{latency}ms`"
    )


@bot.tree.command(
    name="help",
    description="Show ComVerify's commands."
)
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(
        title="ComVerify",
        description="Community verification and recovery.",
        color=discord.Color.blurple()
    )

    embed.add_field(
        name="Available Commands",
        value=(
            "`/ping` — Check if ComVerify is online\n"
            "`/help` — Show this help menu"
        ),
        inline=False
    )

    await interaction.response.send_message(
        embed=embed,
        ephemeral=True
    )


bot.run(TOKEN)
