# Project Overview

## Description
PySide6-based desktop application for enhancing Claude Code's prompt input functionality.

## Tech Stack
- Language: Python 3.x
- Framework: PySide6 (Qt6)
- Fallback: PyQt6
- File Monitoring: watchdog

## Quick Start

### WSL Environment (Recommended)
```bash
pip3 install -r requirements.txt
python3 main.py
```

### Windows Environment (MUST use batch file)
```bash
pip install -r requirements.txt
run_claudeui.bat
```

### WSL Testing (English mode for font compatibility)
```bash
LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 python3 main.py
```

## Key Features
- SQLite-based high-performance indexing (90% faster startup)
- Smart file completion (@filename, !files, #folders)
- Multi-theme support (8 themes)
- Pre/post prompt templates
- Real-time token counting
