---
name: lint
description: Run static analysis on Python code
allowed-tools: Bash, Read
---

# Lint Code

## Usage
```
/lint [path]
```

## Description
Runs static analysis tools on Python code:
- `pylint src/`
- `ruff check .`
- `mypy src/`

## Default Target
If no path specified, analyzes entire `src/` directory.

## Output Format
- **[PASS]**: All checks passed
- **[FAIL]**: List errors with `file:line` references

## Workflow
This skill invokes the `/lint` command which:
1. Runs configured linters (pylint, ruff, mypy)
2. Aggregates results
3. Reports errors with file locations
