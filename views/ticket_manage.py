# ============================================================
#                  ASGARD REALMS BOT
#                 views/ticket_manage.py
# ============================================================

import os
import discord
from datetime import datetime

from services.ticket_service import (
    get_ticket_metadata,
    update_ticket_metadata,
    remove_ticket_metadata,
)

from services.transcript_service import create_transcript
from services.log_service import TicketLogService


class CloseConfirmView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=60)

    @discord.ui.button(
        label="Confirm",
        emoji="✅",
        style=discord.ButtonStyle.danger
    )
    async def confirm(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        metadata = get_ticket_metadata(
            interaction.channel.id
        )

        creator = interaction.user
        claimed_by = None
        opened_at = None

        if metadata:

            creator = (
                interaction.guild.get_member(
                    metadata["creator"]
                )
                or interaction.user
            )

            if metadata.get("claimed_by"):

                claimed_by = interaction.guild.get_member(
                    metadata["claimed_by"]
                )

            if metadata.get("opened_at"):

                opened_at = datetime.fromisoformat(
                    metadata["opened_at"]
                ).replace(tzinfo=None)

        filepath = None
        transcript = None

        try:

            filepath, filename = await create_transcript(
                interaction.channel
            )

            transcript = discord.File(
                filepath,
                filename=filename
            )

        except Exception as e:

            print(f"Transcript Error: {e}")

        await TicketLogService.send_log(
            guild=interaction.guild,
            channel_name="📋ticket-logs",
            ticket_channel=interaction.channel,
            creator=creator,
            closer=interaction.user,
            transcript=transcript,
            claimed_by=claimed_by,
            opened_at=opened_at,
        )

        remove_ticket_metadata(
            interaction.channel.id
        )

        await interaction.response.send_message(
            "🔒 Closing ticket...",
            ephemeral=True
        )

        await interaction.channel.delete()

        if filepath and os.path.exists(filepath):

            os.remove(filepath)

    @discord.ui.button(
        label="Cancel",
        emoji="❌",
        style=discord.ButtonStyle.secondary
    )
    async def cancel(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        await interaction.response.send_message(
            "Ticket closure cancelled.",
            ephemeral=True
        )

        self.stop()


class TicketManageView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Claim Ticket",
        emoji="👤",
        style=discord.ButtonStyle.primary,
        custom_id="ticket_claim"
    )
    async def claim_ticket(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        update_ticket_metadata(
            interaction.channel.id,
            claimed_by=interaction.user.id
        )

        embed = discord.Embed(
            title="⚔ Ticket Claimed",
            description=(
                f"{interaction.user.mention} "
                "has claimed this ticket."
            ),
            color=discord.Color.green()
        )

        await interaction.response.send_message(
            embed=embed
        )

    @discord.ui.button(
        label="Close Ticket",
        emoji="🔒",
        style=discord.ButtonStyle.danger,
        custom_id="ticket_close"
    )
    async def close_ticket(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        embed = discord.Embed(
            title="⚔ Close Ticket?",
            description=(
                "Are you sure you want to close this ticket?\n\n"
                "This action cannot be undone."
            ),
            color=discord.Color.red()
        )

        await interaction.response.send_message(
            embed=embed,
            view=CloseConfirmView(),
            ephemeral=True
        )