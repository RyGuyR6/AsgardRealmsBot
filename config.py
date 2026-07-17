# ============================================================
#                     ASGARD REALMS BOT
#                       config.py
# ============================================================

import os

BOT_NAME = "Odin"
VERSION = "2.0.0"

# ============================================================
# Discord Bot Token
# ============================================================

TOKEN = os.getenv("TOKEN")

if TOKEN is None:
    raise ValueError(
        "Discord bot token not found. Set the TOKEN environment variable."
    )

# ============================================================
# Server Information
# ============================================================

SERVER_NAME = "Asgard Realms"
SERVER_IP = "76.164.198.116:25569"

# ============================================================
# Embed Settings
# ============================================================

EMBED_COLOR = 0x3B82F6
FOOTER = "⚔ Forge Your Saga"

# ============================================================
# Server Roles
# ============================================================

ROLES = [
    "👑 Allfather",
    "🛡 Administrator",
    "⚔ Moderator",
    "👑 Jarl",
    "🪓 Berserker",
    "🛶 Raider",
    "🧭 Traveler",
    "🤖 Herald"
]

# ============================================================
# Discord Categories & Channels
# ============================================================

TEXT_CATEGORIES = {

    "📢 INFORMATION": [
        "📜rules",
        "📚server-guide",
        "📣announcements",
        "📋patch-notes",
        "🛠development-log",
        "📅events",
        "🗳polls"
    ],

    "💬 COMMUNITY": [
        "💬general",
        "😂memes",
        "📸screenshots",
        "🎨media",
        "🏰showcase-builds"
    ],

    "🎮 MINECRAFT": [
        "🟢server-status",
        "👥online-players",
        "💰economy",
        "🏆leaderboards",
        "🎁crates",
        "📜quests",
        "⚔pvp"
    ],

    "🛡 SUPPORT": [
        "❓help",
        "🐞bug-reports",
        "💡suggestions"
    ],

    # Ticket channels are created dynamically by Odin.
    "🎫 TICKETS": [],

    "🔒 STAFF": [
        "🛡staff-chat",
        "📜staff-notes",
        "📊server-logs"
    ],

    # Internal Odin channels
    "🤖 ODIN": [
        "📋ticket-logs"
    ]
}

# ============================================================
# Voice Channels
# ============================================================

VOICE_CHANNELS = [
    "⚔ Midgard",
    "⚔ Asgard",
    "⚔ Valhalla",
    "🌙 AFK"
]