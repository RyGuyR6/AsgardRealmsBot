import logging
import discord

from config import SERVER_NAME, ROLES, TEXT_CATEGORIES, VOICE_CHANNELS
from embeds import make_embed, rules_embed, guide_embed, patch_notes_embed, devlog_embed
from utils.helpers import create_role, create_category, create_text_channel, create_voice_channel, get_text_channel, refresh_embed

log = logging.getLogger("Odin")


def register(bot):

    @bot.tree.command(name="setup", description="Build the Asgard Realms Discord server.")
    async def setup(interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        try:
            guild = interaction.guild

            if guild is None:
                await interaction.followup.send("Setup failed: This command must be used in a server.", ephemeral=True)
                return

            for role in ROLES:
                await create_role(guild, role)

            created_categories = {}

            for category_name in TEXT_CATEGORIES:
                created_categories[category_name] = await create_category(guild, category_name)

            for category_name, channels in TEXT_CATEGORIES.items():
                for channel in channels:
                    await create_text_channel(created_categories[category_name], channel)

            for voice in VOICE_CHANNELS:
                await create_voice_channel(guild, voice)

            await refresh_embed(get_text_channel(guild, "rules"), rules_embed())
            await refresh_embed(get_text_channel(guild, "server-guide"), guide_embed())
            await refresh_embed(get_text_channel(guild, "patch-notes"), patch_notes_embed())
            await refresh_embed(get_text_channel(guild, "development-log"), devlog_embed())

            await interaction.followup.send(
                embed=make_embed("Setup Complete", f"Successfully configured {SERVER_NAME}"),
                ephemeral=True
            )

        except Exception as error:
            log.exception("Server setup failed")
            await interaction.followup.send(
                embed=make_embed("Setup Failed", f"An error occurred: {error}"),
                ephemeral=True
            )
