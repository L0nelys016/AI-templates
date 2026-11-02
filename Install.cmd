@echo off
setlocal
py -3 -c "import sys; sys.exit(sys.version_info < (3, 9))" >nul 2>&1
if not errorlevel 1 (
    py -3 "%~dp0claude-templates.py" %*
    goto done
)
python -c "import sys; sys.exit(sys.version_info < (3, 9))" >nul 2>&1
if errorlevel 1 (
    echo Install Python 3.9 or later, then open this file again.
    pause
    exit /b 1
)
python "%~dp0claude-templates.py" %*
:done
set "result=%errorlevel%"
if "%~1"=="" pause
exit /b %result%
