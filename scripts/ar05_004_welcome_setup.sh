#!/usr/bin/env bash
set -e

cat > views/welcome_setup.py <<'PY'
import discord
from services import settings_service


class WelcomeChannelSelect(discord.ui.ChannelSelect):
    def __init__(self):
        super().__init__(
            placeholder="Select Welcome Channel",
            channel_types=[discord.ChannelType.text],
            min_values=1,
            max_values=1,
        )

    async def callback(self, interaction: discord.Interaction):
        channel = self.values[0]

        settings_service.set_value(
            interaction.guild.id,
            "welcome_channel",
            channel.id,
        )

        await interaction.response.send_message(
            f"✅ Welcome channel set to {channel.mention}",
            ephemeral=True,
        )


class LeaveChannelSelect(discord.ui.ChannelSelect):
    def __init__(self):
        super().__init__(
            placeholder="Select Leave Channel",
            channel_types=[discord.ChannelType.text],
            min_values=1,
            max_values=1,
        )

    async def callback(self, interaction: discord.Interaction):
        channel = self.values[0]

        settings_service.set_value(
            interaction.guild.id,
            "leave_channel",
            channel.id,
        )

        await interaction.response.send_message(
            f"✅ Leave channel set to {channel.mention}",
            ephemeral=True,
        )


class WelcomeSetupView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)
        self.add_item(WelcomeChannelSelect())
        self.add_item(LeaveChannelSelect())
PY

python3 <<'PY'
from pathlib import Path

path = Path("views/setup_panel.py")
text = path.read_text()

if "from views.welcome_setup import WelcomeSetupView" not in text:
    text = text.replace(
        "from services import settings_service",
        "from services import settings_service\nfrom views.welcome_setup import WelcomeSetupView",
    )

old = '''await interaction.response.send_message(
            "Coming soon.",
            ephemeral=True,
        )'''

new = '''await interaction.response.send_message(
            "Configure welcome settings below.",
            view=WelcomeSetupView(),
            ephemeral=True,
        )'''

text = text.replace(old, new, 1)

path.write_text(text)
PY

python -m compileall .

echo
echo "======================================"
echo "AR05_004 COMPLETE"
echo "======================================"
