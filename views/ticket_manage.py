# ============================================================
#                  ASGARD REALMS BOT
#             views/ticket_manage.py
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


class RenameModal(discord.ui.Modal, title="Rename Ticket"):

    new_name = discord.ui.TextInput(
        label="Channel Name",
        placeholder="support-john",
        max_length=90,
    )

    async def on_submit(
        self,
        interaction: discord.Interaction,
    ):

        await interaction.channel.edit(
            name=self.new_name.value.lower().replace(" ", "-")
        )

        await interaction.response.send_message(
            f"✏️ Renamed ticket to **{self.new_name.value}**",
            ephemeral=True,
        )


class CloseConfirmView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=60)

    @discord.ui.button(
        label="Confirm",
        emoji="✅",
        style=discord.ButtonStyle.danger,
    )
    async def confirm(self, interaction: discord.Interaction, button):

        metadata = get_ticket_metadata(interaction.channel.id)

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
                filename=filename,
            )

        except Exception as e:
            print(e)

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

        remove_ticket_metadata(interaction.channel.id)

        await interaction.response.send_message(
            "🔒 Closing ticket...",
            ephemeral=True,
        )

        await interaction.channel.delete()

        if filepath and os.path.exists(filepath):
            os.remove(filepath)

    @discord.ui.button(
        label="Cancel",
        emoji="❌",
        style=discord.ButtonStyle.secondary,
    )
    async def cancel(self, interaction, button):

        await interaction.response.send_message(
            "Cancelled.",
            ephemeral=True,
        )


class TicketManageView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Claim",
        emoji="👤",
        style=discord.ButtonStyle.primary,
        custom_id="ticket_claim",
    )
    async def claim(self, interaction, button):

        metadata = get_ticket_metadata(interaction.channel.id)

        if metadata and metadata.get("claimed_by"):

            if metadata["claimed_by"] != interaction.user.id:

                member = interaction.guild.get_member(
                    metadata["claimed_by"]
                )

                await interaction.response.send_message(
                    f"Already claimed by {member.mention if member else 'another moderator'}",
                    ephemeral=True,
                )
                return

        update_ticket_metadata(
            interaction.channel.id,
            claimed_by=interaction.user.id,
        )

        await interaction.response.send_message(
            f"✅ {interaction.user.mention} claimed this ticket."
        )

    @discord.ui.button(
        label="Unclaim",
        emoji="↩️",
        style=discord.ButtonStyle.secondary,
        custom_id="ticket_unclaim",
    )
    async def unclaim(self, interaction, button):

        update_ticket_metadata(
            interaction.channel.id,
            claimed_by=None,
        )

        await interaction.response.send_message(
            "↩️ Ticket unclaimed."
        )

    @discord.ui.button(
        label="Lock",
        emoji="🔒",
        style=discord.ButtonStyle.secondary,
        custom_id="ticket_lock",
    )
    async def lock(self, interaction, button):

        metadata = get_ticket_metadata(interaction.channel.id)

        if metadata:

            creator = interaction.guild.get_member(
                metadata["creator"]
            )

            if creator:

                await interaction.channel.set_permissions(
                    creator,
                    send_messages=False,
                )

        await interaction.response.send_message(
            "🔒 Ticket locked."
        )

    @discord.ui.button(
        label="Unlock",
        emoji="🔓",
        style=discord.ButtonStyle.success,
        custom_id="ticket_unlock",
    )
    async def unlock(self, interaction, button):

        metadata = get_ticket_metadata(interaction.channel.id)

        if metadata:

            creator = interaction.guild.get_member(
                metadata["creator"]
            )

            if creator:

                await interaction.channel.set_permissions(
                    creator,
                    send_messages=True,
                )

        await interaction.response.send_message(
            "🔓 Ticket unlocked."
        )

    @discord.ui.button(
        label="Rename",
        emoji="✏️",
        style=discord.ButtonStyle.secondary,
        custom_id="ticket_rename",
    )
    async def rename(self, interaction, button):

        await interaction.response.send_modal(
            RenameModal()
        )

    @discord.ui.button(
        label="Close",
        emoji="🗑️",
        style=discord.ButtonStyle.danger,
        custom_id="ticket_close",
    )
    async def close(self, interaction, button):

        embed = discord.Embed(
            title="Close Ticket",
            description="Are you sure?",
            color=discord.Color.red(),
        )

        await interaction.response.send_message(
            embed=embed,
            view=CloseConfirmView(),
            ephemeral=True,
        )