#!/usr/bin/env bash
set -e

echo
echo "======================================"
echo "   ASGARD REALMS BOT RELEASE INSTALLER"
echo "======================================"
echo

python -m compileall .

echo
echo "✅ Installation Complete"
echo
echo "Next:"
echo "git add ."
echo 'git commit -m "Installed release"'
