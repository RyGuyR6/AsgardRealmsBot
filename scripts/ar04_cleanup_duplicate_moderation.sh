#!/usr/bin/env bash
set -e

python3 <<'PY'
from pathlib import Path

path = Path("cogs/moderation.py")
text = path.read_text()

marker = "    # -------------------------------------------------\n    # Shared hierarchy validation"

first = text.find(marker)
if first == -1:
    print("Couldn't find moderation marker.")
    raise SystemExit(1)

second = text.find(marker, first + 1)

if second == -1:
    print("No duplicate moderation block found. Nothing to do.")
    raise SystemExit(0)

text = text[:second].rstrip() + "\n"

path.write_text(text)
print("Removed duplicate moderation block.")
PY

python3 -m compileall .
echo
echo "Cleanup complete."
