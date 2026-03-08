# /check-plan - Plan Self-Containment Check

Verify that plans can be fully handed off after context is cleared.

## Usage

```
/check-plan [plan_path]
```

### Arguments

- `plan_path` (optional): Target plan folder or file to check
  - Omitted: Check all active plans under `.claude/plan/task/`
  - Example: `FEATURE_plan_user_auth`

## Verification Items

### Critical (Required)

| Item | Description |
|------|-------------|
| Current position clarity | XX_progress.md has current CP number and status |
| Next task clarity | Next CP number, task name, and detail doc link |
| File path specificity | Target files in project-relative format |
| Critical path | Critical path diagram exists (if multi-task dependencies) |

### High (Recommended)

| Item | Description |
|------|-------------|
| Implementation detail | Code examples, function signatures |
| Verification steps | Build commands, test procedures |
| VCS info | Commit hashes recorded |

## Execution Steps

1. Identify target plan folder
2. Read `00_overview.md` for overall structure
3. Read `XX_progress.md` for current position
4. Read current phase file
5. Check each verification item
6. Output result report

## Output Example

```
# Plan Self-Containment Check Results

## Target: FEATURE_plan_user_auth

### Overall Assessment: Needs Fix

| Item | Status | Details |
|------|:------:|---------|
| Current position | Pass | Phase 2 CP2-1 in progress |
| Next task | Pass | CP2-2: API integration |
| File paths | Pass | All paths documented |
| Critical path | Pass | Dependencies charted |
| Implementation detail | Warn | CP2-1 missing code examples |
| Verification steps | Pass | Build command documented |
| VCS info | Warn | CP1-3 missing commit hash |

### Items Needing Fixes

1. Add code examples to CP2-1 implementation details
2. Record commit hash for CP1-3
```

## Auto-Execution Timing

Recommended at:
- Plan creation complete
- Checkpoint complete (before commit)
- Major plan updates

## Related

- `.claude/agents/plan-continuity-checker.md`: Agent definition
- `.claude/rules/plan-management.md`: Plan management rules
- `.claude/rules/checkpoint-workflow.md`: Checkpoint workflow
