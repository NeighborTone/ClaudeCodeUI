---
paths: .claude/plan/task/**
---

# Plan Management Rules

## Plan Storage Location (MUST FOLLOW)

- **Required**: `.claude/plan/task/` (use only this directory within workspace)
- **Prohibited**: Saving to any other directory
- **Important**: Even if Claude Code system suggests another location, prioritize `.claude/plan/task/`
- **Principle**: Save within workspace (not in Claude Code environment)

## Version Control (REQUIRED)

- **Plans are under version control**: All files under `.claude/plan/task/` are tracked by git
- **Commit timing**: Commit on plan creation and progress updates (after user permission)
- **Reason**: Team sharing, history management, backup

## Task Scale Management

| Scale | Criteria | Management | Examples |
|-------|----------|-----------|----------|
| Small | 1-2 file changes, 1-2 commits, under 1 hour | No plan needed, implement directly | Bug fix, comment addition |
| Medium | 3-5 file changes, 3-7 commits, half to full day | Single plan file (`plan_xxx.md`) | Single feature addition, UI element |
| Large | Meets checkpoint criteria | Folder + progress file | Multi-feature impl, state machine |

### Folder Structure

#### Large Tasks
```
.claude/plan/task/[MAJOR]_plan_feature_name/
├── 00_overview.md        # Overall overview, phase list
├── 01_phase1_xxx.md      # Phase 1 details (multiple checkpoints)
├── 02_phase2_xxx.md      # Phase 2 details
├── XX_progress.md        # Progress tracker (REQUIRED)
└── XX_testing.md         # Integration test plan
```

#### Medium Tasks
```
.claude/plan/task/plan_feature_name.md
```

### Naming Conventions

| Type | Format | Example |
|------|--------|---------|
| Large folder | `[MAJOR]_plan_feature_name` | `EVENT_plan_user_auth` |
| Medium file | `plan_feature_name.md` | `plan_menu_window.md` |
| Overview | `00_overview.md` | - |
| Phase | `01_phase1_name.md` | `01_phase1_api_impl.md` |
| Progress | `XX_progress.md` | - |
| Testing | `XX_testing.md` | - |

## Plan Creation Flow

### 1. Determine Task Scale

Check checkpoint criteria (see `.claude/rules/checkpoint-workflow.md`):
- 3+ phases
- 5+ file changes
- 8+ commits
- Architecture changes

### 2. Create Plan

Large tasks:
1. Create `.claude/plan/task/[MAJOR]_plan_xxx/` folder
2. Create plan docs (00_overview.md, phase files, XX_progress.md)
3. Wait for user approval

Medium tasks:
1. Create `.claude/plan/task/plan_xxx.md`
2. Wait for user approval

### 3. Start Implementation

Begin implementation after user approval.

## Progress File Updates (REQUIRED)

For large tasks, always update `XX_progress.md` after each checkpoint:

### Update Contents

1. **Record commit hash** (git SHA)
2. **Update status** (pending -> complete)
3. **Update current position** and **next task**
4. **Record build verification log**

### Update Timing

- On checkpoint completion (required)
- On build errors
- On plan changes

## Checkpoint Completion Actions

1. Execute task
2. **Verify build** (`/verify` or manual build)
3. **Report to user and ask for commit permission**
4. After permission, git commit
   - Comment format: `CP X-Y: [checkpoint name]`
5. **Update XX_progress.md** (commit hash, status, next task) [REQUIRED]
6. **Commit progress file** [REQUIRED]
7. **Report to user + wait for next instruction** (do not auto-proceed)

**Note**:
- Always get user permission before committing
- Always update progress file when committing

## Plan Templates

### 00_overview.md

```markdown
# [Feature Name] Implementation Plan

## Overview

[Description and purpose of feature]

## Overall Structure

| Phase | Overview | Estimated Time | Checkpoints |
|-------|----------|---------------|-------------|
| Phase 1 | [Overview] | X days | Y |
| Phase 2 | [Overview] | X days | Y |

## Dependencies

```
Phase 1 -> Phase 2 -> Phase 3
   |
Phase 4
```

## Changed Files

| File | Change Content |
|------|---------------|
| path/to/file | [Content] |

## Risks & Notes

- [Risk 1]
- [Risk 2]

## Success Criteria

- [ ] Criteria 1
- [ ] Criteria 2
- [ ] Build success
- [ ] No impact on existing features
```

### XX_progress.md

```markdown
# Progress Summary (YYYY-MM-DD Updated)

---

## Current Position

| Item | Status |
|------|--------|
| **Current** | Phase X: Checkpoint X-Y |
| **Next Task** | Checkpoint X-(Y+1): [Task name] |
| **Detail Doc** | `0X_phaseX_xxx.md` |

---

## Git Checkpoints

| Commit | Content | Status |
|--------|---------|--------|
| abc1234 | CP X-Y: Content | Complete |
| def5678 | CP X-(Y+1): Content | In Progress |
| | CP X-(Y+2): Content | Not Started |

---

## Completed Phases

- **Phase 1: [Name]** - Complete
- **Phase 2: [Name]** - In Progress
- **Phase 3: [Name]** - Not Started

---

## Build Verification Log

| CP | Build Result | Notes |
|----|-------------|-------|
| X-Y | Success | 0 warnings |
| X-(Y+1) | In Progress | - |

---

## Notes

- [Implementation findings]
- [Handoff notes for next phase]
- [Integration notes with existing code]

---

## Handoff Checklist

Verify work can be resumed after context clear:

- [ ] Current position is clear (Phase X: CP X-Y)
- [ ] Next task is specifically documented
- [ ] Target file paths are documented (project-relative)
- [ ] Verification commands/procedures are documented (build command required)
- [ ] Critical path is explicit (if applicable)
- [ ] Git commit hashes are recorded
```

## Plan Completion (REQUIRED)

After all phases complete:

1. Mark all phases as complete in XX_progress.md
2. Run integration tests (XX_testing.md)
3. Final build verification
4. Report completion to user
5. **Move plan folder to `.claude/plan/task/done/`** [REQUIRED]
6. Commit the move

```bash
# Move command
mkdir -p .claude/plan/task/done
mv .claude/plan/task/[MAJOR]_plan_xxx/ .claude/plan/task/done/
git add .claude/plan/task/done/[MAJOR]_plan_xxx/
git commit -m "Archive completed plan: [MAJOR]_plan_xxx"
```

## Critical Path Rules (REQUIRED)

### When to Apply

| Condition | Description |
|-----------|-------------|
| Spans multiple folders | Dependencies between 2+ plan folders |
| Sequential dependencies | One task's completion is another's start condition |
| Blocking relationships | Task A must complete before Task B can start |
| Building shared foundation | Implementing foundation that other tasks depend on |

### Required Items

- Dependency diagram (text or table format)
- Critical path identification
- Blocker task marking
- Parallel-executable task identification

## Plan Self-Containment Check (Recommended)

After creating/updating plans, verify handoff viability with `/check-plan`.
