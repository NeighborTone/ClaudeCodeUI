# Project Structure

```
ClaudeCodeUI/
├── main.py                 # Application entry point
├── src/
│   ├── core/              # Core business logic
│   │   ├── settings_manager.py
│   │   ├── workspace_manager.py
│   │   ├── sqlite_indexer.py
│   │   ├── fast_sqlite_searcher.py
│   │   ├── template_manager.py
│   │   ├── token_counter.py
│   │   └── localization_manager.py
│   ├── ui/                # User interface
│   │   ├── main_window.py
│   │   ├── style.py
│   │   └── themes/        # Theme system
│   └── widgets/           # Specialized UI widgets
│       ├── prompt_input_widget.py
│       ├── file_tree_widget.py
│       ├── thinking_selector_widget.py
│       └── template_selector.py
├── data/                   # Application data (version controlled)
│   ├── locales/strings.json
│   └── file_filters.json
├── saved/                  # User data (NOT version controlled)
│   ├── settings.json
│   └── workspace.json
├── templates/              # Prompt templates
│   ├── pre/
│   └── post/
└── assets/icons/           # Theme icons
```

## Directory Responsibilities
| Directory | Responsibility |
|-----------|----------------|
| `src/core/` | Business logic, data management, indexing |
| `src/ui/` | Main window, styling, theme management |
| `src/widgets/` | Specialized UI components |
| `data/` | Application resources (read-only) |
| `saved/` | User preferences (read-write) |
| `templates/` | Pre/post prompt templates |
