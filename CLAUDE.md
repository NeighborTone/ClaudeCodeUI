# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Running the Application (WSL Environment)
```bash
# Recommended: Use WSL Python
python3 main.py

# Alternative: Use system Python
python main.py
```

### Running the Application (Windows Environment)
```cmd
# Use Windows Python
python main.py

# Or with py launcher
py main.py
```

### Installing Dependencies
```bash
# WSL environment
pip3 install -r requirements.txt

# Windows environment
pip install -r requirements.txt
```

### WSL Environment Setup
For WSL environments, it's recommended to use the WSL Python installation rather than Windows Python:

1. **Install Python in WSL**:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip
   ```

2. **Install dependencies in WSL**:
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python3 main.py
   ```

### Path Handling
The application automatically handles path conversion between Windows and WSL formats:
- **Windows mode**: Uses forward slashes (/) for Claude Code compatibility
- **WSL mode**: Converts paths to /mnt/c format for WSL compatibility
- Path mode is automatically detected based on environment

### WSL Python Execution Issues & Solutions

If Claude Code cannot execute Python files from WSL environment, try these solutions:

#### Solution 1: Use WSL Python (Recommended)
```bash
# Install Python in WSL
sudo apt update
sudo apt install python3 python3-pip

# Install dependencies
pip3 install -r requirements.txt

# Run application
python3 main.py
```

#### Solution 2: Create a run script
The application can automatically create run scripts for WSL compatibility. Use the Python Helper utility:
```python
from core.python_helper import PythonHelper
script_path = PythonHelper.create_run_script('/path/to/main.py')
```

#### Solution 3: Use WSL command from Windows
If you need to run from Windows side, use wsl command:
```cmd
wsl python3 /mnt/c/Users/owner/Desktop/PythonTools/ClaudeCodeUI/main.py
```

#### Solution 4: Check Python executable
Use the built-in Python environment checker:
- Go to menu: `HelP → Python実行環境`
- Check available Python executables
- Choose the appropriate one for your environment

### Common WSL Issues

1. **Permission Issues**: Ensure proper file permissions in WSL
2. **Path Conversion**: Use forward slashes (/) for all paths
3. **Environment Variables**: Some environment variables may not be available
4. **Dependencies**: Install dependencies in the same environment where Python runs

### Required Dependencies
- PySide6 >= 6.5.0 (primary Qt framework)
- PyQt6 >= 6.5.0 (compatibility)
- watchdog >= 3.0.0 (file system monitoring)

### New Features (Latest Update)

#### File Preview System
- **Syntax Highlighting**: Supports Python, JavaScript/TypeScript, C/C++ with proper color coding
- **Large File Handling**: Files over 1MB are partially loaded to prevent performance issues
- **Binary File Detection**: Automatically detects and displays binary files in hex format
- **Image File Support**: Shows image file information and dimensions
- **Search Functionality**: Real-time search within file content with highlighting
- **Toggle Visibility**: Preview pane can be hidden/shown via View menu

#### UI Improvements
- **Three-Pane Layout**: File Tree | Preview | Prompt Input for better workflow
- **Enhanced Usability**: Updated placeholders and help text for new features
- **Responsive Design**: Proper splitter ratios and minimum width constraints

#### Code Architecture Improvements

##### Theme System Refactoring
- **Modular Theme Structure**: Themes are now separated into individual files in `ui/themes/` package
- **Base Theme Class**: `BaseTheme` abstract class provides consistent interface for all themes
- **Easy Theme Addition**: New themes can be added by creating a new file and registering it in `theme_manager.py`
- **Available Themes**: Light, Dark, Cyberpunk, Nordic (example of extensibility)
- **Backward Compatibility**: Old `ui/style_themes.py` still works for legacy code

##### File Preview Optimizations
- **5000 Line Limit**: Text files display up to 5000 lines for better performance
- **Smart Interruption**: Files over 10MB or binary files show "プレビューを中断しました" message
- **Better Error Handling**: Graceful fallback for unsupported file types
- **Performance**: Reduced memory usage for large files

##### Settings Persistence Enhancement
- **Theme Settings**: Selected theme is automatically saved and restored on restart
- **Preview Visibility**: Preview pane visibility state is saved in settings.json
- **Splitter Sizes**: Main splitter sizes are saved and restored for consistent layout
- **Comprehensive State**: Window geometry, thinking level, path mode, and all UI preferences persist
- **Auto-save**: Settings are automatically saved every 30 seconds and on application close

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
- `FileTreeWidget`: Hierarchical workspace browser
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