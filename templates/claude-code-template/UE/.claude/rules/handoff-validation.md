---
paths: .claude/plan/task/**
---

# Handoff Validation Rules

## Auto-Validation Timing

Run `/check-plan` handoff validation at:

| Timing | Required | Description |
|--------|:--------:|-------------|
| Plan creation complete | Yes | Before user approval |
| Checkpoint complete | Yes | Before committing |
| Phase complete | Yes | Before starting next phase |
| Major plan updates | Recommended | On scope changes, etc. |

## On Validation Failure

1. Identify missing items
2. Fix plan (auto where possible, confirm with user for unknowns)
3. Report fixes to user
4. Re-validate

**Commits are only allowed after validation passes.**

## Required Items

### XX_progress.md Required Items

- [ ] Current position (Phase X: Checkpoint X-Y)
- [ ] Next task (Checkpoint X-(Y+1): [Task name])
- [ ] Reference to detail document
- [ ] Git checkpoint table (with commit hashes)
- [ ] Build verification log
- [ ] Critical path status (if multi-task dependencies exist)
- [ ] Handoff checklist

### Each Checkpoint Required Items

- [ ] Task list (including subtasks)
- [ ] Target file paths (project-relative format)
- [ ] Implementation details (code examples or implementation steps)
- [ ] Verification commands or procedures (build command required)
- [ ] Completion criteria (including build success)
- [ ] Reference to next checkpoint
- [ ] Dependencies (blocked by / blocks)

### Critical Path Required Items (for multi-task scenarios)

- [ ] Dependency diagram (text or table format)
- [ ] Critical path identification
- [ ] Blocker task warning marks
- [ ] Parallel-executable task identification

## Related

- `.claude/skills/check-plan/SKILL.md`: Self-containment check skill
- `.claude/agents/plan-continuity-checker.md`: Checker agent
- `.claude/rules/plan-management.md`: Plan management rules
- `.claude/rules/checkpoint-workflow.md`: Checkpoint workflow
