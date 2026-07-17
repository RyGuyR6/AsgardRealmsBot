import discord
from datetime import datetime, timezone


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
            description="A support ticket has been closed.",
            color=discord.Color.red(),
            timestamp=datetime.now(timezone.utc)
        )

        embed.add_field(
            name="Ticket",
            value=f"`{ticket_channel.name}`",
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

        embed.add_field(
            name="Claimed By",
            value=claimed_by.mention if claimed_by else "*Unclaimed*",
            inline=True
        )

        if opened_at:

            if opened_at.tzinfo is not None:
                opened_at = opened_at.astimezone(timezone.utc).replace(tzinfo=None)

            duration = datetime.utcnow() - opened_at

            total = int(duration.total_seconds())

            days, rem = divmod(total, 86400)
            hours, rem = divmod(rem, 3600)
            minutes, seconds = divmod(rem, 60)

            if days:
                duration_text = f"{days}d {hours}h {minutes}m"
            elif hours:
                duration_text = f"{hours}h {minutes}m"
            else:
                duration_text = f"{minutes}m {seconds}s"

            embed.add_field(
                name="Duration",
                value=duration_text,
                inline=False
            )

        embed.set_footer(
            text="⚔ Odin Ticket System"
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