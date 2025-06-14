# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Running the Application
```bash
python main.py
```

### Installing Dependencies
```bash
pip install -r requirements.txt
```

### Required Dependencies
- PySide6 >= 6.5.0 (primary Qt framework)
- PyQt6 >= 6.5.0 (compatibility)
- watchdog >= 3.0.0 (file system monitoring)

## Architecture Overview

This is a PySide6-based desktop application that enhances Claude Code's prompt input functionality. The architecture follows a **layered MVC pattern** with signal-driven component communication.

### Core Architecture Layers

**Core Layer (`core/`)**:
- `SettingsManager`: Hierarchical JSON configuration with dot-notation access and auto-save
- `WorkspaceManager`: VSCode-like multi-project workspace management with file discovery
- `FileSearcher`: Implements `@filename` completion with relevance scoring for Claude Code integration

**UI Layer (`ui/`)**:
- `MainWindow`: Central orchestrator managing all components and menu system

**Widget Layer (`widgets/`)**:
- `PromptInputWidget`: Rich text editor with real-time file completion and thinking level integration
- `FileTreeWidget`: Hierarchical workspace browser with drag-drop support
- `ThinkingSelectorWidget`: 14-level thinking system for Claude Code prompts

### Key Design Patterns

**Signal-Slot Architecture**: Components communicate via Qt signals for loose coupling:
- `thinking_level_changed`: ThinkingSelectorWidget → MainWindow → PromptInputWidget
- `file_selected`/`file_double_clicked`: FileTreeWidget → MainWindow
- `generate_and_copy`: PromptInputWidget → MainWindow

**Configuration Management**: Two-tier system:
- `config/settings.json`: Application preferences, window geometry, UI settings
- `config/workspace.json`: Project folders and workspace configuration

### Claude Code Integration

The application generates prompts specifically formatted for Claude Code:
- **File paths**: Uses forward slashes and workspace-relative paths (`@relative/path/to/file.ext`)
- **Thinking levels**: Prepends recognized thinking commands (`think`, `ultrathink`, etc.)
- **Clipboard integration**: Auto-copies generated prompts for seamless pasting

### File Handling Architecture

**Path Normalization**: Converts Windows backslashes to forward slashes for Claude Code compatibility

**File Discovery**: 40+ supported file types with smart filtering:
- Programming languages: `.py`, `.cpp`, `.js`, `.ts`, `.rs`, `.go`, etc.
- Configuration: `.json`, `.yaml`, `.ini`, `.cfg`
- Documentation: `.md`, `.txt`
- Game development: `.ue`, `.umap`, `.uasset` (Unreal Engine)

**Performance Optimizations**:
- Lazy loading with depth limits
- 300ms debounced completion to prevent excessive searches
- Directory exclusion for build folders (`node_modules`, `__pycache__`, etc.)

### Settings System

Uses hierarchical dot-notation for configuration access:
```python
settings.get('window.width', 1200)
settings.set('ui.thinking_level', 'think harder')
```

Auto-saves every 30 seconds and persists window geometry, thinking levels, and workspace state.

### Theme System

The application features a dynamic theme system with three built-in themes:

**Theme Management**:
- `ui/style_themes.py`: Centralized theme management with ThemeManager class
- Multiple themes: Light, Dark, Cyberpunk
- Runtime theme switching without restart
- Theme preference persistence in settings

**Available Themes**:
- **Light Mode**: Clean, traditional light theme with blue accents
- **Dark Mode**: Modern dark theme with subtle colors
- **Cyberpunk**: Original neon-purple theme with cyberpunk aesthetics

**Usage**:
- Menu: `表示 → テーマ` to switch themes
- Themes auto-save to `config/settings.json`
- Custom themes can be added to ThemeManager class

### Internationalization

Built for mixed Japanese/English environments:
- UTF-8 encoding throughout
- Japanese UI labels with English technical terms
- Unicode-safe file handling with graceful error recovery

## Key Implementation Details

**File Completion Flow**:
1. User types `@` → triggers 300ms debounced timer
2. `FileSearcher.search_files_by_name()` queries workspace
3. Results ranked by relevance (exact match > filename start > path depth)
4. Selection converts to Claude Code-compatible relative path

**Thinking Level Integration**:
14 levels from basic "think" to "ultrathink" and "megathink", prepended to generated prompts for Claude Code processing.

**Error Handling**:
Graceful degradation for missing workspaces, permission errors, and file I/O failures without crashing the application.