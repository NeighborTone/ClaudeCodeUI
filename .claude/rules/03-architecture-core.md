---
paths: src/core/**/*.py
---

# Architecture: Core Layer

## Overview
```
┌─────────────────────────────────────────────────────────┐
│                     Core Layer                          │
├──────────────┬──────────────┬──────────────────────────┤
│   Indexing   │   Managers   │      Utilities           │
├──────────────┼──────────────┼──────────────────────────┤
│ SQLiteIndexer│ Settings     │ TokenCounter             │
│ FastSearcher │ Workspace    │ EnvironmentDetector      │
│ IndexAdapter │ Template     │ PathConverter            │
│ StartupOpt   │ Localization │ Logger                   │
└──────────────┴──────────────┴──────────────────────────┘
```

## Components

### High-Performance Indexing System
| Component | Responsibility |
|-----------|----------------|
| `SQLiteIndexer` | FTS5 full-text search database |
| `FastSQLiteSearcher` | LRU caching, fuzzy search |
| `SQLiteIndexingWorker` | Background indexing with progress |
| `IndexingAdapter` | Old/new system compatibility |
| `StartupOptimizer` | Intelligent startup optimization |

### System Managers
| Component | Responsibility |
|-----------|----------------|
| `SettingsManager` | JSON config with dot-notation access |
| `WorkspaceManager` | Multi-project workspace management |
| `TemplateManager` | Pre/post prompt templates |
| `LocalizationManager` | Language management (ja/en) |

### Utilities
| Component | Responsibility |
|-----------|----------------|
| `TokenCounter` | Japanese/English token estimation |
| `EnvironmentDetector` | Windows/WSL detection |
| `PathConverter` | Cross-platform path normalization |
| `Logger` | Application-wide logging |

## Patterns
- Signal-based communication between components
- Hierarchical configuration with auto-save
- Background workers for non-blocking operations
