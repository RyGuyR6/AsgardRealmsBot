#!/usr/bin/env bash
set -Eeuo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_ROOT"

FILE="cogs/tickets.py"

echo "===================================="
echo " AR-02B Ticket Panel Repair"
echo "===================================="

if [[ ! -f "$FILE" ]]; then
    echo "ERROR: $FILE not found."
    exit 1
fi

cp "$FILE" "$FILE.bak.$(date +%Y%m%d_%H%M%S)"

python3 <<'PY'
from pathlib import Path
import sys

path = Path("cogs/tickets.py")
text = path.read_text(encoding="utf-8")

# Only replace the response call.
# Defer will be added manually in the next sprint if needed.
count = text.count("interaction.response.send_message(")

if count == 0:
    print("No interaction.response.send_message() calls found.")
    sys.exit(0)

text = text.replace(
    "interaction.response.send_message(",
    "interaction.followup.send("
)

path.write_text(text, encoding="utf-8")

print(f"Updated {count} response(s).")
PY

python3 -m py_compile "$FILE"

echo
echo "Ticket panel repaired successfully."