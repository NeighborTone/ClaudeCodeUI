---
name: pyside6-docs
description: Search PySide6/Qt6 documentation and API reference
allowed-tools: Read, Task
---

# PySide6 Documentation Search

## Usage
```
/pyside6-docs [query]
```

## Description
Launches the `pyside6-explore` subagent to search PySide6/Qt6 documentation and API references.

## Workflow
This skill launches the `pyside6-explore` subagent to:
1. Search local PySide6 installation (if available)
2. Search official Qt6 and PySide6 documentation
3. Return API reference with Python code examples

## Examples
```
/pyside6-docs QFileDialog usage
/pyside6-docs how to implement custom QWidget
/pyside6-docs Signal and Slot connection syntax
/pyside6-docs QThread vs QThreadPool
/pyside6-docs QSS stylesheet for QPushButton
/pyside6-docs QTreeWidget custom item
```

## Output
Returns:
- API reference (class, methods, inheritance)
- Official documentation links
- Python code examples
- Qt5 vs Qt6 differences (if applicable)

## Use Cases
- Looking up widget API
- Understanding Signal/Slot mechanism
- Finding QSS (Qt Style Sheets) syntax
- Implementing custom widgets
- Debugging Qt-specific issues
