# ============================================================
#                     ASGARD REALMS BOT
#                        utils.py
# ============================================================

import logging
import discord

log = logging.getLogger("Odin")

# ============================================================
#                      GET HELPERS
# ============================================================

def get_role(guild, name):
    return discord.utils.get(guild.roles, name=name)


def get_category(guild, name):
    return discord.utils.get(guild.categories, name=name)


def get_text_channel(guild, name):
    return discord.utils.get(guild.text_channels, name=name)


def get_voice_channel(guild, name):
    return discord.utils.get(guild.voice_channels, name=name)


# ============================================================
#                  CREATE ROLE
# ============================================================

async def create_role(guild, role_name):

    role = get_role(guild, role_name)

    if role is None:

        role = await guild.create_role(name=role_name)

        log.info(f"✅ Created role: {role_name}")

    else:

        log.info(f"✔ Role exists: {role_name}")

    return role


# ============================================================
#                CREATE CATEGORY
# ============================================================

async def create_category(guild, category_name):

    category = get_category(guild, category_name)

    if category is None:

        category = await guild.create_category(category_name)

        log.info(f"✅ Created category: {category_name}")

    else:

        log.info(f"✔ Category exists: {category_name}")

    return category


# ============================================================
#              CREATE TEXT CHANNEL
# ============================================================

async def create_text_channel(category, channel_name):

    channel = discord.utils.get(
        category.text_channels,
        name=channel_name
    )

    if channel is None:

        channel = await category.create_text_channel(channel_name)

        log.info(f"✅ Created channel: {channel_name}")

    else:

        log.info(f"✔ Channel exists: {channel_name}")

    return channel


# ============================================================
#             CREATE VOICE CHANNEL
# ============================================================

async def create_voice_channel(guild, channel_name):

    channel = get_voice_channel(guild, channel_name)

    if channel is None:

        channel = await guild.create_voice_channel(channel_name)

        log.info(f"✅ Created voice channel: {channel_name}")

    else:

        log.info(f"✔ Voice channel exists: {channel_name}")

    return channel


# ============================================================
#             PURGE & SEND EMBED
# ============================================================

async def refresh_embed(channel, embed):

    if channel is None:
        return

    await channel.purge(limit=25)
    await channel.send(embed=embed)