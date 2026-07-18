import logging
import discord

log = logging.getLogger("Odin")


def get_role(guild, name):
    return discord.utils.get(guild.roles, name=name)


def get_category(guild, name):
    return discord.utils.get(guild.categories, name=name)


def get_text_channel(guild, name):
    return discord.utils.get(guild.text_channels, name=name)


def get_voice_channel(guild, name):
    return discord.utils.get(guild.voice_channels, name=name)


async def create_role(guild, role_name):
    role = get_role(guild, role_name)

    if role is None:
        role = await guild.create_role(name=role_name)
        log.info("Created role: %s", role_name)
    else:
        log.info("Role exists: %s", role_name)

    return role


async def create_category(guild, category_name):
    category = get_category(guild, category_name)

    if category is None:
        category = await guild.create_category(category_name)
        log.info("Created category: %s", category_name)
    else:
        log.info("Category exists: %s", category_name)

    return category


async def create_text_channel(category, channel_name):
    channel = discord.utils.get(category.text_channels, name=channel_name)

    if channel is not None:
        log.info("Channel exists: %s", channel_name)
        return channel

    guild = category.guild
    overwrites = None

    if channel_name == "ticket-logs":
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False)
        }

    channel = await category.create_text_channel(
        channel_name,
        overwrites=overwrites
    )

    log.info("Created channel: %s", channel_name)
    return channel


async def create_voice_channel(guild, channel_name):
    channel = get_voice_channel(guild, channel_name)

    if channel is None:
        channel = await guild.create_voice_channel(channel_name)
        log.info("Created voice channel: %s", channel_name)
    else:
        log.info("Voice channel exists: %s", channel_name)

    return channel


async def refresh_embed(channel, embed):
    if channel is None:
        log.warning("Cannot refresh embed: channel not found")
        return

    await channel.purge(limit=25)
    await channel.send(embed=embed)
