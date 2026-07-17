# ============================================================
#                  ASGARD REALMS BOT
#                     cogs/tickets.py
# ============================================================

import discord

from embeds import make_embed

from views.ticket_views import TicketView

from services.ticket_service import create_ticket


# ============================================================
#              REGISTER TICKET COMMANDS
# ============================================================

def register(bot):


    @bot.tree.command(
        name="ticketpanel",
        description="Post the ticket support panel."
    )
    async def ticketpanel(
        interaction: discord.Interaction
    ):

        embed = make_embed(

            "⚔ Asgard Realms Support Center",

            """
Need assistance?

Choose an option below.

🎫 **General Support**

Questions, help, or gameplay issues.

🐞 **Bug Report**

Report bugs or exploits.

⚠️ **Player Report**

Report rule violations.

💳 **Purchase Support**

Store or donation assistance.

A staff member will assist you shortly.
"""

        )


        await interaction.response.send_message(

            embed=embed,

            view=TicketView()

        )