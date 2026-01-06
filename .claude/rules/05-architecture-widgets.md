---
paths: src/widgets/**/*.py
---

# Architecture: Widget Layer

## Overview
```
┌─────────────────────────────────────────────────────────┐
│                    Widget Layer                         │
├──────────────────┬──────────────────┬──────────────────┤
│   Input/Edit     │   Navigation     │    Selection     │
├──────────────────┼──────────────────┼──────────────────┤
│ PromptInput      │ FileTree         │ ThinkingSelector │
│ PromptPreview    │ FileTreeWorker   │ TemplateSelector │
│                  │                  │ PromptHistory    │
└──────────────────┴──────────────────┴──────────────────┘
```

## Components

### Input/Edit Widgets
| Widget | Responsibility |
|--------|----------------|
| `PromptInputWidget` | Rich text editor with file completion |
| `PromptPreviewWidget` | Real-time final prompt preview |

### Navigation Widgets
| Widget | Responsibility |
|--------|----------------|
| `FileTreeWidget` | Hierarchical workspace browser |
| `FileTreeWorker` | Async file tree operations |

### Selection Widgets
| Widget | Responsibility |
|--------|----------------|
| `ThinkingSelectorWidget` | 14-level thinking system |
| `TemplateSelector` | Pre/post template selection |
| `PromptHistory` | History management and search |

## Smart File Completion
Patterns supported in PromptInputWidget:
- `@filename` - Search files and folders
- `!filename` - Search files only
- `#foldername` - Search folders only

## Completion Flow
```
User types @ → 200ms debounce → Search triggered →
Results filtered → Ranked by relevance →
Selection → Convert to @relative/path format
```

## Widget Communication
All widgets communicate via Qt signals to MainWindow.
No direct widget-to-widget communication.
