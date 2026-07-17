# ============================================================
#                     ASGARD REALMS BOT
#                       embeds.py
# ============================================================

import discord

from config import (
    EMBED_COLOR,
    FOOTER,
    SERVER_NAME,
    SERVER_IP,
)


# ============================================================
#                      EMBED BUILDER
# ============================================================

def make_embed(title: str, description: str):

    embed = discord.Embed(
        title=title,
        description=description,
        color=EMBED_COLOR
    )

    embed.set_author(
        name=SERVER_NAME
    )

    embed.set_footer(
        text=FOOTER
    )

    return embed


# ============================================================
#                      RULES EMBED
# ============================================================

def rules_embed():

    return make_embed(
        "📜 Rules of Asgard Realms",
        """
# Welcome, Viking!

To keep the realm enjoyable for everyone:

⚔ Respect all players.

🚫 No cheating, hacks, x-ray, or exploits.

🏠 No griefing or stealing.

💬 Keep chat respectful.

📢 No excessive spam.

🛡 Staff decisions are final.

🎉 Most importantly...

Forge your own saga and have fun!
"""
    )


# ============================================================
#                    SERVER GUIDE EMBED
# ============================================================

def guide_embed():

    return make_embed(
        "📚 Server Guide",
        f"""
# Welcome to Asgard Realms

**Server IP**

`{SERVER_IP}`

## Getting Started

🪓 Gather resources

🏠 Build your settlement

💰 Earn money

📜 Complete quests

🎁 Open crates

🏆 Climb the leaderboards

Good luck, Viking!
"""
    )


# ============================================================
#                   PATCH NOTES EMBED
# ============================================================

def patch_notes_embed():

    return make_embed(
        "📋 Patch Notes",
        """
## Version 2.0

### Added

✅ Odin Discord Bot

✅ Server Roles

✅ Discord Categories

✅ Text Channels

✅ Voice Channels

More updates coming soon!
"""
    )


# ============================================================
#                  DEVELOPMENT LOG EMBED
# ============================================================

def devlog_embed():

    return make_embed(
        "🛠 Development Log",
        """
## Current Progress

✅ Discord Bot

✅ Branding

🚧 Minecraft Server

🚧 Economy

🚧 Spawn

🚧 Quests

Thanks for following development!
"""
    )