# ============================================================
#                  ASGARD REALMS BOT
#                services/ticket_service.py
# ============================================================

import json
import os
from datetime import datetime, UTC

import discord

from config import SERVER_NAME

TICKET_FILE = "data/ticket_counter.json"


def load_ticket_data():

    if not os.path.exists(TICKET_FILE):

        os.makedirs("data", exist_ok=True)

        with open(TICKET_FILE, "w") as file:

            json.dump(
                {
                    "next_ticket": 1,
                    "tickets": {}
                },
                file,
                indent=4
            )

    with open(TICKET_FILE, "r") as file:
        data = json.load(file)

    data.setdefault("next_ticket", 1)
    data.setdefault("tickets", {})

    return data


def save_ticket_data(data):

    with open(TICKET_FILE, "w") as file:
        json.dump(data, file, indent=4)


def get_next_ticket_number():

    data = load_ticket_data()

    number = data["next_ticket"]

    data["next_ticket"] += 1

    save_ticket_data(data)

    return number


def save_ticket_metadata(channel_id, creator_id, ticket_number, ticket_type):

    data = load_ticket_data()

    data["tickets"][str(channel_id)] = {
        "ticket_number": ticket_number,
        "creator": creator_id,
        "ticket_type": ticket_type,
        "claimed_by": None,
        "opened_at": datetime.now(UTC).isoformat()
    }

    save_ticket_data(data)


def get_ticket_metadata(channel_id):

    data = load_ticket_data()

    return data["tickets"].get(str(channel_id))


def update_ticket_metadata(channel_id, **updates):

    data = load_ticket_data()

    ticket = data["tickets"].get(str(channel_id))

    if ticket is None:
        return

    ticket.update(updates)

    save_ticket_data(data)


def remove_ticket_metadata(channel_id):

    data = load_ticket_data()

    data["tickets"].pop(str(channel_id), None)

    save_ticket_data(data)


def get_ticket_category(guild):

    return discord.utils.get(
        guild.categories,
        name="🎫 TICKETS"
    )


async def create_ticket(
    interaction: discord.Interaction,
    ticket_type: str
):

    # Import here to avoid circular imports
    from views.ticket_manage import TicketManageView

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
        guild.default_role: discord.PermissionOverwrite(
            view_channel=False
        ),
        user: discord.PermissionOverwrite(
            view_channel=True,
            send_messages=True,
            read_message_history=True
        )
    }

    for role_name in (
        "👑 Allfather",
        "🛡 Administrator",
        "⚔ Moderator",
    ):

        role = discord.utils.get(guild.roles, name=role_name)

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

    save_ticket_metadata(
        channel.id,
        user.id,
        ticket_number,
        ticket_type
    )

    embed = discord.Embed(
        title=f"⚔ Ticket #{ticket_number:04}",
        description=(
            f"Welcome {user.mention}!\n\n"
            f"**Category:** {ticket_type}\n\n"
            "A staff member will assist you shortly."
        ),
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