# /check-progress - Progress Check Command

Check plan progress status and report current position and next task.

## Usage

```
/check-progress [plan_name]
```

### Arguments

- `plan_name` (optional): Target plan folder name
  - Omitted: Check all active plans under `.claude/plan/task/`
  - Example: `FEATURE_plan_user_auth`

## Execution Steps

1. Search for active plan folders under `.claude/plan/task/` (exclude `done/`)
2. Read `XX_progress.md` from each folder
3. Aggregate current position, next task, completion rate
4. Output result report

## Output Format

```
Project Progress Status

---

## Active Tasks

### [MAJOR]_plan_feature_name

| Item | Status |
|------|--------|
| **Current** | Phase X: Checkpoint X-Y |
| **Progress** | Y/Z checkpoints complete (XX%) |
| **Latest Commit** | abc1234 - CP X-Y: [Content] |
| **Next Task** | CP X-(Y+1): [Task name] |
| **Detail** | `0X_phaseX_xxx.md` |

---

## Summary

| Task | Phase | Progress | Next CP |
|------|-------|----------|---------|
| [Task A] | Phase X | Y/Z | CP X-Y |
| [Task B] | Phase X | Y/Z | CP X-Y |

---

To continue, say "next checkpoint".
To check plan self-containment, run `/check-plan`.
```

## Related

- `/check-plan`: Plan self-containment check (handoff verification)
- `.claude/rules/plan-management.md`: Plan management rules
- `.claude/rules/checkpoint-workflow.md`: Checkpoint workflow
