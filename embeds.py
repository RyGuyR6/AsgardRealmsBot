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
    SERVER_VERSION,
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
#                     WELCOME EMBED
# ============================================================

def welcome_embed(member=None):

    if member is None:
        player = "Adventurer"
    else:
        player = member.mention

    embed = make_embed(
        "⚔ Odin Welcomes You to Asgard Realms",
        f"""
Welcome, {player}.

# Your journey begins now.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 🎮 Server Information

**Minecraft Version**
`{SERVER_VERSION}`

**Server IP**
`{SERVER_IP}`

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Before setting out

📜 Read the server rules.

💬 Introduce yourself to the community.

🎮 Join the Minecraft server and begin your adventure.

🎫 Need help?

Visit the **Odin Support Center**.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Forge alliances.

Build your legacy.

Become a legend.

*May Odin guide your path through the Nine Realms.*
"""
    )

    embed.set_image(
        url="attachment://odin_welcome.PNG"
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