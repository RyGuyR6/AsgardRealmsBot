# ============================================================
#                  ASGARD REALMS BOT
#                services/ticket_service.py
# ============================================================

import json
import os

import discord

from config import SERVER_NAME
from views.ticket_views import TicketManageView


# ============================================================
#                  TICKET DATABASE
# ============================================================

TICKET_FILE = "data/ticket_counter.json"


def load_ticket_data():

    if not os.path.exists(TICKET_FILE):

        with open(TICKET_FILE, "w") as file:

            json.dump(
                {
                    "next_ticket": 1
                },
                file,
                indent=4
            )

    with open(TICKET_FILE, "r") as file:

        return json.load(file)


def save_ticket_data(data):

    with open(TICKET_FILE, "w") as file:

        json.dump(
            data,
            file,
            indent=4
        )


def get_next_ticket_number():

    data = load_ticket_data()

    number = data["next_ticket"]

    data["next_ticket"] += 1

    save_ticket_data(data)

    return number


# ============================================================
#                  FIND CATEGORY
# ============================================================

def get_ticket_category(guild):

    return discord.utils.get(
        guild.categories,
        name="🎫 TICKETS"
    )


# ============================================================
#                  CREATE TICKET
# ============================================================

async def create_ticket(
    interaction: discord.Interaction,
    ticket_type: str
):

    guild = interaction.guild
    user = interaction.user

    ticket_number = get_next_ticket_number()

    category = get_ticket_category(guild)

    if category is None:

        await interaction.response.send_message(
            "❌ Ticket category missing. Run /setup first.",
            ephemeral=True
        )

        return

    channel_name = f"ticket-{ticket_number:04}"

    overwrites = {

        guild.default_role:
            discord.PermissionOverwrite(
                view_channel=False
            ),

        user:
            discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True
            )

    }

    staff_roles = [

        "👑 Allfather",

        "🛡 Administrator",

        "⚔ Moderator"

    ]

    for role_name in staff_roles:

        role = discord.utils.get(
            guild.roles,
            name=role_name
        )

        if role:

            overwrites[role] = discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True
            )

    channel = await guild.create_text_channel(
        name=channel_name,
        category=category,
        overwrites=overwrites
    )

    embed = discord.Embed(
        title=f"⚔ Ticket #{ticket_number:04}",
        description=f"""
Welcome {user.mention}!

Your ticket has been created.

**Category**

{ticket_type}

A staff member will assist you shortly.

Thank you for supporting **{SERVER_NAME}**.
""",
        color=0x3B82F6
    )

    await channel.send(
        embed=embed,
        view=TicketManageView()
    )

    await interaction.response.send_message(
        f"✅ Your ticket has been created: {channel.mention}",
        ephemeral=True
    )

    return channel