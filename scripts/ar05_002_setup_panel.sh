#!/usr/bin/env bash
set -e

mkdir -p views

cat > views/setup_panel.py <<'PY'
import discord

class SetupPanel(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Welcome",
        emoji="👋",
        style=discord.ButtonStyle.blurple,
        custom_id="setup:welcome"
    )
    async def welcome(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        await interaction.response.send_message(
            "Welcome configuration coming soon.",
            ephemeral=True
        )

    @discord.ui.button(
        label="Moderation",
        emoji="🛡️",
        style=discord.ButtonStyle.red,
        custom_id="setup:moderation"
    )
    async def moderation(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        await interaction.response.send_message(
            "Moderation configuration coming soon.",
            ephemeral=True
        )

    @discord.ui.button(
        label="Tickets",
        emoji="🎫",
        style=discord.ButtonStyle.green,
        custom_id="setup:tickets"
    )
    async def tickets(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        await interaction.response.send_message(
            "Ticket configuration coming soon.",
            ephemeral=True
        )

    @discord.ui.button(
        label="Logging",
        emoji="📜",
        style=discord.ButtonStyle.gray,
        custom_id="setup:logging"
    )
    async def logging(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        await interaction.response.send_message(
            "Logging configuration coming soon.",
            ephemeral=True
        )
PY

python3 <<'PY'
from pathlib import Path

p = Path("cogs/setup.py")
text = p.read_text()

if "from views.setup_panel import SetupPanel" not in text:
    text = text.replace(
        "from services import settings_service",
        "from services import settings_service\nfrom views.setup_panel import SetupPanel"
    )

text = text.replace(
    "await interaction.response.send_message(\n            embed=embed,\n            ephemeral=True\n        )",
    "await interaction.response.send_message(\n            embed=embed,\n            view=SetupPanel(),\n            ephemeral=True\n        )"
)

p.write_text(text)
print("Updated setup.py")
PY

python -m compileall .

echo
echo "AR05_002 COMPLETE"
