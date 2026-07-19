#!/usr/bin/env bash
set -Eeuo pipefail

FILE="cogs/tickets.py"

cp "$FILE" "$FILE.bak.$(date +%Y%m%d_%H%M%S)"

python3 <<'PY'
from pathlib import Path

path = Path("cogs/tickets.py")
text = path.read_text(encoding="utf-8")

needle = "async def ticketpanel(interaction: discord.Interaction):"

# Add defer immediately after the async function definition if it's missing.
if needle in text and "await interaction.response.defer" not in text:
    text = text.replace(
        needle,
        needle + "\n\n        await interaction.response.defer(ephemeral=True)",
        1
    )

# If the followup.send call is missing its closing parenthesis, add it.
target = """await interaction.followup.send(
            embed=embed,
            file=file,
            view=TicketView()"""

replacement = """await interaction.followup.send(
            embed=embed,
            file=file,
            view=TicketView()
        )"""

if target in text:
    text = text.replace(target, replacement, 1)

path.write_text(text, encoding="utf-8")
print("Patched ticketpanel.")
PY

python3 -m py_compile "$FILE"

echo
echo "AR-02C completed successfully."
