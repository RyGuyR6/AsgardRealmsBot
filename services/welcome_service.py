# ============================================================
#                  ASGARD REALMS BOT
#              services/welcome_service.py
# ============================================================

import discord

from embeds import make_embed
from config import (
    SERVER_NAME,
    SERVER_IP,
)

WELCOME_BANNER = "assets/odin_welcome.PNG"


# ============================================================
#                  WELCOME EMBED
# ============================================================

def welcome_embed(member: discord.Member) -> discord.Embed:

    embed = make_embed(
        "⚔ Odin Welcomes You to Asgard Realms",
        f"""
Welcome, {member.mention}.

# Your journey begins now.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 🎮 Server Information

**IP Address**
`{SERVER_IP}`

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Before setting out:

📜 Read the server rules.

💬 Introduce yourself to the community.

🎮 Join the server and begin your adventure.

🎫 Need help?

Visit the **Odin Support Center**.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

*May Odin guide your path through the Nine Realms.*
"""
    )

    embed.set_image(
        url="attachment://odin_welcome.PNG"
    )

    return embed


# ============================================================
#                  GOODBYE EMBED
# ============================================================

def goodbye_embed(member: discord.Member) -> discord.Embed:

    embed = make_embed(
        "⚔ Farewell, Viking",
        f"""
{member.display_name} has departed **{SERVER_NAME}**.

May your legend live on throughout the Nine Realms.

Until we meet again...
"""
    )

    return embed


# ============================================================
#                  BANNER FILE
# ============================================================

def welcome_banner():

    return discord.File(
        WELCOME_BANNER,
        filename="odin_welcome.PNG"
    )