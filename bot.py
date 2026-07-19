# ============================================================
#                    ASGARD REALMS BOT
#                         bot.py
# ============================================================

from services.logger import setup_logging

import logging

import discord
from discord.ext import commands

from config import (
    BOT_NAME,
    VERSION,
    TOKEN,
)

from embeds import make_embed

# ============================================================
# Import Cogs
# ============================================================

from cogs.server_setup import register as register_setup
from cogs.tickets import register as register_tickets
from cogs.welcome import register as register_welcome
from cogs.moderation import register as register_moderation

# ============================================================
#                        LOGGING
# ============================================================

setup_logging()

log = logging.getLogger("Odin")

# ============================================================
#                    DISCORD INTENTS
# ============================================================

intents = discord.Intents.default()

intents.guilds = True
intents.members = True
intents.message_content = True

# ============================================================
#                      CREATE BOT
# ============================================================

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

# ============================================================
#                  REGISTER COMMANDS
# ============================================================

register_setup(bot)
register_tickets(bot)
register_welcome(bot)
register_moderation(bot)

# ============================================================
#                        EVENTS
# ============================================================

@bot.event
async def on_ready():

    print("=" * 60)
    print()

    print("⚔ ASGARD REALMS")
    print(f"{BOT_NAME} v{VERSION}")
    print()

    print(f"Logged in as {bot.user}")
    print()

    try:

        synced = await bot.tree.sync()

        print(f"✅ Synced {len(synced)} slash commands.")

    except Exception as error:

        print(error)

    print()
    print("Bot Ready.")
    print("=" * 60)

# ============================================================
#                    SLASH COMMANDS
# ============================================================

@bot.tree.command(
    name="ping",
    description="Check if Odin is online."
)
async def ping(interaction: discord.Interaction):

    await interaction.response.send_message(

        embed=make_embed(

            "⚔ Odin",

            "🏓 Pong!\n\nOdin is online and protecting the realm."

        )

    )

# ============================================================
#                       START BOT
# ============================================================

bot.run(TOKEN)