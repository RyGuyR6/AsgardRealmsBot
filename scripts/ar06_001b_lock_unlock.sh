#!/usr/bin/env bash
set -e

python3 <<'PY'
from pathlib import Path

path = Path("views/ticket_manage.py")
text = path.read_text()

if 'custom_id="ticket_lock"' not in text:

    code = '''

    @discord.ui.button(
        label="Lock",
        emoji="🔒",
        style=discord.ButtonStyle.secondary,
        custom_id="ticket_lock"
    )
    async def lock_ticket(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        metadata = get_ticket_metadata(interaction.channel.id)

        if not metadata:
            await interaction.response.send_message(
                "Ticket metadata not found.",
                ephemeral=True
            )
            return

        member = interaction.guild.get_member(metadata["owner_id"])

        if member:
            await interaction.channel.set_permissions(
                member,
                send_messages=False
            )

        await interaction.response.send_message(
            f"🔒 Ticket locked by {interaction.user.mention}"
        )


    @discord.ui.button(
        label="Unlock",
        emoji="🔓",
        style=discord.ButtonStyle.success,
        custom_id="ticket_unlock"
    )
    async def unlock_ticket(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        metadata = get_ticket_metadata(interaction.channel.id)

        if not metadata:
            await interaction.response.send_message(
                "Ticket metadata not found.",
                ephemeral=True
            )
            return

        member = interaction.guild.get_member(metadata["owner_id"])

        if member:
            await interaction.channel.set_permissions(
                member,
                send_messages=True
            )

        await interaction.response.send_message(
            f"🔓 Ticket unlocked by {interaction.user.mention}"
        )
'''

    marker = "@discord.ui.button(\n        label=\"Close Ticket\""

    text = text.replace(marker, code + "\n\n    " + marker)

path.write_text(text)
PY

python -m compileall .

echo
echo "=================================="
echo " AR06.001B COMPLETE"
echo "=================================="
