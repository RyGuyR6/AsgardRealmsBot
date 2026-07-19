#!/usr/bin/env bash
set -e

python3 <<'PY'
from pathlib import Path

p = Path("cogs/moderation.py")
text = p.read_text()

if 'name="case"' in text:
    print("case command already exists.")
    raise SystemExit(0)

insert = '''

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

'''

marker = '\n\n    @bot.tree.command(\n        name="slowmode"'
idx = text.find(marker)

if idx == -1:
    print("Couldn't find insertion point.")
    raise SystemExit(1)

text = text[:idx] + insert + text[idx:]

p.write_text(text)

print("Added /case command.")
PY

python3 -m compileall .
