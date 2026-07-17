# ============================================================
#                  ASGARD REALMS BOT
#                     cogs/tickets.py
# ============================================================

import discord

from embeds import make_embed
from views.ticket_views import TicketView


# ============================================================
#              REGISTER TICKET COMMANDS
# ============================================================

def register(bot):

    @bot.tree.command(
        name="ticketpanel",
        description="Post the Odin support panel."
    )
    async def ticketpanel(
        interaction: discord.Interaction
    ):

        embed = make_embed(

            "⚔ Odin Support Center",

            """
# Welcome to Asgard Realms!

Need help? Choose the button below that best matches your issue.

━━━━━━━━━━━━━━━━━━━━━━

## 🎫 General Support
Questions about gameplay, commands, ranks, or anything server related.

## 🐞 Bug Reports
Found a bug, exploit, or broken feature?
Let us know so we can fix it.

## ⚠️ Player Reports
Report cheating, harassment, griefing, or rule violations.

## 💳 Store Support
Problems with purchases, ranks, donations, or the webstore.

━━━━━━━━━━━━━━━━━━━━━━

## 📋 Before Opening a Ticket

• One issue per ticket.

• Explain your issue clearly.

• Include screenshots if possible.

• Please be patient while waiting for staff.

━━━━━━━━━━━━━━━━━━━━━━

⏱ **Average Response Time**
**Usually within 15–30 minutes**

Thank you for supporting **Asgard Realms**!
"""

        )

        embed.set_thumbnail(
            url="https://cdn.discordapp.com/emojis/⚔️.png"
        )

        embed.add_field(
            name="🟢 Ticket Status",
            value="Support Team Online",
            inline=True
        )

        embed.add_field(
            name="🎟 Open Tickets",
            value="Unlimited",
            inline=True
        )

        embed.add_field(
            name="🤖 Powered By",
            value="Odin",
            inline=True
        )

        embed.set_footer(
            text="⚔ Asgard Realms • Odin Ticket System"
        )

        await interaction.response.send_message(
            embed=embed,
            view=TicketView()
        )