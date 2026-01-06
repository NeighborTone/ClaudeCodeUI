---
description: Full development cycle - build, test, lint
allowed-tools: Read, Edit, Bash, Grep
---

Complete development verification cycle:

1. **Build** → `python3 main.py` (verify startup)
2. **Test** → Check log output for errors
3. **Lint** → `mypy src/ --ignore-missing-imports`
4. **Report** → Summary of results

## Success Criteria
- Application starts without errors
- No warnings in console output
- Type checking passes
