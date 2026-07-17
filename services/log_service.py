import discord
from datetime import datetime


class TicketLogService:

    @staticmethod
    async def send_log(
        guild: discord.Guild,
        channel_name: str,
        ticket_channel: discord.TextChannel,
        creator: discord.Member,
        closer: discord.Member,
        transcript: discord.File | None = None,
        claimed_by: discord.Member | None = None,
        opened_at: datetime | None = None,
    ):

        log_channel = discord.utils.get(
            guild.text_channels,
            name=channel_name
        )

        if log_channel is None:
            return

        embed = discord.Embed(
            title="🎫 Ticket Closed",
            color=discord.Color.red(),
            timestamp=datetime.utcnow()
        )

        embed.add_field(
            name="Ticket",
            value=ticket_channel.name,
            inline=False
        )

        embed.add_field(
            name="Opened By",
            value=creator.mention,
            inline=True
        )

        embed.add_field(
            name="Closed By",
            value=closer.mention,
            inline=True
        )

        if claimed_by is not None:
            embed.add_field(
                name="Claimed By",
                value=claimed_by.mention,
                inline=True
            )

        if opened_at is not None:

            duration = datetime.utcnow() - opened_at

            hours, remainder = divmod(
                int(duration.total_seconds()),
                3600
            )

            minutes, seconds = divmod(
                remainder,
                60
            )

            embed.add_field(
                name="Duration",
                value=f"{hours}h {minutes}m {seconds}s",
                inline=False
            )

        embed.set_footer(
            text="Odin Ticket System"
        )

        if transcript:

            await log_channel.send(
                embed=embed,
                file=transcript
            )

        else:

            await log_channel.send(
                embed=embed
            )