import discord

from database import is_server_linked


async def customize_bot(
    interaction: discord.Interaction,
    display_name: str
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
            "to customize ComVerify in this server.",
            ephemeral=True
        )
        return

    if not is_server_linked(str(guild.id)):
        await interaction.response.send_message(
            "🔒 **This server isn't connected to ComVerify.**\n\n"
            "Use `/login` first.",
            ephemeral=True
        )
        return

    me = guild.me

    if me is None:
        await interaction.response.send_message(
            "❌ I couldn't find my member profile "
            "in this server.",
            ephemeral=True
        )
        return

    if not me.guild_permissions.manage_nicknames:
        await interaction.response.send_message(
            "❌ I need the **Manage Nicknames** permission "
            "to change my server display name.",
            ephemeral=True
        )
        return

    if not display_name.strip():
        await interaction.response.send_message(
            "❌ The display name cannot be empty.",
            ephemeral=True
        )
        return

    display_name = display_name.strip()

    if len(display_name) > 32:
        await interaction.response.send_message(
            "❌ Discord display names can be at most "
            "32 characters.",
            ephemeral=True
        )
        return

    try:
        await me.edit(
            nick=display_name,
            reason="ComVerify server customization"
        )

    except discord.Forbidden:
        await interaction.response.send_message(
            "❌ Discord refused the nickname change. "
            "Make sure ComVerify's role is high enough "
            "in the server's role list.",
            ephemeral=True
        )
        return

    except discord.HTTPException as error:
        print(
            f"Customization error: {error}"
        )

        await interaction.response.send_message(
            "❌ Discord returned an error while "
            "changing the display name.",
            ephemeral=True
        )
        return

    await interaction.response.send_message(
        "✅ **ComVerify customized!**\n\n"
        f"Server display name: **{display_name}**\n\n"
        "This only changes how ComVerify appears "
        "in this server. It does not change the "
        "bot's global Discord username.",
        ephemeral=True
    )
