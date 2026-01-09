---
name: verify
description: Verify code changes by running the PySide6 application
allowed-tools: Bash(python3:*), Bash(python:*), Read
---

# Verify Application

## Usage
```
/verify
```

## Description
Runs the PySide6 application to verify:
1. No import/compile errors
2. No runtime errors during startup
3. Application window launches successfully

## Environment Detection
- **WSL**: `LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 python3 main.py`
- **Windows**: `python main.py`

## Timeout
GUI applications are run with timeout (5-10 seconds) to verify startup only.

## Workflow
This skill invokes the `/verify` command which:
1. Detects environment (WSL/Windows)
2. Runs application with appropriate command
3. Reports startup status
