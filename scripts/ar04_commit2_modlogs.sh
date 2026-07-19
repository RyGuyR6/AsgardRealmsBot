#!/usr/bin/env bash
set -e

python3 <<'PY'
from pathlib import Path

path = Path("cogs/moderation.py")
text = path.read_text()

# ------------------------------------------------------------------
# import
# ------------------------------------------------------------------
if "from services import modlog_service" not in text:
    text = text.replace(
        "from services import warning_service",
        "from services import warning_service\nfrom services import modlog_service"
    )

# ------------------------------------------------------------------
# helper
# ------------------------------------------------------------------
helper = '''

    async def _modlog_channel(guild):

        for channel in guild.text_channels:
            if channel.name.lower() in (
                "mod-logs",
                "modlog",
                "moderation-log",
                "moderation-logs",
            ):
                return channel

        return None
'''

if "_modlog_channel" not in text:
    marker = "warning_service.initialize()\n"
    text = text.replace(marker, marker + helper)

# ------------------------------------------------------------------
# warn
# ------------------------------------------------------------------
warn_old = """        await interaction.response.send_message(
            embed=embed
        )
"""

warn_new = """        await interaction.response.send_message(
            embed=embed
        )

        await modlog_service.log_action(
            channel=await _modlog_channel(interaction.guild),
            action="Warn",
            moderator=interaction.user,
            target=member,
            reason=reason,
            color=discord.Color.orange(),
        )
"""

text = text.replace(warn_old, warn_new, 1)

# ------------------------------------------------------------------
# kick
# ------------------------------------------------------------------
kick_marker = """        await interaction.response.send_message(
            embed=embed
        )
"""

kick_add = """        await interaction.response.send_message(
            embed=embed
        )

        await modlog_service.log_action(
            channel=await _modlog_channel(interaction.guild),
            action="Kick",
            moderator=interaction.user,
            target=member,
            reason=reason,
            color=discord.Color.red(),
        )
"""

text = text.replace(kick_marker, kick_add, 1)

# ------------------------------------------------------------------
# ban
# ------------------------------------------------------------------
ban_add = """        await interaction.response.send_message(
            embed=embed
        )

        await modlog_service.log_action(
            channel=await _modlog_channel(interaction.guild),
            action="Ban",
            moderator=interaction.user,
            target=member,
            reason=reason,
            color=discord.Color.dark_red(),
        )
"""

text = text.replace(kick_marker, ban_add, 1)

# ------------------------------------------------------------------
# timeout
# ------------------------------------------------------------------
timeout_add = """        await interaction.response.send_message(
            embed=embed
        )

        await modlog_service.log_action(
            channel=await _modlog_channel(interaction.guild),
            action="Timeout",
            moderator=interaction.user,
            target=member,
            reason=reason,
            color=discord.Color.gold(),
        )
"""

text = text.replace(kick_marker, timeout_add, 1)

path.write_text(text)

print("✔ moderation.py updated")
PY

python3 -m compileall .

echo
echo "AR04 Commit 2 complete."
