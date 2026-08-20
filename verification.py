import os

import discord


COMVERIFY_VERIFY_URL = os.getenv(
    "COMVERIFY_VERIFY_URL",
    "https://example.com/verify"
)


class VerifyView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        self.add_item(
            discord.ui.Button(
                label="Verify",
                style=discord.ButtonStyle.success,
                emoji="✅",
                url=COMVERIFY_VERIFY_URL
            )
        )


async def send_verification_embed(
    interaction: discord.Interaction
):
    embed = discord.Embed(
        title="Verify with ComVerify",
        description=(
            "Click the button below to begin verification.\n\n"
            "You will be taken to the ComVerify verification "
            "page where you can review what information is "
            "requested before continuing."
        ),
        color=discord.Color.blurple()
    )

    embed.set_footer(
        text="ComVerify • Community Verification"
    )

    await interaction.response.send_message(
        embed=embed,
        view=VerifyView()
    )
