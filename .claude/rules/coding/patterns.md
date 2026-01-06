---
paths: src/**/*.py
---

# Coding Patterns

## Signal-Slot Architecture
```python
# Define signal in widget
class MyWidget(QWidget):
    value_changed = Signal(str)

    def on_change(self):
        self.value_changed.emit(self.value)

# Connect in MainWindow
self.my_widget.value_changed.connect(self.handle_change)
```

## Configuration Access
```python
# Dot-notation for settings
settings.get('window.width', 1200)
settings.set('ui.thinking_level', 'think harder')

# Workspace management
workspace.add_folder('/path/to/project')
workspace.get_recent_files()
```

## Localization
```python
# Always use tr() for UI strings
from src.core.ui_strings import tr
label.setText(tr("label.thinking_level"))

# Add strings to data/locales/strings.json
```

## Error Handling
```python
# Graceful degradation pattern
try:
    result = risky_operation()
except SpecificError as e:
    logger.warning(f"Operation failed: {e}")
    result = fallback_value
```

## Background Workers
```python
# Use QThread for non-blocking operations
class Worker(QThread):
    finished = Signal(object)

    def run(self):
        result = long_operation()
        self.finished.emit(result)
```

## Naming Conventions
| Type | Convention | Example |
|------|------------|---------|
| Class | PascalCase | `PromptInputWidget` |
| Method | snake_case | `get_selected_item` |
| Signal | snake_case | `value_changed` |
| Constant | UPPER_SNAKE | `DEFAULT_WIDTH` |
| Private | _prefix | `_internal_state` |
