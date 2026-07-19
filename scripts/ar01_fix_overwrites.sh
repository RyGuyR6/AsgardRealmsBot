#!/usr/bin/env bash
set -Eeuo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_ROOT"

echo "========================================="
echo " AsgardRealmsBot AR-01"
echo " Fix overwrites TypeError"
echo "========================================="

TARGET="utils/helpers.py"

if [[ ! -f "$TARGET" ]]; then
    echo "ERROR: $TARGET not found."
    exit 1
fi

BACKUP="${TARGET}.bak.$(date +%Y%m%d_%H%M%S)"
cp "$TARGET" "$BACKUP"

echo "Backup created: $BACKUP"

python3 <<'PY'
from pathlib import Path
import sys

path = Path("utils/helpers.py")
text = path.read_text(encoding="utf-8")

changed = False

if "overwrites = None" in text:
    text = text.replace("overwrites = None", "overwrites = {}", 1)
    changed = True

old = """    channel = await category.create_text_channel(
        channel_name,
        overwrites=overwrites
    )"""

new = """    if overwrites:
        channel = await category.create_text_channel(
            channel_name,
            overwrites=overwrites
        )
    else:
        channel = await category.create_text_channel(
            channel_name
        )"""

if old in text:
    text = text.replace(old, new, 1)
    changed = True

if not changed:
    print("ERROR: Expected code patterns were not found.")
    sys.exit(1)

path.write_text(text, encoding="utf-8")
print("Patch applied.")
PY

python3 -m py_compile "$TARGET"

echo
echo "========================================="
echo " AR-01 completed successfully"
echo "========================================="
echo "Restart the bot and test /setup."
