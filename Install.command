#!/bin/bash
# Finder opens executable .command files in Terminal.
cd "$(dirname "$0")" || exit 1
printf '%s\n' 'Install project instructions for Claude, Codex and Copilot'
if ! python3 -c 'import sys; sys.exit(sys.version_info < (3, 9))' 2>/dev/null; then
    echo 'Install Python 3.9 or later from https://www.python.org/downloads/macos/ and open this file again.'
    read -r -p 'Press Enter to close this window.'
    exit 1
fi
installer=setup.py
if [[ ! -f "$installer" ]]; then installer=claude-templates.py; fi
echo 'Select the project folder where you want to install the instructions.'
target=$(osascript -e 'POSIX path of (choose folder with prompt "Choose your project folder")') || exit 0
python3 "$installer" --target "$target"
status=$?
read -r -p 'Press Enter to finish.'
exit "$status"
