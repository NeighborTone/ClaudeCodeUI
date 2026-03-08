# Claude Code Template

Reusable `.claude` directory template for setting up Claude Code projects quickly.

Extracted and generalized from a production Unreal Engine project's Claude Code configuration.

## Quick Start

### Windows (PowerShell)
```powershell
.\setup.ps1
# Or specify target directory:
.\setup.ps1 -TargetDir "C:\path\to\your\project"
```

### Linux / macOS / WSL
```bash
chmod +x setup.sh
./setup.sh
# Or specify target directory:
./setup.sh /path/to/your/project
```

## What's Included

### Base Template (Generic)

| Category | Files | Description |
|----------|-------|-------------|
| **Rules** | `core-rules.md` | Core development principles (R1-R11) |
| | `plan-management.md` | Plan creation, naming, progress tracking |
| | `checkpoint-workflow.md` | Checkpoint-based workflow for large tasks |
| | `handoff-validation.md` | Context-clear handoff validation |
| | `nul-cleanup.md` | Windows NUL file cleanup |
| **Agents** | `builder.md` | Build automation |
| | `debugger.md` | Runtime error debugging |
| | `tester.md` | QA testing |
| | `plan-continuity-checker.md` | Plan self-containment verification |
| **Skills** | `checkpoint-plan/` | Interactive checkpoint plan generator |
| | `check-plan/` | Plan self-containment checker |
| | `dev/` | Full development cycle |
| | `verify/` | Build verification only |
| | `read-excel/` | Excel file reader |
| | `drawio-verify/` | draw.io PNG export & verification |
| **Commands** | `check-progress.md` | Progress status report |
| **Hooks** | `cleanup-nul.ps1` | Auto-delete Windows NUL files |
| | `notify-complete.ps1` | Beep on task completion |
| | `notify-question.ps1` | Beep on question/notification |
| **Refs** | `drawio-rules.md` | draw.io authoring rules |

### Addons (Installable via Setup)

#### `ue` - Unreal Engine

| Category | Files | Description |
|----------|-------|-------------|
| **Agents** | `ue-explore.md` | UE source/doc search |
| | `builder.md` | UE-specific build automation |
| **Rules** | `ue-editor-operations.md` | Manual UE Editor operation rules |
| | `coding/ue-cpp.md` | UE C++ coding conventions |
| **Skills** | `ue-docs/` | UE documentation search |
| | `ue-log/` | UE log viewer/filter |
| | `bp-analyze/` | Blueprint asset analyzer |
| **Config** | `ue-config.json` | UE engine/project paths |

## Directory Structure

```
claude-code-template/
├── setup.ps1                    # Windows setup script
├── setup.sh                     # Unix setup script
├── CLAUDE.md.template           # Root CLAUDE.md template
├── README.md                    # This file
├── .claude/
│   ├── settings.json            # Generic settings with hooks
│   ├── agents/                  # 4 generic agents
│   ├── commands/                # 1 generic command
│   ├── hooks/                   # 3 notification/cleanup hooks
│   ├── rules/                   # 7 generic rules + templates
│   ├── skills/                  # 6 generic skills
│   ├── refs/                    # 1 reference doc
│   └── plan/task/done/          # Plan archive directory
└── UE/                          # Unreal Engine addon
    ├── agents/
    ├── rules/
    ├── skills/
    └── config/
```

## Creating Custom Addons

Create a new directory under the template root with subdirectories matching `.claude` structure:

```
my-addon/
├── agents/         # -> .claude/agents/
├── rules/          # -> .claude/rules/
├── skills/         # -> .claude/skills/
└── config/         # -> .claude/config/
```

Use `{{PLACEHOLDER}}` syntax in files for values configured during setup.

## Key Concepts

### Checkpoint Workflow
Large tasks (3+ phases, 5+ files, 8+ commits) use checkpoint-based workflow:
1. Create plan in `.claude/plan/task/`
2. Split into checkpoints (1-2 hours each)
3. Execute one checkpoint at a time
4. Verify build, update progress, commit
5. Wait for user instruction before next checkpoint
6. Archive completed plans to `done/`

### Handoff Validation
Plans are written to be self-contained, so work can resume after context is cleared.
Use `/check-plan` to verify handoff viability.

### Hooks (Windows)
- **cleanup-nul.ps1**: Prevents Windows NUL file accumulation
- **notify-complete.ps1**: Audio notification on task completion
- **notify-question.ps1**: Audio notification when Claude asks a question
