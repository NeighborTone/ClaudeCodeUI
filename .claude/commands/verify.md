---
description: Verify code changes by running the PySide6 application
allowed-tools: Bash(python3:*), Bash(python:*)
---

Run the application to verify:
1. No import/compile errors
2. No runtime errors during startup
3. Clean log output (no warnings)

## Commands
- WSL: `LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 python3 main.py`
- Windows: `python main.py`

## Expected Result
Application window should appear without errors in console.
