#!/usr/bin/env bash
set -Eeuo pipefail

FILES=(
    cogs/server_setup.py
    cogs/tickets.py
    cogs/welcome.py
)

for file in "${FILES[@]}"; do
    latest="$(ls -t "${file}".bak.* 2>/dev/null | head -1 || true)"

    if [[ -n "$latest" ]]; then
        cp "$latest" "$file"
        echo "Restored $file"
    else
        echo "No backup found for $file"
    fi
done

python3 -m compileall cogs

echo
echo "Restore complete."