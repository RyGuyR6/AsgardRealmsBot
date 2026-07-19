#!/usr/bin/env bash
set -e

python3 <<'PY'
from pathlib import Path
import re

path = Path("cogs/moderation.py")
text = path.read_text()

old = """        warning_service.add_warning(
            interaction.guild.id,
            member.id,
            interaction.user.id,
            reason
        )
"""

new = """        warning_id, case_id = warning_service.add_warning(
            interaction.guild.id,
            member.id,
            interaction.user.id,
            reason
        )
"""

if old not in text:
    raise SystemExit("Couldn't locate add_warning() call.")

text = text.replace(old, new, 1)

old = """        embed.add_field(
            name="Total Warnings",
            value=str(total)
        )
"""

new = """        embed.add_field(
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
"""

if old not in text:
    raise SystemExit("Couldn't locate Total Warnings field.")

text = text.replace(old, new, 1)

path.write_text(text)
print("Updated /warn command.")
PY

python3 -m compileall .
echo
echo "AR04_003 complete."
