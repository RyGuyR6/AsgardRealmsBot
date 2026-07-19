#!/usr/bin/env bash
set -e

python3 <<'PY'
from pathlib import Path

path = Path("cogs/moderation.py")
text = path.read_text()

if 'name="cases"' in text:
    print("/cases already exists.")
    raise SystemExit(0)

insert = '''

    @bot.tree.command(
        name="cases",
        description="View a member's moderation history."
    )
    @app_commands.default_permissions(
        moderate_members=True
    )
    async def cases(
        interaction: discord.Interaction,
        member: discord.Member
    ):

        rows = warning_service.get_cases(member.id)

        if not rows:
            return await interaction.response.send_message(
                embed=make_embed(
                    "📁 Case History",
                    f"{member.mention} has no moderation cases."
                ),
                ephemeral=True
            )

        embed = make_embed(
            "📁 Moderation History",
            f"Showing the latest {min(len(rows),10)} cases for {member.mention}"
        )

        for case_id, action, moderator_id, reason, created in rows[:10]:

            reason = reason if len(reason) <= 50 else reason[:47] + "..."

            embed.add_field(
                name=f"Case #{case_id} • {action}",
                value=(
                    f"Moderator: `{moderator_id}`\\n"
                    f"Reason: {reason}\\n"
                    f"Date: {created}"
                ),
                inline=False
            )

        await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )

'''

marker = '''

    @bot.tree.command(
        name="slowmode"'''

idx = text.find(marker)

if idx == -1:
    raise SystemExit("Couldn't find insertion point before slowmode.")

text = text[:idx] + insert + text[idx:]

path.write_text(text)

print("Added /cases command.")
PY

python3 -m compileall .
