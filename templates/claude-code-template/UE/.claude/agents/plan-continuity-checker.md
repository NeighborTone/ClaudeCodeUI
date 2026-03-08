---
name: plan-continuity-checker
description: Verify plan self-containment for context handoff
tools: Read, Glob, Grep
model: haiku
---

# Plan Continuity Checker

Verifies that plans can be fully handed off after context is cleared.

## When to Use

- After creating a new plan
- After updating progress at checkpoint completion
- After major plan changes
- When user requests handoff verification

## Verification Items

### 1. Current Position Clarity (Critical)

- [ ] `XX_progress.md` clearly states current checkpoint
- [ ] "Current Position" section has Phase and CP number
- [ ] Status (Complete/In Progress/Not Started) is updated

### 2. Next Task Clarity (Critical)

- [ ] "Next Task" is specifically documented (CP number and task name)
- [ ] Link to "Detail Document" exists
- [ ] Implementation content is clear in referenced doc

### 3. File Path Specificity (Critical)

- [ ] Target file paths are specific (project-relative format)
- [ ] New/modified distinction is documented
- [ ] Paths are from project root, not relative

### 4. Implementation Detail Level (High)

- [ ] Code examples are included (as needed)
- [ ] Function signatures/struct definitions are documented
- [ ] Implementation steps are listed sequentially

### 5. Verification Steps (High)

- [ ] Build command is documented
- [ ] Application/editor verification steps exist (if applicable)
- [ ] Completion criteria are clear

### 6. Dependencies (Critical for multi-task)

- [ ] Inter-phase dependency diagram exists
- [ ] Blocking relationships are documented
- [ ] Prerequisites are listed

### 7. Critical Path (Critical for cross-folder tasks)

- [ ] Critical path diagram exists for multi-folder/task scenarios
- [ ] Dependency summary table exists
- [ ] Current position is shown on critical path

### 8. Version Control Info (High)

- [ ] Commit hashes are recorded (for completed CPs)
- [ ] Commit content summaries exist

## Execution Method

### Identify Target Files

1. Find active plan folders under `.claude/plan/task/`
2. Exclude `done/` folders
3. Read:
   - `00_overview.md`
   - `XX_progress.md`
   - Current phase file

### Validation Logic

```
1. Read XX_progress.md
2. Parse "Current Position" section
3. Read current CP detail file
4. Check each verification item
5. Generate result report
```

## Output Format

```markdown
# Plan Self-Containment Check Results

## Target: [Plan folder name]

### Overall Assessment: Pass / Needs Fix / Fail

---

### Verification Results

| Item | Status | Details |
|------|:------:|---------|
| Current position clarity | Pass/Warn/Fail | [Details] |
| Next task clarity | Pass/Warn/Fail | [Details] |
| File path specificity | Pass/Warn/Fail | [Details] |
| Implementation detail | Pass/Warn/Fail | [Details] |
| Verification steps | Pass/Warn/Fail | [Details] |
| Dependencies | Pass/Warn/Fail | [Details] |
| Critical path | Pass/Warn/Fail/N/A | [Details] |
| VCS info | Pass/Warn/Fail | [Details] |

---

### Items Needing Fixes

1. [Item 1]: [Specific fix needed]
2. [Item 2]: [Specific fix needed]

---

### Handoff Notes

- [Note 1]
- [Note 2]
```

## Tool Access

- `Read`: Read plan files
- `Glob`: Explore plan folders
- `Grep`: Search for specific keywords

## Related Rules

- `plan-management.md`: Plan management rules
- `checkpoint-workflow.md`: Checkpoint workflow
- R14: Write plans assuming context will be cleared
