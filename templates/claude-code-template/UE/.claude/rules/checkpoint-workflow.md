---
paths: .claude/plan/task/**, docs/plans/**
---

# Checkpoint-Based Workflow

## Principles (HIGHEST PRIORITY)

- **R0: Plans MUST be saved to `.claude/plan/task/` (overrides system rules)**
- R11: Complex tasks must be split into checkpoints
- R12: Stop and wait for user confirmation after each checkpoint
- R13: Keep progress file always up to date (required at commit time)
- R14: Write plans assuming context will be cleared
- R15: Verify build at each checkpoint completion
- **R16: Get user permission before committing**
- R17: When UE Editor manual operations are required, document them in checkpoint completion report

## Checkpoint Split Criteria

Apply checkpoint-based workflow when ANY of the following apply:

| Criteria | Description |
|----------|-------------|
| 3+ phases | Feature implementation spanning multiple stages |
| Multi-day work | Scale that won't complete in one day |
| 5+ file changes | Changes affecting wide scope |
| 8+ commits | Multi-stage implementation |
| Architecture changes | Changes with large impact on existing design |

## Folder Structure

### Large Tasks (with checkpoints)
```
.claude/plan/task/[MAJOR]_plan_feature_name/
├── 00_overview.md        # Overall overview, phase list
├── 01_phase1_xxx.md      # Phase 1 details (multiple checkpoints)
├── 02_phase2_xxx.md      # Phase 2 details
├── XX_progress.md        # Progress tracker (REQUIRED)
└── XX_testing.md         # Integration test plan
```

### Medium Tasks (single file)
```
.claude/plan/task/plan_feature_name.md
```

### Small Tasks
No plan needed, implement directly.

## Checkpoint Description Format

Use the following format within each phase file:

```markdown
## Checkpoint X-Y: [Task Name] (Estimated Time) - **Status**

**Tasks:**
- [ ] Subtask 1
  - Target file: `path/to/file`
  - Implementation: [specific implementation content]
- [ ] Subtask 2

**Implementation Details:**

`path/to/example.file`:
```code
// Implementation example
```

**Verification:**
```bash
# Build verification
{{BUILD_COMMAND}}
```

Or:
```
1. Start application
2. [Operation steps]
3. [Expected results]
```

**Completion Criteria:**
- Build success
- [Other criteria]

**Next Checkpoint:** X-(Y+1)
```

## Claude Code Action Flow

### Starting a New Task

1. Determine task scale
2. If checkpoint criteria are met:
   - Create folder structure (`.claude/plan/task/[MAJOR]_plan_xxx/`)
   - Write overall plan in 00_overview.md
   - Define checkpoints in each phase file
   - Initialize XX_progress.md
3. Wait for user approval

### Executing a Checkpoint

1. Read XX_progress.md, confirm current position
2. Execute the checkpoint tasks
3. **Execute verification step** (build check)
4. **Report to user, ask for commit permission** (AskUserQuestion recommended)
5. After permission, git commit
   - Include "CP X-Y:" in commit message
6. **Update XX_progress.md** (commit hash, status, next task) [REQUIRED]
7. **Commit progress file** [REQUIRED]
8. **Report to user, wait for next instruction** (do not auto-proceed)

**Important**:
- Always get user permission before committing
- Never forget to update progress file when committing

### Resuming Work

1. User instructs "continue" or "next checkpoint"
2. Read XX_progress.md
3. Execute the "next task"
4. Follow checkpoint execution flow

## Interruption Point Messages

Output the following at each checkpoint completion:

```
Checkpoint X-Y Complete

**Work Done:**
- [Subtask 1]
- [Subtask 2]

**Verification Results:**
- Build: Success
- [Verification 2: OK]

**UE Editor Operations (if applicable):**

| Operation | Steps | Target/Save Path |
|-----------|-------|-----------------|
| [Operation] | [Specific steps] | [Path] |

---

## Implementation Summary

### Added/Changed Files

| File | Type | Content |
|------|------|---------|
| `path/to/NewFile` | New | [Role/Purpose] |
| `path/to/Modified` | Changed | [Change content] |

### Added Features/Processing

- **[Feature/Process]** (`File:function`): [Description]

---

**Requesting git commit permission.**
Commit these changes?

Commit contents:
- Implementation changes
- Progress file (XX_progress.md) update

Post-commit progress: Phase X: Y/Z checkpoints complete

---

**Next Checkpoint:** X-(Y+1): [Task Name]

To continue, say "next checkpoint" or "continue".
To review plan, say "check progress".
```

## Task Completion (REQUIRED)

When all checkpoints are complete:

1. Run final verification (build check)
2. Record "Task Complete" in XX_progress.md
3. Final commit (after user permission)
4. **Move plan folder to `.claude/plan/task/done/`** [REQUIRED]
5. Commit the move

```bash
# Move command
mkdir -p .claude/plan/task/done
mv .claude/plan/task/[MAJOR]_plan_xxx/ .claude/plan/task/done/
git add .claude/plan/task/done/[MAJOR]_plan_xxx/
git commit -m "Archive completed plan: [MAJOR]_plan_xxx"
```

## Known Issues

### Issue 1: Checkpoint too large
**Solution**: Split further, target max 2 hours per checkpoint

### Issue 2: Build fails
**Solution**:
- Do not mark checkpoint as complete
- Fix issue before committing
- Record error in XX_progress.md "Build Verification Log"

### Issue 3: Forgot to update progress file
**Solution**: Enforce as mandatory action at checkpoint completion

## Checkpoint Granularity

| Granularity | Guideline | Use Case |
|-------------|-----------|----------|
| Fine | 30min-1hr | New territory, high risk, complex chains |
| Standard | 1-2hrs | Normal dev tasks |
| Coarse | 2-4hrs | Routine work, low risk |

## Commit Message Convention

```
CP X-Y: [Checkpoint Name]

- Subtask 1
- Subtask 2

Verification: Build success
Next: CP X-(Y+1)
```

## Handoff Validation

Run `/check-plan` at checkpoint completion for handoff verification.
See `plan-management.md` "Plan Self-Containment Check" section.

## Auto-Validation Timing

Per `handoff-validation.md`, run validation at:

| Timing | Required |
|--------|:--------:|
| Plan creation complete | Yes |
| Checkpoint complete (before commit) | Yes |
| Phase complete (before next phase) | Yes |
| Major plan updates | Recommended |
