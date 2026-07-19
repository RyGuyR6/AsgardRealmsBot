#!/usr/bin/env bash
set -e

python3 <<'PY'
from pathlib import Path
import re

path = Path("views/ticket_manage.py")
text = path.read_text()

old = """        update_ticket_metadata(
            interaction.channel.id,
            claimed_by=interaction.user.id
        )
"""

new = """        metadata = get_ticket_metadata(
            interaction.channel.id
        )

        if metadata and metadata.get("claimed_by"):

            if metadata["claimed_by"] != interaction.user.id:

                member = interaction.guild.get_member(
                    metadata["claimed_by"]
                )

                owner = (
                    member.mention
                    if member
                    else "another moderator"
                )

                await interaction.response.send_message(
                    f"❌ This ticket is already claimed by {owner}.",
                    ephemeral=True
                )
                return

            await interaction.response.send_message(
                "ℹ️ You already claimed this ticket.",
                ephemeral=True
            )
            return

        update_ticket_metadata(
            interaction.channel.id,
            claimed_by=interaction.user.id
        )
"""

text = text.replace(old,new)

if "ticket_unclaim" not in text:

    insert = '''
    @discord.ui.button(
        label="Unclaim",
        emoji="↩️",
        style=discord.ButtonStyle.secondary,
        custom_id="ticket_unclaim"
    )
    async def unclaim_ticket(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        metadata = get_ticket_metadata(
            interaction.channel.id
        )

        if not metadata:

            await interaction.response.send_message(
                "No ticket metadata found.",
                ephemeral=True
            )
            return

        if metadata.get("claimed_by") != interaction.user.id:

            await interaction.response.send_message(
                "Only the current claimer can unclaim this ticket.",
                ephemeral=True
            )
            return

        update_ticket_metadata(
            interaction.channel.id,
            claimed_by=None
        )

        embed = discord.Embed(
            title="↩️ Ticket Unclaimed",
            description=f"{interaction.user.mention} released this ticket.",
            color=discord.Color.orange()
        )

        await interaction.response.send_message(embed=embed)
'''

    text = text.replace(
        "@discord.ui.button(\n        label=\"Close Ticket\"",
        insert + "\n\n    @discord.ui.button(\n        label=\"Close Ticket\""
    )

path.write_text(text)
PY

python -m compileall .

echo
echo "=================================="
echo " AR06_001A COMPLETE"
echo "=================================="
