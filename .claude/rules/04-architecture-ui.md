---
paths: src/ui/**/*.py
---

# Architecture: UI Layer

## Overview
```
┌─────────────────────────────────────────────────────────┐
│                      UI Layer                           │
├──────────────┬──────────────┬──────────────────────────┤
│  MainWindow  │    Style     │        Themes            │
├──────────────┼──────────────┼──────────────────────────┤
│ Orchestrator │ Global CSS   │ Light, Dark, Cyberpunk   │
│ Menu System  │ Theme Apply  │ Nordic, Electric         │
│ State Mgmt   │              │ Material, Retro, Sci-Fi  │
└──────────────┴──────────────┴──────────────────────────┘
```

## Components

### MainWindow
- Central orchestrator for all components
- Menu system management
- Application state coordination
- Signal routing between widgets

### Style System
| Component | Responsibility |
|-----------|----------------|
| `style.py` | Global style management |
| `style_themes.py` | Theme-specific definitions |

### Theme Architecture
Located in `src/ui/themes/`:
- `BaseTheme` - Abstract base class
- `ThemeManager` - Dynamic registration and switching
- 8 available themes with no-restart switching

## Signal Flow
```
TemplateSelector → MainWindow → PromptPreviewWidget
FileTreeWidget → MainWindow → PromptInputWidget
```

## Theme Implementation Pattern
```python
class CustomTheme(BaseTheme):
    def get_display_name(self) -> str:
        return "Custom Theme"

    def get_styles(self) -> str:
        return """QMainWindow { background-color: #custom; }"""
```
