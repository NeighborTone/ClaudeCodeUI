---
description: Run static analysis on Python code
allowed-tools: Bash(mypy:*), Bash(pylint:*), Bash(ruff:*)
---

Run static analysis and report results:

## Commands
```bash
# Type checking
mypy src/ --ignore-missing-imports

# Linting (choose one)
pylint src/ --disable=C0114,C0115,C0116
ruff check src/
```

## Report
- [PASS]: All checks passed
- [FAIL]: List errors with file:line
