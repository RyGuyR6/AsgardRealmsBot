# ============================================================
#                  ASGARD REALMS BOT
#                 views/ticket_views.py
# ============================================================

import discord


class TicketView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    async def create_ticket(
        self,
        interaction: discord.Interaction,
        ticket_type: str
    ):

        from services.ticket_service import create_ticket

        await create_ticket(
            interaction,
            ticket_type
        )

    @discord.ui.button(
        label="General Support",
        emoji="🎫",
        style=discord.ButtonStyle.primary,
        custom_id="ticket_general"
    )
    async def general_support(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        await self.create_ticket(
            interaction,
            "General Support"
        )

    @discord.ui.button(
        label="Bug Report",
        emoji="🐞",
        style=discord.ButtonStyle.danger,
        custom_id="ticket_bug"
    )
    async def bug_report(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        await self.create_ticket(
            interaction,
            "Bug Report"
        )

    @discord.ui.button(
        label="Player Report",
        emoji="⚠️",
        style=discord.ButtonStyle.secondary,
        custom_id="ticket_player"
    )
    async def player_report(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        await self.create_ticket(
            interaction,
            "Player Report"
        )

    @discord.ui.button(
        label="Purchase Support",
        emoji="💳",
        style=discord.ButtonStyle.success,
        custom_id="ticket_purchase"
    )
    async def purchase_support(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        await self.create_ticket(
            interaction,
            "Purchase Support"
        )


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

        await interaction.response.send_message(
            "🔒 Ticket closed.",
            ephemeral=True
        )

        await interaction.channel.delete()

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
            "Ticket close cancelled.",
            ephemeral=True
        )

        self.stop()