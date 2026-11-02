#!/bin/sh
if ! python3 -c 'import sys; sys.exit(sys.version_info < (3, 9))' 2>/dev/null; then
    echo 'Install Python 3.9 or later, then run this script again.' >&2
    exit 1
fi
exec python3 "$(dirname "$0")/claude-templates.py" "$@"
