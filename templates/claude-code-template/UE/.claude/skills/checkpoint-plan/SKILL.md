# /checkpoint-plan - Checkpoint Plan Generator

Generate a checkpoint-based plan interactively for a new task.

## Usage

```
/checkpoint-plan [feature_name]
```

### Arguments

- `feature_name`: Name of the feature to implement
  - Example: `user_auth`, `api_integration`, `ui_redesign`

## Execution Steps

### 1. Requirements Gathering

Use AskUserQuestion tool to confirm:
- Feature overview and purpose
- Estimated scale (file count, commit count)
- Dependent existing systems
- Special verification requirements

### 2. Task Splitting

Split into checkpoints using these criteria:

| Criteria | Value |
|----------|-------|
| Max time per CP | 2 hours |
| Commits per CP | 1-2 |
| CP verifiability | Required (build success) |

### 3. Create Plan Folder

Generate under `.claude/plan/task/[MAJOR]_plan_[feature_name]/`:

```
[MAJOR]_plan_[feature_name]/
├── 00_overview.md        # Overall overview, critical path
├── 01_phase1_xxx.md      # Phase 1 details
├── 02_phase2_xxx.md      # Phase 2 details (as needed)
├── XX_progress.md        # Progress tracker (initialized)
└── XX_testing.md         # Integration test plan (as needed)
```

### 4. Apply Templates

Generate each file following:
- `plan-management.md` plan templates
- `checkpoint-workflow.md` checkpoint format

### 5. Self-Containment Check

Run `/check-plan` after generation to verify handoff viability.

## Naming Convention

| Task Type | MAJOR Prefix Example |
|-----------|---------------------|
| Feature | `FEATURE` |
| UI | `UI` |
| System/Infrastructure | `SYSTEM` |
| Bug Fix | `BUG` |
| Refactoring | `REFACTOR` |
| API | `API` |
| Database | `DB` |
| Testing | `TEST` |

## User Approval Flow

1. Generate plan
2. Present to user for approval
3. Begin implementation after approval

## Related

- `.claude/rules/plan-management.md`: Plan management rules
- `.claude/rules/checkpoint-workflow.md`: Checkpoint workflow
- `.claude/agents/plan-continuity-checker.md`: Self-containment checker
