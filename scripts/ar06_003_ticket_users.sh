#!/usr/bin/env bash
set -e

echo "==============================="
echo " AR06.003 - Ticket User Manager"
echo "==============================="

cat > views/ticket_user_manage.py <<'PY'
import discord


class AddUserModal(discord.ui.Modal, title="Add User"):

    user_id = discord.ui.TextInput(
        label="User ID",
        placeholder="Enter Discord User ID",
        required=True,
    )

    async def on_submit(self, interaction: discord.Interaction):

        try:
            member = await interaction.guild.fetch_member(
                int(self.user_id.value)
            )
        except Exception:
            await interaction.response.send_message(
                "❌ User not found.",
                ephemeral=True,
            )
            return

        await interaction.channel.set_permissions(
            member,
            view_channel=True,
            send_messages=True,
            read_message_history=True,
        )

        await interaction.response.send_message(
            f"✅ Added {member.mention} to the ticket."
        )


class RemoveUserModal(discord.ui.Modal, title="Remove User"):

    user_id = discord.ui.TextInput(
        label="User ID",
        placeholder="Enter Discord User ID",
        required=True,
    )

    async def on_submit(self, interaction: discord.Interaction):

        try:
            member = await interaction.guild.fetch_member(
                int(self.user_id.value)
            )
        except Exception:
            await interaction.response.send_message(
                "❌ User not found.",
                ephemeral=True,
            )
            return

        await interaction.channel.set_permissions(
            member,
            overwrite=None,
        )

        await interaction.response.send_message(
            f"🗑 Removed {member.mention} from the ticket."
        )
PY

python3 <<'PY'
from pathlib import Path

path = Path("views/ticket_manage.py")
text = path.read_text()

if "ticket_user_manage" not in text:
    text = text.replace(
        "import discord",
        "import discord\nfrom views.ticket_user_manage import AddUserModal, RemoveUserModal"
    )

marker = '''
    @discord.ui.button(
        label="Close"
'''

buttons = '''
    @discord.ui.button(
        label="Add User",
        emoji="➕",
        style=discord.ButtonStyle.success,
        custom_id="ticket_add_user",
    )
    async def add_user(self, interaction: discord.Interaction, button):

        await interaction.response.send_modal(
            AddUserModal()
        )


    @discord.ui.button(
        label="Remove User",
        emoji="➖",
        style=discord.ButtonStyle.secondary,
        custom_id="ticket_remove_user",
    )
    async def remove_user(self, interaction: discord.Interaction, button):

        await interaction.response.send_modal(
            RemoveUserModal()
        )


''' + marker

text = text.replace(marker, buttons)

path.write_text(text)
PY

echo
echo "Compiling..."
python -m compileall .

echo
echo "================================"
echo "AR06.003 COMPLETE"
echo "================================"
echo
echo "Commit with:"
echo "git add ."
echo 'git commit -m "AR06.003: Ticket user management"'

