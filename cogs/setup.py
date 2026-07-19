import discord
from discord import app_commands

from embeds import make_embed
from services import settings_service


def register(bot):

    @bot.tree.command(
        name="setup",
        description="View the server setup status."
    )
    @app_commands.default_permissions(administrator=True)
    async def setup(interaction: discord.Interaction):

        settings = settings_service.get(interaction.guild.id)

        def value(v):
            return f"<#{v}>" if v else "❌ Not Configured"

        embed = make_embed(
            "⚙️ Asgard Realms Setup",
            "Server configuration overview"
        )

        embed.add_field(
            name="Welcome Channel",
            value=value(settings["welcome_channel"]),
            inline=False
        )

        embed.add_field(
            name="Leave Channel",
            value=value(settings["leave_channel"]),
            inline=False
        )

        embed.add_field(
            name="Moderation Logs",
            value=value(settings["modlog_channel"]),
            inline=False
        )

        embed.add_field(
            name="Ticket Category",
            value=value(settings["ticket_category"]),
            inline=False
        )

        embed.add_field(
            name="Ticket Log Channel",
            value=value(settings["ticket_log_channel"]),
            inline=False
        )

        embed.add_field(
            name="Autorole",
            value=f"<@&{settings['autorole']}>" if settings["autorole"] else "❌ Not Configured",
            inline=False
        )

        await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )
