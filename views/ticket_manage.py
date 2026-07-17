# ============================================================
#                  ASGARD REALMS BOT
#                 views/ticket_manage.py
# ============================================================

import discord

from views.ticket_views import CloseConfirmView


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

        embed = discord.Embed(
            title="⚔ Ticket Claimed",
            description=f"""
Assigned Staff

{interaction.user.mention}

Status

🟢 Being handled
""",
            color=0x3B82F6
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
            description="""
Are you sure you want to close this ticket?

This action cannot be undone.
""",
            color=discord.Color.red()
        )

        await interaction.response.send_message(
            embed=embed,
            view=CloseConfirmView(),
            ephemeral=True
        )