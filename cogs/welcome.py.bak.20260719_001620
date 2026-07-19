# ============================================================
#                  ASGARD REALMS BOT
#                     cogs/welcome.py
# ============================================================

import discord

from discord import app_commands

from embeds import make_embed

from services.welcome_service import (
    welcome_embed,
    goodbye_embed,
    welcome_banner,
)

# ============================================================
#                  WELCOME CHANNEL
# ============================================================

WELCOME_CHANNEL_NAME = "👋welcome"

# ============================================================
#                  REGISTER COG
# ============================================================

def register(bot):

    # --------------------------------------------------------
    # Member Joins
    # --------------------------------------------------------

    @bot.event
    async def on_member_join(member: discord.Member):

        channel = discord.utils.get(
            member.guild.text_channels,
            name=WELCOME_CHANNEL_NAME
        )

        if channel is None:
            return

        await channel.send(
            file=welcome_banner(),
            embed=welcome_embed(member)
        )

    # --------------------------------------------------------
    # Member Leaves
    # --------------------------------------------------------

    @bot.event
    async def on_member_remove(member: discord.Member):

        channel = discord.utils.get(
            member.guild.text_channels,
            name=WELCOME_CHANNEL_NAME
        )

        if channel is None:
            return

        await channel.send(
            embed=goodbye_embed(member)
        )

    # --------------------------------------------------------
    # Test Welcome
    # --------------------------------------------------------

    @bot.tree.command(
        name="testwelcome",
        description="Preview the welcome message."
    )
    @app_commands.default_permissions(administrator=True)
    async def testwelcome(
        interaction: discord.Interaction
    ):

        await interaction.response.send_message(
            file=welcome_banner(),
            embed=welcome_embed(interaction.user)
        )

    # --------------------------------------------------------
    # Set Welcome Channel
    # --------------------------------------------------------

    @bot.tree.command(
        name="setwelcome",
        description="Choose the welcome channel."
    )
    @app_commands.default_permissions(administrator=True)
    async def setwelcome(

        interaction: discord.Interaction,
        channel: discord.TextChannel

    ):

        global WELCOME_CHANNEL_NAME

        WELCOME_CHANNEL_NAME = channel.name

        await interaction.response.send_message(

            embed=make_embed(

                "⚔ Welcome Channel Updated",

                f"""
Odin will now welcome new adventurers in

{channel.mention}

⚔ Your journey begins now.
"""

            ),

            ephemeral=True

        )