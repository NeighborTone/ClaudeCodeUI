# CLAUDE.md

This file provides comprehensive guidance for Claude Code when working with this repository. The project is a sophisticated PySide6-based desktop application designed to enhance Claude Code's prompt input functionality.

## High-Performance SQLite Indexing System

This application features a **state-of-the-art SQLite-based indexing system** that dramatically improves startup time and search performance:

### Performance Improvements
- **90% faster startup**: Cold start time reduced from ~30 seconds to ~3 seconds for large projects
- **10x faster search**: Average search time reduced from ~100ms to ~1ms  
- **Efficient storage**: SQLite database with FTS5 provides compact, fast storage
- **Instant availability**: No Trie reconstruction needed - ready to search immediately after startup

### Key Features
- **Automatic system detection**: Chooses optimal indexing system based on project size
- **Background indexing**: Updates happen in background without blocking UI
- **Smart caching**: LRU cache with TTL for frequently accessed searches
- **Fuzzy search**: Advanced search capabilities with partial matching
- **Real-time completion**: Enhanced @filename completion with instant suggestions

## Core Principles

### 1. Communication Guidelines

⚠️ **ABSOLUTE RULES - MUST BE FOLLOWED:**

| Principle | Description |
|-----------|-------------|
| **🔒 MANDATORY COMPLIANCE** | These rules are the highest priority commands and MUST be followed absolutely without distortion or reinterpretation |
| **Clarify First** | Say "I don't understand" and ask questions instead of guessing |
| **No Assumptions** | Always confirm intent before proceeding |
| **Never Answer Uncertainly** | If unclear about something, don't answer - ask for clarification instead |
| **Question Before Execution** | Always ask clarifying questions before executing tasks to resolve any doubts |
| **Objective Only** | Avoid subjective opinions, excessive praise, unnecessary opinion expression, personal preferences/judgments, and excessive apologies or overly polite expressions |
| **Search When Needed** | Use web search for additional context |
| **Structured Questioning** | When facing ambiguous requests, ask specific clarifying questions |

### 2. Development Quality Assurance Rules

⚠️ **MANDATORY QUALITY REQUIREMENTS:**

| Rule | Implementation |
|------|----------------|
| **Always Test First** | Execute tests and verify functionality before completing any task |
| **Verify Runtime Behavior** | Check for runtime errors and handle them appropriately |
| **Log and Monitor** | Write diagnostic logs during testing to ensure proper operation |
| **Clarify Before Implementing** | Ask for clarification on unclear requirements - never guess |
| **Verify Before Completion** | Always verify implementation works as expected before marking complete |
| **Follow Existing Patterns** | Study and maintain consistency with existing code patterns and architecture |
| **Implement Only What's Requested** | Build exactly what is asked for, nothing more, nothing less |
| **Utilize Existing Resources** | Use existing files, functions, and patterns whenever possible |
| **Research When Needed** | Use web search for additional context when encountering unfamiliar concepts |

#### Ambiguity Resolution Protocol

When receiving unclear instructions, ALWAYS follow this questioning pattern:

1. **What** - Identify the specific subject/object of the request
2. **Where** - Clarify the location, file, or context 
3. **How** - Determine the method, approach, or level of detail required

### 3. Language Requirements

| Context | Language | Reason |
|---------|----------|---------|
| **CLAUDE.md** | English | Optimizes Claude processing |
| **User Communication** | Japanese | User preference (ALWAYS) |
| **Code** | English | Industry standard |
| **Code Comments** | Japanese | Team readability |
| **Documentation** | Japanese | Team usage |
| **Log Error Messages** | English | Debugging |
| **User-facing Messages** | Japanese | End users |

### 4. Implementation Philosophy

```
NO UNNECESSARY:
├── Complexity     # Keep solutions simple
├── Extensibility  # Only what's needed now
└── Features       # Exactly what's requested
```


## Development Commands

### Running the Application

#### WSL Environment (Recommended)
```bash
# Navigate to the project root directory
# (Already in ClaudeCodeUI root)

# Use WSL Python (recommended)
python3 main.py

# Alternative with system python
python main.py
```

#### Windows Environment
```cmd
# Navigate to the project root directory
# (Already in ClaudeCodeUI root)

# Use Windows Python
python main.py

# Or with py launcher
py main.py
```

### Dependency Management

#### Installing Dependencies
```bash
# WSL environment (recommended)
pip3 install -r requirements.txt

# Windows environment
pip install -r requirements.txt
```

#### Core Dependencies
- **PySide6 >= 6.5.0** (primary Qt framework)
- **PyQt6 >= 6.5.0** (compatibility fallback)
- **watchdog >= 3.0.0** (file system monitoring)

### Development Environment Setup

#### WSL Setup (Recommended)
```bash
# 1. Install Python in WSL
sudo apt update
sudo apt install python3 python3-pip

# 2. Install dependencies
pip3 install -r requirements.txt

# 3. Run application
python3 main.py
```

#### WSL Testing Environment
**IMPORTANT**: When testing in WSL environment, always use English language mode due to font compatibility limitations:

```bash
# Force English mode for WSL testing
LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 python3 main.py
```

**Reasoning**: WSL environment may not have proper Japanese font support, causing display issues. English mode ensures reliable testing and debugging.

#### Troubleshooting Python Execution in WSL

##### Solution 1: Use WSL Python (Recommended)
```bash
# Install Python in WSL environment
sudo apt update
sudo apt install python3 python3-pip

# Install dependencies in WSL
pip3 install -r requirements.txt

# Run from WSL
python3 main.py
```

##### Solution 2: WSL Command from Windows
```cmd
# Execute via WSL from Windows command line
wsl python3 /mnt/c/Users/owner/Desktop/PythonTools/ClaudeCodeUI/main.py
```

##### Solution 3: Python Environment Checker
The application includes a built-in Python environment checker:
- Menu: `Help → Python実行環境` 
- Shows available Python executables
- Helps select appropriate environment

### Path Handling & Environment Detection

The application automatically handles cross-platform compatibility:
- **Windows mode**: Uses forward slashes (/) for Claude Code compatibility
- **WSL mode**: Converts paths to /mnt/c format automatically
- **Auto-detection**: Environment is detected automatically at runtime
- **Manual override**: Available via settings if needed

## Project Architecture

This application follows a **layered MVC architecture** with signal-driven component communication and modular design principles.

### New High-Performance Indexing Architecture

The application now features a **dual-system indexing architecture** that automatically selects the optimal indexing system:

#### SQLite-Based System (Default)
- **SQLiteIndexer**: High-performance database with FTS5 full-text search
- **FastSQLiteSearcher**: Advanced search capabilities with caching
- **SQLiteIndexingWorker**: Background indexing with progress tracking
- **StartupOptimizer**: Intelligent startup optimization and background processing

#### Legacy Trie System (Fallback)
- **FileIndexer**: Original JSON-based Trie indexing system
- **FastFileSearcher**: Traditional in-memory search implementation
- **IndexingWorker**: Original indexing worker implementation

#### Integration Layer
- **IndexingAdapter**: Seamless integration between old and new systems
- **AdaptiveFileSearcher**: Unified interface maintaining backward compatibility

### Directory Structure

#### Application Directory Organization
The application follows a clear separation between application data and user-specific data:

```
ClaudeCodeUI/
├── src/                    # Source code directory
│   ├── core/              # Core business logic
│   ├── ui/                # User interface components
│   └── widgets/           # Specialized UI widgets
├── data/                   # Application data (committed to version control)
│   └── locales/           # Localization files
│       └── strings.json   # UI strings for all supported languages
├── saved/                  # User-specific data (NOT committed to version control)
│   ├── settings.json      # User preferences and application state
│   ├── workspace.json     # User's workspace configuration
│   └── file_index.db*     # SQLite index database files
├── templates/              # Prompt templates
│   ├── pre/               # Pre-prompt templates
│   └── post/              # Post-prompt templates
├── assets/                 # Application assets
│   └── icons/             # Icon files for themes and UI
└── main.py                 # Application entry point
```

##### Important Directory Distinctions
- **`data/` directory**: Contains application data that is part of the codebase
  - Includes localization files and other application resources
  - Should be committed to version control
  - Read-only during normal application operation

- **`saved/` directory**: Contains user-specific configuration and state
  - Created automatically on first run
  - Contains settings.json (user preferences) and workspace.json (workspace state)
  - Should NOT be committed to version control (add to .gitignore)
  - Modified during application usage to persist user choices

### Architecture Layers

#### Core Layer (`src/core/`)
**Central business logic and system management**

**High-Performance Indexing System:**
- `SQLiteIndexer` - High-performance SQLite database with FTS5 full-text search capabilities
- `FastSQLiteSearcher` - Advanced search system with LRU caching and fuzzy search
- `SQLiteIndexingWorker` - Background indexing worker with progress tracking and optimization
- `SQLitePersistentConnection` - Efficient database connection management with connection pooling
- `StartupOptimizer` - Intelligent startup optimization with background processing
- `IndexingAdapter` - Seamless integration layer for old/new system compatibility

**System Management Components:**
- `SettingsManager` - Hierarchical JSON configuration with dot-notation access and auto-save
- `WorkspaceManager` - VSCode-like multi-project workspace management with file discovery
- `FileSearcher` - Original Trie-based `@filename` completion with relevance scoring
- `TemplateManager` - Pre/post prompt template management system with JSON-based storage
- `TokenCounter` - Intelligent token estimation for Japanese/English mixed content
- `PromptHistoryManager` - Manages prompt history with search and persistence capabilities

**Internationalization & Environment:**
- `LocalizationManager` - Language management with strings loaded from `data/locales/strings.json`
- `LanguageManager` - Dynamic language switching and preference management
- `UIStrings` - Internationalized string management for UI components
- `EnvironmentDetector` - Windows/WSL environment detection and path conversion
- `PathConverter` - Cross-platform path normalization for Claude Code compatibility
- `PythonHelper` - Python execution environment assistance and script generation

**Utilities:**
- `Logger` - Application-wide logging system with multiple output levels

#### UI Layer (`src/ui/`)
**Main application interface and orchestration**

- `MainWindow` - Central orchestrator managing all components, menu system, and application state
- `style.py` - Global style management and application-wide theming
- `style_themes.py` - Theme-specific style definitions and customizations
- `themes/` - Modular theme system with pluggable theme architecture
  - `ThemeManager` - Dynamic theme registration and switching system
  - `BaseTheme` - Abstract base class for all themes
  - **Available Themes**: Light, Dark, Cyberpunk, Nordic, Electric, Material, Retro, Sci-Fi

#### Widget Layer (`src/widgets/`)
**Specialized UI components with specific functionality**

- `PromptInputWidget` - Rich text editor with real-time file completion and thinking level integration
- `FileTreeWidget` - Hierarchical workspace browser with file type filtering and async loading
- `FileTreeWorker` - Background worker for asynchronous file tree operations
- `ThinkingSelectorWidget` - 14-level thinking system for Claude Code prompts
- `TemplateSelector` - Pre/post prompt template selection and management interface
- `PromptPreviewWidget` - Real-time final prompt preview with syntax highlighting
- `PromptHistory` - Prompt history management and search interface

### Key Design Patterns

#### Signal-Slot Architecture
Components communicate via Qt signals for loose coupling and maintainability:

```python
# Example signal flows
thinking_level_changed: ThinkingSelectorWidget → MainWindow → PromptInputWidget
template_changed: TemplateSelector → MainWindow → PromptPreviewWidget
file_selected: FileTreeWidget → MainWindow → PromptInputWidget
generate_and_copy: PromptInputWidget → MainWindow (clipboard integration)
```

#### Configuration Management
Two-tier hierarchical configuration system:

```python
# Application settings
settings.get('window.width', 1200)
settings.set('ui.thinking_level', 'think harder')
settings.set('theme.current', 'dark')

# Workspace configuration  
workspace.add_folder('/path/to/project')
workspace.get_recent_files()
```

#### Template System Architecture
JSON-based template management with pre/post prompt support:

```json
{
  "title": "Bug Analysis Template",
  "content": "Analyze the following bug systematically..."
}
```

### Claude Code Integration Features

#### File Path Handling
- **Relative paths**: Converts absolute paths to workspace-relative format
- **Forward slash normalization**: Ensures Claude Code compatibility across platforms
- **@ file completion**: Implements Claude Code's @filename syntax with intelligent completion

#### Thinking Level Integration
14-level thinking system mapped to Claude Code commands:
- `think` (basic) → `ultrathink` (maximum)
- Automatic prepending to generated prompts
- Contextual level selection based on task complexity

#### Token Counting System
Intelligent token estimation for prompt optimization:
```python
# Japanese/English mixed content support
japanese_tokens = japanese_chars / 2.5  # Japanese character ratio
english_tokens = english_chars / 4.0    # English character ratio
special_handling = urls + code_blocks    # Additional token overhead
```

### Theme System Architecture

#### Modular Theme Structure
**Location**: `src/ui/themes/`

- `BaseTheme` - Abstract base class defining theme interface
- `LightTheme` - Clean, traditional light theme with blue accents
- `DarkTheme` - Modern dark theme with subtle color palette
- `CyberpunkTheme` - Original neon-purple theme with cyberpunk aesthetics
- `NordicTheme` - Minimalist Nordic-inspired theme with neutral colors
- `ElectricTheme` - High-contrast electric theme with bright accents
- `MaterialTheme` - Google Material Design inspired theme
- `RetroTheme` - Vintage retro theme with warm color palette
- `SciFiTheme` - Futuristic sci-fi theme with cool tones
- `ThemeManager` - Dynamic theme switching and registration system

#### Theme Implementation Pattern
```python
class CustomTheme(BaseTheme):
    def get_display_name(self) -> str:
        return "Custom Theme"
    
    def get_styles(self) -> str:
        return """
        QMainWindow { background-color: #custom; }
        /* ... theme-specific styles ... */
        """
```

#### Runtime Theme Switching
- No application restart required
- Settings persistence in `saved/settings.json` (user-specific, not in version control)
- Theme preference restoration on startup

### Template Management System

#### Template Types
- **Pre-prompts**: Task initialization templates (Claude Code Best Practice, Sample templates)
- **Post-prompts**: Additional instruction templates (Sample templates, expandable system)

#### Template Storage Structure
```
templates/
├── pre/                    # Pre-prompt templates
│   ├── ClaudeCodeBestPractice.json
│   └── Sample_Pre.json
└── post/                   # Post-prompt templates
    └── Sample_Post.json
```

#### Template Format
```json
{
  "title": "Human-readable template name",
  "content": "Template content with placeholders and instructions..."
}
```

### File Discovery & Filtering System

#### Supported File Types (40+ formats)
**Programming Languages**: `.py`, `.cpp`, `.h`, `.hpp`, `.js`, `.ts`, `.jsx`, `.tsx`, `.cs`, `.java`, `.php`, `.go`, `.rs`, `.swift`, `.kt`

**Configuration Files**: `.json`, `.yaml`, `.yml`, `.xml`, `.ini`, `.cfg`, `.config`, `.toml`

**Documentation**: `.md`, `.txt`, `.csv`, `.rst`

**Game Development**: `.ue`, `.umap`, `.uasset` (Unreal Engine)

**Web Development**: `.html`, `.css`, `.vue`, `.scss`, `.sass`

#### Performance Optimizations
- **Lazy loading**: Files loaded on-demand with depth limits
- **Directory exclusion**: Automatic exclusion of build folders (`node_modules`, `__pycache__`, `.git`, etc.)
- **Debounced completion**: 300ms delay prevents excessive file searches
- **Relevance scoring**: Intelligent ranking (exact match > filename start > path depth)

### Internationalization Architecture

#### Language Support
- **Primary languages**: Japanese, English
- **Auto-detection**: Based on system locale and environment
- **Manual switching**: Via application menu or settings
- **Mixed content**: Japanese UI with English technical terms

#### Implementation Details
```python
# Language detection flow
EnvironmentDetector.get_recommended_language() → LanguageManager.set_language()
→ UIStrings.tr(key) → Localized string output
```

#### String Management
- Centralized in `core/ui_strings.py`
- String definitions stored in `data/locales/strings.json`
- Dot-notation key access: `tr("label.thinking_level")`
- Fallback to English for missing translations

### Configuration System

#### Settings Hierarchy
```json
{
  "window": {
    "width": 1200,
    "height": 800,
    "geometry": "..."
  },
  "ui": {
    "theme": "cyberpunk",
    "language": "ja",
    "thinking_level": "think harder",
    "preview_visible": true
  },
  "workspace": {
    "recent_folders": [],
    "file_filters": []
  }
}
```

#### Auto-save Features
- **Interval saving**: Every 30 seconds
- **Application close**: Final save on exit
- **State restoration**: Window geometry, UI preferences, workspace state

### Error Handling & Resilience

#### Graceful Degradation
- **Missing workspaces**: Application continues with empty workspace
- **File permission errors**: Shows warning, continues operation
- **Theme loading failures**: Falls back to default theme
- **Template loading errors**: Uses built-in defaults

#### Cross-platform Compatibility
- **Path handling**: Automatic Windows/WSL path conversion
- **Font selection**: Platform-appropriate font fallbacks (Consolas → Courier New)
- **Environment detection**: Automatic platform detection and optimization

## Development Workflow Integration

### File Completion Flow
1. User types `@` in prompt input
2. 300ms debounced timer triggers file search
3. `FileSearcher.search_files_by_name()` queries workspace files
4. Results ranked by relevance scoring algorithm
5. Selection converts to Claude Code-compatible relative path format
6. File content automatically included in prompt

### Prompt Generation Pipeline
1. **Template selection**: Pre-prompt template applied
2. **Thinking level**: Thinking command prepended
3. **Main content**: User input with @file expansions
4. **Post-template**: Additional instructions appended
5. **Token counting**: Real-time token estimation
6. **Preview generation**: Real-time final prompt preview
7. **Clipboard output**: Formatted for Claude Code paste

### Template Development Workflow
1. Create JSON template file in `templates/pre/` or `templates/post/`
2. Define title and content structure
3. Use placeholder syntax for dynamic content
4. Test via template selector interface
5. Template automatically available in dropdown

## Troubleshooting Guide

### Common Issues & Solutions

#### WSL Python Execution Problems
```bash
# Verify Python installation
python3 --version
which python3

# Check environment variables
echo $PATH

# Reinstall dependencies if needed
pip3 uninstall PySide6 PyQt6 -y
pip3 install -r ClaudeCodeUI/requirements.txt
```

#### File Discovery Issues
1. **Workspace not added**: Use "Add Folder" button or Ctrl+O
2. **File type not supported**: Check supported extensions list
3. **Permission errors**: Ensure read access to workspace folders
4. **Refresh needed**: Press F5 to refresh file tree

#### Theme Loading Problems
1. **Theme file corruption**: Check `ui/themes/` for valid Python files
2. **Missing theme**: Falls back to default cyberpunk theme
3. **Style conflicts**: Clear `saved/settings.json` theme section

#### Template Loading Issues
1. **Invalid JSON**: Validate template JSON syntax
2. **Missing title/content**: Ensure required fields present
3. **File permissions**: Check read access to `templates/` directory

### Performance Optimization

#### Large Workspace Handling
- Use `.gitignore`-style patterns to exclude build directories
- Limit workspace depth to reasonable levels
- Consider splitting very large projects into multiple workspaces

#### Memory Management
- Application auto-manages file loading with size limits
- Large files (>1MB) are handled with partial loading
- Preview system includes memory-conscious rendering

## Testing & Quality Assurance

### Manual Testing Checklist
1. **Application startup**: Verify clean startup without errors
2. **Workspace management**: Add/remove folders, file tree updates
3. **File completion**: Test @filename completion accuracy
4. **Template system**: Verify pre/post template loading and application
5. **Theme switching**: Test all themes for visual consistency
6. **Token counting**: Verify reasonable token estimates
7. **Language switching**: Test Japanese/English UI updates
8. **Settings persistence**: Verify settings save/restore across restarts

### Cross-platform Testing
1. **Windows native**: Test with Windows Python installation
2. **WSL environment**: Test with WSL Python installation
3. **Path handling**: Verify correct path conversion between environments
4. **Font rendering**: Check font selection and readability

## Contributing to the Project

### UI Design Guidelines

#### Professional Interface Standards
- **NO EMOJIS**: Absolutely no emojis in menu items, status messages, dialog titles, or any UI text
  - Emojis create an unprofessional, childish impression
  - Use clear, descriptive text instead
  - Examples: "Startup Statistics" not "🚀 Startup Statistics"
- **NO DUPLICATE MENUS**: Avoid creating duplicate or redundant menu items
  - Each menu item should have a distinct, clear purpose
  - Remove similar functions that confuse users
  - Example: Keep "Rebuild Index" but remove "Reload Index" if they serve similar purposes
- **CONSISTENT LOCALIZATION**: All UI text must be properly localized
  - Never use hardcoded Japanese or English text
  - Use `tr()` function for all displayed strings
  - Add new strings to `data/locales/strings.json`
- **CLEAR FUNCTIONALITY**: Every menu item and button should have obvious purpose
  - Use descriptive names that indicate what the action does
  - Group related functions logically in menus
  - Avoid technical jargon when possible

### Code Style Guidelines
- Follow PySide6/Qt naming conventions
- Use type hints for function parameters and returns
- Implement proper signal-slot connections
- Maintain separation of concerns across architecture layers

### Adding New Features

#### New Widget Development
1. Create widget class in `widgets/` directory
2. Inherit from appropriate Qt base class
3. Implement signal-slot communication
4. Add to main window layout and connections
5. Update settings system if needed

#### Theme Development
1. Create new theme class in `ui/themes/`
2. Inherit from `BaseTheme`
3. Implement required methods (`get_display_name()`, `get_styles()`)
4. Register in `ThemeManager._theme_classes`
5. Test across all UI components

#### Template Development
1. Create JSON template in appropriate `templates/` subdirectory
2. Follow standard template format (title, content)
3. Test template loading and application
4. Document template purpose and usage

This project demonstrates Claude Code's capabilities in creating sophisticated desktop applications with modern UI frameworks, comprehensive feature sets, and maintainable architecture patterns.