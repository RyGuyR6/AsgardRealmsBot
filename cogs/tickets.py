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
Choose the support option that best matches your issue.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎫 **General Support**
Gameplay questions, commands, quests, ranks, or general assistance.

🐞 **Bug Reports**
Report bugs, exploits, glitches, or broken features.

⚠️ **Player Reports**
Report griefing, cheating, harassment, or rule violations.

💳 **Purchase Support**
Issues involving purchases, donations, store ranks, or the webstore.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### 📋 Before Opening a Ticket

• One issue per ticket.

• Explain your issue clearly.

• Include screenshots whenever possible.

• Please remain respectful to staff.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🟢 **Support Status**
Online

⏱ **Average Response Time**
Usually within **15–30 minutes**

Click one of the buttons below to create your support ticket.

⚔ May Odin guide your journey.
"""
        )

        # Load the banner image from the assets folder
        file = discord.File(
            "assets/odin_banner.PNG",
            filename="odin_banner.PNG"
        )

        # Display the banner at the top of the embed
        embed.set_image(
            url="attachment://odin_banner.PNG"
        )

        embed.add_field(
            name="🎟 Ticket System",
            value="Open 24/7",
            inline=True
        )

        embed.add_field(
            name="🛡 Staff Status",
            value="Ready to Assist",
            inline=True
        )

        embed.add_field(
            name="🤖 Powered By",
            value="Odin",
            inline=True
        )

        embed.set_footer(
            text="⚔ Asgard Realms • Guardian of the Nine Realms"
        )

        await interaction.response.send_message(
            embed=embed,
            view=TicketView(),
            file=file
        )