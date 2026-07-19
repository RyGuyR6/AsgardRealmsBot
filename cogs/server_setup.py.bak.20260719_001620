# ============================================================
#                  ASGARD REALMS BOT
#                  server_setup.py
# ============================================================

import discord

from config import (
    SERVER_NAME,
    ROLES,
    TEXT_CATEGORIES,
    VOICE_CHANNELS,
)

from embeds import (
    make_embed,
    rules_embed,
    guide_embed,
    patch_notes_embed,
    devlog_embed,
)

from utils.helpers import (
    create_role,
    create_category,
    create_text_channel,
    create_voice_channel,
    get_text_channel,
    refresh_embed,
)


def register(bot):

    @bot.tree.command(
        name="setup",
        description="Build the Asgard Realms Discord server."
    )
    async def setup(interaction: discord.Interaction):

        await interaction.response.defer(ephemeral=True)

        guild = interaction.guild

        # =====================================================
        # Create Roles
        # =====================================================

        for role in ROLES:
            await create_role(guild, role)

        # =====================================================
        # Create Categories
        # =====================================================

        created_categories = {}

        for category_name in TEXT_CATEGORIES:

            created_categories[category_name] = await create_category(
                guild,
                category_name
            )

        # =====================================================
        # Create Text Channels
        # =====================================================

        for category_name, channels in TEXT_CATEGORIES.items():

            category = created_categories[category_name]

            for channel in channels:

                await create_text_channel(
                    category,
                    channel
                )

        # =====================================================
        # Create Voice Channels
        # =====================================================

        for voice in VOICE_CHANNELS:

            await create_voice_channel(
                guild,
                voice
            )

        # =====================================================
        # Populate Information Channels
        # =====================================================

        await refresh_embed(
            get_text_channel(guild, "📜rules"),
            rules_embed()
        )

        await refresh_embed(
            get_text_channel(guild, "📚server-guide"),
            guide_embed()
        )

        await refresh_embed(
            get_text_channel(guild, "📋patch-notes"),
            patch_notes_embed()
        )

        await refresh_embed(
            get_text_channel(guild, "🛠development-log"),
            devlog_embed()
        )

        # =====================================================
        # Finished
        # =====================================================

        await interaction.followup.send(

            embed=make_embed(

                "⚔ Setup Complete",

                f"""
Successfully configured **{SERVER_NAME}**

✅ Roles Created

✅ Categories Created

✅ Text Channels Created

✅ Voice Channels Created

✅ Rules Published

✅ Server Guide Published

✅ Patch Notes Published

✅ Development Log Published

⚔ Welcome to Asgard Realms!
"""
            ),

            ephemeral=True
        )