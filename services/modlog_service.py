import discord
from datetime import datetime

from embeds import make_embed


async def send(
    channel: discord.TextChannel | None,
    title: str,
    description: str,
):
    """
    Backwards-compatible helper.
    Existing code can continue calling:
        await modlog_service.send(...)
    """
    if channel is None:
        return

    embed = make_embed(title, description)
    embed.timestamp = datetime.utcnow()

    await channel.send(embed=embed)


async def log_action(
    *,
    channel: discord.TextChannel | None,
    action: str,
    moderator: discord.Member | discord.User,
    target: discord.Member | discord.User,
    reason: str | None = None,
    color: discord.Color = discord.Color.blurple(),
):
    """
    Rich moderation log helper.

    Example:

    await modlog_service.log_action(
        channel=log_channel,
        action="Warn",
        moderator=interaction.user,
        target=member,
        reason=reason
    )
    """

    if channel is None:
        return

    embed = discord.Embed(
        title=f"🛡 {action}",
        color=color,
        timestamp=datetime.utcnow(),
    )

    embed.add_field(
        name="Moderator",
        value=f"{moderator.mention}\n`{moderator.id}`",
        inline=True,
    )

    embed.add_field(
        name="Target",
        value=f"{target.mention}\n`{target.id}`",
        inline=True,
    )

    if reason:
        embed.add_field(
            name="Reason",
            value=reason,
            inline=False,
        )

    embed.set_footer(
        text="Asgard Realms Moderation"
    )

    await channel.send(embed=embed)
