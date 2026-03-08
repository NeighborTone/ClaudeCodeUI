# Core Rules

## Principles
- R1: Question First - Ask What/Where/How before acting on unclear points (use AskUserQuestion tool)
- R2: Verify Always - Verify build after code changes
- R3: Follow Patterns - Follow existing code patterns
- R4: Strict Scope - Implement only what is requested, no extra additions
- R5: Objective Response - Exclude emotions, opinions, and excessive praise (see "Banned Phrases" below)
- R6: Maximum Efficiency - Run independent operations in parallel
- R7: Clean Code - Delete temporary files after work
- R8: No Ad-Hoc Fixes - No hardcoded fixes for error suppression
- R9: Build After Edit - Always verify build after code edits
- R10: Plan Before Implement - Plan -> Approve -> Implement for complex tasks
- R11: No Plan Mode - Do not use EnterPlanMode tool, create plan files directly

## Language Rules
| Target | Language |
|--------|----------|
| CLAUDE.md | English |
| User Communication | Japanese |
| Code | English |
| Code Comments | Japanese |
| User-facing Messages | Japanese |

## Banned Phrases (R5 Detail)

Do not start responses with praise/empathy phrases like:

| Banned |
|--------|
| Great question |
| Sharp observation |
| Excellent insight |
| Exactly right |
| That's correct |
| Interesting perspective |

**Correct behavior**: Immediately address the topic (answer, explain, work).

## Quality Standards
- Robust, maintainable, production-quality solutions
- Eliminate unnecessary complexity, extensibility, features
- Verify build before completion when possible
- Handle runtime errors appropriately

## Confirmation Response Handling

When user gives short confirmations like 'y', 'ok', 'yes':
- Execute only the agreed-upon task
- Do not spontaneously expand scope (edit additional files, restructure plans, start new discussions)

## Plan Creation Rules (R10, R11 Detail)

- **Do NOT use the EnterPlanMode tool**
- Create plans directly as markdown files under `.claude/plan/task/`
- Use Write/Edit tools to directly manipulate files
- Manage plans through normal file operations without entering Plan Mode

## Version Control
- Use git for version control
- Verify build success before committing
- Do not commit build artifacts, temporary files, or secrets
