import discord

from discord import app_commands

from embeds import make_embed
from services import warning_service
from services import modlog_service


def register(bot):

    warning_service.initialize()


    async def _modlog_channel(guild):

        for channel in guild.text_channels:
            if channel.name.lower() in (
                "mod-logs",
                "modlog",
                "moderation-log",
                "moderation-logs",
            ):
                return channel

        return None


    @bot.tree.command(
        name="warn",
        description="Warn a member."
    )
    @app_commands.default_permissions(
        moderate_members=True
    )
    async def warn(
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str
    ):

        if member.bot:
            return await interaction.response.send_message(
                embed=make_embed(
                    "⚠ Cannot Warn",
                    "Bots cannot receive warnings."
                ),
                ephemeral=True
            )

        if member == interaction.user:
            return await interaction.response.send_message(
                embed=make_embed(
                    "⚠ Invalid",
                    "You cannot warn yourself."
                ),
                ephemeral=True
            )

        warning_id, case_id = warning_service.add_warning(
            interaction.guild.id,
            member.id,
            interaction.user.id,
            reason
        )

        total = warning_service.warning_count(
            member.id
        )

        embed = make_embed(
            "⚔ Member Warned",
            f"{member.mention} has been warned."
        )

        embed.add_field(
            name="Reason",
            value=reason,
            inline=False
        )

        embed.add_field(
            name="Moderator",
            value=interaction.user.mention
        )

        embed.add_field(
            name="Total Warnings",
            value=str(total)
        )

        embed.add_field(
            name="Warning ID",
            value=f"#{warning_id}",
            inline=True
        )

        embed.add_field(
            name="Case ID",
            value=f"#{case_id}",
            inline=True
        )

        await interaction.response.send_message(
            embed=embed
        )

        await modlog_service.log_action(
            channel=await _modlog_channel(interaction.guild),
            action="Timeout",
            moderator=interaction.user,
            target=member,
            reason=reason,
            color=discord.Color.gold(),
        )

        await modlog_service.log_action(
            channel=await _modlog_channel(interaction.guild),
            action="Ban",
            moderator=interaction.user,
            target=member,
            reason=reason,
            color=discord.Color.dark_red(),
        )

        await modlog_service.log_action(
            channel=await _modlog_channel(interaction.guild),
            action="Kick",
            moderator=interaction.user,
            target=member,
            reason=reason,
            color=discord.Color.red(),
        )

        await modlog_service.log_action(
            channel=await _modlog_channel(interaction.guild),
            action="Warn",
            moderator=interaction.user,
            target=member,
            reason=reason,
            color=discord.Color.orange(),
        )


    @bot.tree.command(
        name="warnings",
        description="View member warnings."
    )
    async def warnings(
        interaction: discord.Interaction,
        member: discord.Member
    ):

        rows = warning_service.get_warnings(
            member.id
        )

        if not rows:

            return await interaction.response.send_message(
                embed=make_embed(
                    "📖 Warning History",
                    f"{member.mention} has no warnings."
                )
            )

        embed = make_embed(
            "📖 Warning History",
            member.mention
        )

        for warning_id, moderator, reason, created in rows:

            embed.add_field(
                name=f"Warning #{warning_id}",
                value=(
                    f"Reason: {reason}\n"
                    f"Moderator ID: {moderator}\n"
                    f"Date: {created}"
                ),
                inline=False
            )

        await interaction.response.send_message(
            embed=embed
        )


    @bot.tree.command(
        name="clearwarnings",
        description="Remove every warning from a member."
    )
    @app_commands.default_permissions(
        moderate_members=True
    )
    async def clearwarnings(
        interaction: discord.Interaction,
        member: discord.Member
    ):

        warning_service.clear_warnings(
            member.id
        )

        embed = make_embed(
            "🛡 Warnings Cleared",
            f"All warnings removed from {member.mention}"
        )

        await interaction.response.send_message(
            embed=embed
        )


    # -------------------------------------------------
    # Shared hierarchy validation
    # -------------------------------------------------

    def _can_moderate(actor: discord.Member,
                      target: discord.Member):

        if actor == target:
            return False, "You cannot moderate yourself."

        if target.guild.owner == target:
            return False, "You cannot moderate the server owner."

        if actor.guild.owner == actor:
            return True, None

        if actor.top_role <= target.top_role:
            return False, (
                "Target has an equal or higher role."
            )

        return True, None


    @bot.tree.command(
        name="kick",
        description="Kick a member."
    )
    @app_commands.default_permissions(
        kick_members=True
    )
    async def kick(
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str="No reason provided"
    ):

        ok,msg = _can_moderate(
            interaction.user,
            member
        )

        if not ok:
            return await interaction.response.send_message(
                embed=make_embed(
                    "⚠ Kick Failed",
                    msg
                ),
                ephemeral=True
            )

        try:
            await member.send(
                f"You were kicked from "
                f"{interaction.guild.name}\n\n"
                f"Reason: {reason}"
            )
        except Exception:
            pass

        await member.kick(reason=reason)

        embed = make_embed(
            "⚔ Member Kicked",
            f"{member.mention} has been kicked."
        )

        embed.add_field(
            name="Moderator",
            value=interaction.user.mention
        )

        embed.add_field(
            name="Reason",
            value=reason,
            inline=False
        )

        await interaction.response.send_message(
            embed=embed
        )


    @bot.tree.command(
        name="ban",
        description="Ban a member."
    )
    @app_commands.default_permissions(
        ban_members=True
    )
    async def ban(
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str="No reason provided"
    ):

        ok,msg = _can_moderate(
            interaction.user,
            member
        )

        if not ok:
            return await interaction.response.send_message(
                embed=make_embed(
                    "⚠ Ban Failed",
                    msg
                ),
                ephemeral=True
            )

        try:
            await member.send(
                f"You were banned from "
                f"{interaction.guild.name}\n\n"
                f"Reason: {reason}"
            )
        except Exception:
            pass

        await member.ban(reason=reason)

        embed = make_embed(
            "🛡 Member Banned",
            f"{member.mention} has been banned."
        )

        embed.add_field(
            name="Moderator",
            value=interaction.user.mention
        )

        embed.add_field(
            name="Reason",
            value=reason,
            inline=False
        )

        await interaction.response.send_message(
            embed=embed
        )


    @bot.tree.command(
        name="timeout",
        description="Timeout a member."
    )
    @app_commands.default_permissions(
        moderate_members=True
    )
    async def timeout(
        interaction: discord.Interaction,
        member: discord.Member,
        minutes: int,
        reason: str="No reason provided"
    ):

        ok,msg = _can_moderate(
            interaction.user,
            member
        )

        if not ok:
            return await interaction.response.send_message(
                embed=make_embed(
                    "⚠ Timeout Failed",
                    msg
                ),
                ephemeral=True
            )

        from datetime import timedelta

        await member.timeout(
            timedelta(minutes=minutes),
            reason=reason
        )

        embed = make_embed(
            "⚔ Member Timed Out",
            f"{member.mention} has been timed out."
        )

        embed.add_field(
            name="Duration",
            value=f"{minutes} minute(s)"
        )

        embed.add_field(
            name="Reason",
            value=reason,
            inline=False
        )

        embed.add_field(
            name="Moderator",
            value=interaction.user.mention
        )

        await interaction.response.send_message(
            embed=embed
        )


    ###########################################################
    # CHANNEL TOOLS
    ###########################################################

    @bot.tree.command(
        name="purge",
        description="Delete messages."
    )
    @app_commands.default_permissions(
        manage_messages=True
    )
    async def purge(
        interaction: discord.Interaction,
        amount: app_commands.Range[int,1,500]
    ):

        await interaction.response.defer(
            ephemeral=True
        )

        deleted = await interaction.channel.purge(
            limit=amount
        )

        embed = make_embed(
            "🧹 Messages Purged",
            f"Deleted **{len(deleted)}** messages."
        )

        await interaction.followup.send(
            embed=embed,
            ephemeral=True
        )


    @bot.tree.command(
        name="lock",
        description="Lock this channel."
    )
    @app_commands.default_permissions(
        manage_channels=True
    )
    async def lock(
        interaction: discord.Interaction
    ):

        overwrite = interaction.channel.overwrites_for(
            interaction.guild.default_role
        )

        overwrite.send_messages = False

        await interaction.channel.set_permissions(
            interaction.guild.default_role,
            overwrite=overwrite
        )

        embed = make_embed(
            "🔒 Channel Locked",
            f"{interaction.channel.mention} is now locked."
        )

        await interaction.response.send_message(
            embed=embed
        )


    @bot.tree.command(
        name="unlock",
        description="Unlock this channel."
    )
    @app_commands.default_permissions(
        manage_channels=True
    )
    async def unlock(
        interaction: discord.Interaction
    ):

        overwrite = interaction.channel.overwrites_for(
            interaction.guild.default_role
        )

        overwrite.send_messages = None

        await interaction.channel.set_permissions(
            interaction.guild.default_role,
            overwrite=overwrite
        )

        embed = make_embed(
            "🔓 Channel Unlocked",
            f"{interaction.channel.mention} is now unlocked."
        )

        await interaction.response.send_message(
            embed=embed
        )


    @bot.tree.command(
        name="case",
        description="View a moderation case."
    )
    @app_commands.default_permissions(
        moderate_members=True
    )
    async def case(
        interaction: discord.Interaction,
        case_id: int
    ):

        row = warning_service.get_case(case_id)

        if row is None:
            return await interaction.response.send_message(
                embed=make_embed(
                    "❌ Case Not Found",
                    f"No moderation case with ID **{case_id}** exists."
                ),
                ephemeral=True
            )

        cid,guild_id,action,moderator,user,reason,created = row

        embed = make_embed(
            f"📁 Case #{cid}",
            action
        )

        embed.add_field(
            name="User ID",
            value=str(user),
            inline=True
        )

        embed.add_field(
            name="Moderator ID",
            value=str(moderator),
            inline=True
        )

        embed.add_field(
            name="Reason",
            value=reason,
            inline=False
        )

        embed.add_field(
            name="Created",
            value=created,
            inline=False
        )

        await interaction.response.send_message(
            embed=embed
        )



    @bot.tree.command(
        name="slowmode",
        description="Set slowmode."
    )
    @app_commands.default_permissions(
        manage_channels=True
    )
    async def slowmode(
        interaction: discord.Interaction,
        seconds: app_commands.Range[int,0,21600]
    ):

        await interaction.channel.edit(
            slowmode_delay=seconds
        )

        embed = make_embed(
            "⏳ Slowmode Updated",
            f"Slowmode set to **{seconds} seconds**."
        )

        await interaction.response.send_message(
            embed=embed
        )
