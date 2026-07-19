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

        metadata = get_ticket_metadata(
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