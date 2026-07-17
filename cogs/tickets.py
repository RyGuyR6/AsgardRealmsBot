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

Need help? Select the option below that best matches your issue.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 🎫 General Support
Questions about gameplay, commands, ranks, quests, or anything server related.

## 🐞 Bug Reports
Found a bug or exploit?
Report it here so our developers can investigate.

## ⚠️ Player Reports
Report cheating, griefing, harassment, or rule violations.

## 💳 Purchase Support
Issues involving purchases, donations, ranks, or the webstore.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 📋 Before Opening a Ticket

⚔ One issue per ticket.

📸 Include screenshots whenever possible.

📝 Explain your issue clearly.

🤝 Please remain respectful to staff.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🟢 **Support Status**
Staff Available

⏱ **Average Response**
Usually within **15–30 minutes**

Thank you for supporting **Asgard Realms**.

May Odin guide your journey.
"""
        )

        file = discord.File(
            "assets/odin_logo.png",
            filename="odin_logo.png"
        )

        embed.set_thumbnail(
            url="attachment://odin_logo.png"
        )

        embed.set_footer(
            text="⚔ Asgard Realms • Powered by Odin"
        )

        await interaction.response.send_message(
            embed=embed,
            view=TicketView(),
            file=file
        )