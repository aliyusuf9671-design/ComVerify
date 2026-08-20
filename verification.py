import discord

from config import load_config


class VerifyView(discord.ui.View):
    def __init__(
        self,
        verification_url: str,
        button_text: str,
        button_emoji: str
    ):
        super().__init__(timeout=None)

        self.add_item(
            discord.ui.Button(
                label=button_text,
                style=discord.ButtonStyle.success,
                emoji=button_emoji,
                url=verification_url
            )
        )


async def send_verification_embed(
    interaction: discord.Interaction
):
    guild = interaction.guild

    if guild is None:
        await interaction.response.send_message(
            "❌ This command can only be used inside a server.",
            ephemeral=True
        )
        return

    config = load_config(str(guild.id))
    verification = config["verification"]

    if not verification["enabled"]:
        await interaction.response.send_message(
            "❌ Verification is currently disabled.",
            ephemeral=True
        )
        return

    verification_url = verification.get(
        "verification_url"
    )

    if not verification_url:
        await interaction.response.send_message(
            "⚠️ The verification system hasn't been "
            "configured yet.",
            ephemeral=True
        )
        return

    color = discord.Color(
        verification.get(
            "color",
            0x5865F2
        )
    )

    embed = discord.Embed(
        title=verification.get(
            "title",
            "Verify with ComVerify"
        ),
        description=verification.get(
            "description",
            "Click the button below to begin verification."
        ),
        color=color
    )

    embed.set_footer(
        text="ComVerify • Community Verification"
    )

    view = VerifyView(
        verification_url=verification_url,
        button_text=verification.get(
            "button_text",
            "Verify"
        ),
        button_emoji=verification.get(
            "button_emoji",
            "✅"
        )
    )

    await interaction.response.send_message(
        embed=embed,
        view=view
    )
