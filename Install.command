#!/bin/bash
# Finder opens executable .command files in Terminal.
cd "$(dirname "$0")" || exit 1
printf '%s\n' 'Установка правил для Claude, Codex и Copilot'
if ! python3 -c 'import sys; sys.exit(sys.version_info < (3, 9))' 2>/dev/null; then
    echo 'Установите Python 3.9 или новее с https://www.python.org/downloads/macos/ и снова откройте этот файл.'
    read -r -p 'Нажмите Enter, чтобы закрыть окно.'
    exit 1
fi
installer=setup.py
if [[ ! -f "$installer" ]]; then installer=claude-templates.py; fi
echo 'Выберите папку проекта, в который хотите установить правила.'
target=$(osascript -e 'POSIX path of (choose folder with prompt "Выберите папку вашего проекта")') || exit 0
python3 "$installer" --target "$target"
status=$?
read -r -p 'Нажмите Enter, чтобы завершить.'
exit "$status"
