import discord
from discord import app_commands

from embeds import make_embed
from services import settings_service


def register(bot):

    @bot.tree.command(
        name="setup",
        description="View Asgard Realms configuration."
    )
    @app_commands.default_permissions(administrator=True)
    async def setup(interaction: discord.Interaction):

        settings = settings_service.get(interaction.guild.id)

        def channel(channel_id):
            return f"<#{channel_id}>" if channel_id else "❌ Not Configured"

        def role(role_id):
            return f"<@&{role_id}>" if role_id else "❌ Not Configured"

        embed = make_embed(
            "⚙️ Asgard Realms Setup",
            "Current server configuration"
        )

        embed.add_field(
            name="Welcome Channel",
            value=channel(settings["welcome_channel"]),
            inline=False
        )

        embed.add_field(
            name="Leave Channel",
            value=channel(settings["leave_channel"]),
            inline=False
        )

        embed.add_field(
            name="Moderation Logs",
            value=channel(settings["modlog_channel"]),
            inline=False
        )

        embed.add_field(
            name="Ticket Category",
            value=channel(settings["ticket_category"]),
            inline=False
        )

        embed.add_field(
            name="Ticket Log Channel",
            value=channel(settings["ticket_log_channel"]),
            inline=False
        )

        embed.add_field(
            name="Autorole",
            value=role(settings["autorole"]),
            inline=False
        )

        await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )
