---
name: dev
description: Full development cycle - build, test, lint
allowed-tools: Read, Edit, Bash, Grep
---

# Development Cycle

## Usage
```
/dev
```

## Description
Executes complete development workflow:
1. **Build** → Run `python3 main.py` to verify startup
2. **Test** → Verify application behavior (GUI startup)
3. **Lint** → Run static analysis (pylint, ruff, mypy)
4. **Report** → Aggregate results

## Workflow Order
```
Code Edit → Lint → Verify → Complete
```

## Use Cases
- After implementing new features
- Before committing changes
- Pre-merge quality check

## Output Format
```
DEV CYCLE RESULTS:
- Build: [SUCCESS/FAILED]
- Lint: [PASS/FAIL with errors]
- Status: [READY/BLOCKED]
```

## Notes
This skill invokes the `/dev` command which orchestrates the full cycle using builder, tester, and code-lint agents.
