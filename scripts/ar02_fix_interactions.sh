#!/usr/bin/env bash
set -Eeuo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_ROOT"

echo "=========================================="
echo " AR-02 Discord Interaction Repair"
echo "=========================================="

FILES=(
    "cogs/server_setup.py"
    "cogs/tickets.py"
    "cogs/welcome.py"
)

for file in "${FILES[@]}"; do

    if [[ ! -f "$file" ]]; then
        echo "Skipping $file (not found)"
        continue
    fi

    cp "$file" "$file.bak.$(date +%Y%m%d_%H%M%S)"

done

python3 <<'PY'
from pathlib import Path
import re

FILES = [
    Path("cogs/server_setup.py"),
    Path("cogs/tickets.py"),
    Path("cogs/welcome.py"),
]

for path in FILES:

    if not path.exists():
        continue

    text = path.read_text(encoding="utf-8")
    original = text

    #
    # Add defer immediately after command definition
    #

    pattern = re.compile(
        r'(\)\s*:\n)(\s+)(?!await interaction\.response\.defer)',
        re.MULTILINE
    )

    def add_defer(match):
        indent = match.group(2)
        return (
            match.group(1)
            + indent
            + "await interaction.response.defer(ephemeral=True)\n"
            + indent
        )

    text = pattern.sub(add_defer, text, count=1)

    #
    # Replace response.send_message with followup.send
    #

    text = text.replace(
        "interaction.response.send_message(",
        "interaction.followup.send("
    )

    if text != original:
        path.write_text(text, encoding="utf-8")
        print(f"Updated {path}")

PY

echo
echo "Compiling..."

python3 -m compileall cogs

echo
echo "=========================================="
echo " AR-02 Complete"
echo "=========================================="

echo "Commit if compilation succeeds."