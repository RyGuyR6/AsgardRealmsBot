#!/usr/bin/env bash
set -e

cat > views/autorole_setup.py <<'PY'
import discord
from services import settings_service


class AutoroleSelect(discord.ui.RoleSelect):

    def __init__(self):
        super().__init__(
            placeholder="Select the default member role...",
            min_values=1,
            max_values=1
        )

    async def callback(self, interaction: discord.Interaction):

        role = self.values[0]

        settings_service.set_value(
            interaction.guild.id,
            "autorole",
            role.id
        )

        await interaction.response.send_message(
            f"✅ Autorole set to {role.mention}",
            ephemeral=True
        )


class AutoroleView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=300)
        self.add_item(AutoroleSelect())
PY

python3 <<'PY'
from pathlib import Path

path = Path("views/setup_panel.py")
text = path.read_text()

if "from views.autorole_setup import AutoroleView" not in text:
    text = text.replace(
        "from views.welcome_setup import WelcomeSetupView",
        "from views.welcome_setup import WelcomeSetupView\nfrom views.autorole_setup import AutoroleView"
    )

old = '''await interaction.response.send_message(
            "Configure welcome settings below.",
            view=WelcomeSetupView(),
            ephemeral=True,
        )'''

new = '''await interaction.response.send_message(
            "Configure welcome settings and autorole below.",
            view=AutoroleView(),
            ephemeral=True,
        )'''

text = text.replace(old, new)

path.write_text(text)
PY

python3 <<'PY'
from pathlib import Path

path = Path("cogs/welcome.py")
text = path.read_text()

if "autorole" not in text:

    listener = '''

@bot.event
async def on_member_join(member):

    settings = welcome_service.settings(member.guild.id)

    role_id = settings.get("autorole")

    if role_id:
        role = member.guild.get_role(role_id)

        if role:
            try:
                await member.add_roles(role, reason="Autorole")
            except Exception:
                pass
'''

    text += listener

path.write_text(text)
PY

python -m compileall .

echo
echo "=================================="
echo "AR05_005 COMPLETE"
echo "=================================="
