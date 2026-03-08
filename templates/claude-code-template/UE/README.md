# Claude Code Template for Unreal Engine

Reusable `.claude` directory template for setting up Claude Code in UE projects.

Extracted and generalized from a production Unreal Engine project's Claude Code configuration.

## Installation Methods

### Method 1: Setup Script (Recommended)

#### Windows (PowerShell)
```powershell
.\setup.ps1
# Or specify target directory:
.\setup.ps1 -TargetDir "C:\path\to\your\project"
```

#### Linux / macOS / WSL
```bash
chmod +x setup.sh
./setup.sh
# Or specify target directory:
./setup.sh /path/to/your/project
```

### Method 2: Plugin Installation

This template also supports Claude Code's plugin system:

```bash
# Install as a plugin (from local path)
/plugin install /path/to/this/template

# Or from a git repository
/plugin install owner/repo
```

See `.claude-plugin/plugin.json` for the plugin manifest.

### Method 3: Manual Copy

1. Copy `.claude/` directory to your project root
2. Copy `CLAUDE.md.template` as `CLAUDE.md` and replace `{{placeholders}}`
3. Customize skills and rules for your project

## What's Included

### Core (All Projects)

| Category | Files | Description |
|----------|-------|-------------|
| **Rules** | `core-rules.md` | Core development principles (R1-R11) |
| | `plan-management.md` | Plan creation, naming, progress tracking |
| | `checkpoint-workflow.md` | Checkpoint-based workflow (R0, R11-R17) |
| | `handoff-validation.md` | Context-clear handoff validation |
| | `nul-cleanup.md` | Windows NUL file cleanup |
| **Agents** | `debugger.md` | Runtime error debugging (sonnet) |
| | `tester.md` | QA testing (haiku) |
| | `plan-continuity-checker.md` | Plan self-containment verification (haiku) |
| **Skills** | `checkpoint-plan/` | Interactive checkpoint plan generator |
| | `check-plan/` | Plan self-containment checker |
| | `dev/` | Full development cycle |
| | `verify/` | Build verification only |
| | `checkin/` | VCS check-in + build verification |
| | `vcs-status/` | Show VCS pending changes |
| | `read-excel/` | Excel file reader |
| | `drawio-verify/` | draw.io PNG export & verification |
| **Commands** | `check-progress.md` | Progress status report |
| **Hooks** | `cleanup-nul.ps1` | Auto-delete Windows NUL files (PostToolUse) |
| | `notify-complete.ps1` | Beep on task completion (Stop) |
| | `notify-question.ps1` | Beep on question/notification |
| **Refs** | `drawio-rules.md` | draw.io authoring rules |

### UE-Specific

| Category | Files | Description |
|----------|-------|-------------|
| **Agents** | `builder.md` | UE build automation (haiku) |
| | `ue-explore.md` | UE engine source/doc search (sonnet) |
| | `quality-checker.md` | Code quality verification (haiku) |
| **Rules** | `ue-editor-operations.md` | Manual UE Editor operation rules (R-UE1~R-UE7) |
| | `coding/ue-cpp.md` | UE C++ coding conventions |
| | `coding/no-tick-polling.md` | No Tick/Timer/polling rule |
| | `coding/debug-output.md` | Debug output guidelines for Standalone mode |
| **Skills** | `ue-docs/` | UE documentation search |
| | `ue-log/` | UE log viewer/filter |
| | `bp-analyze/` | Blueprint .uasset analyzer |
| **Config** | `ue-config.json` | UE engine/project paths |

## Template Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `{{PROJECT_NAME}}` | Project name | `MyGame` |
| `{{PROJECT_DESCRIPTION}}` | Project description | `An UE5 action game` |
| `{{BUILD_COMMAND}}` | Build/verify command | `Build.bat MyGame Win64 Development` |
| `{{QUICK_START_COMMANDS}}` | Quick start commands | `pip install -r requirements.txt` |
| `{{USER_LANGUAGE}}` | Communication language | `Japanese` / `English` |
| `{{COMMENT_LANGUAGE}}` | Code comment language | `Japanese` / `English` |
| `{{UE_VERSION}}` | UE version (addon) | `UE 5.5` |
| `{{UE_ENGINE_PATH}}` | UE engine path (addon) | `C:\EpicGames\UE_5.5` |
| `{{PROJECT_PATH}}` | UE project path (addon) | `C:\Projects\MyGame\UE` |
| `{{SOURCE_DIR}}` | Source code directory | `Source` |

## Directory Structure

```
claude-code-template/UE/
├── setup.ps1                    # Windows setup script
├── setup.sh                     # Unix setup script
├── setup.bat                    # Windows batch wrapper
├── CLAUDE.md.template           # Root CLAUDE.md template
├── README.md                    # This file
├── .claude/
│   ├── settings.json            # Settings with hooks, permissions, env
│   ├── agents/                  # 6 agents (builder, debugger, tester, etc.)
│   ├── commands/                # 1 command (check-progress)
│   ├── hooks/                   # 3 hooks (cleanup, notify)
│   ├── rules/                   # 9 rules + coding/ subdirectory
│   │   └── coding/             # 3 coding rules (ue-cpp, no-tick, debug-output)
│   ├── skills/                  # 14 skills
│   ├── config/                  # UE config template
│   ├── refs/                    # Reference docs
│   └── plan/task/done/          # Plan archive directory
└── .claude-plugin/
    └── plugin.json              # Plugin manifest for plugin distribution
```

## All Commands

| Command | Description |
|---------|-------------|
| `/verify` | Build verification |
| `/dev` | Full development cycle (build + test + quality) |
| `/checkin [message]` | VCS check-in + build verification |
| `/vcs-status` | Show pending VCS changes |
| `/ue-docs [query]` | Search UE documentation |
| `/ue-log [filter]` | View UE log files (Standalone/Editor) |
| `/bp-analyze [args]` | Analyze Blueprint .uasset files |
| `/check-plan [path]` | Verify plan self-containment |
| `/check-progress` | Check current checkpoint progress |
| `/checkpoint-plan [name]` | Generate checkpoint-based plan |
| `/drawio-verify [path]` | Export draw.io to PNG and verify |
| `/read-excel [path]` | Read Excel files |

## Key Concepts

### Checkpoint Workflow
Large tasks (3+ phases, 5+ files, 8+ commits) use checkpoint-based workflow:
1. Create plan in `.claude/plan/task/`
2. Split into checkpoints (1-2 hours each)
3. Execute one checkpoint at a time
4. Verify build, update progress, commit (with user permission)
5. Document UE Editor operations if applicable (R17)
6. Wait for user instruction before next checkpoint
7. Archive completed plans to `done/`

### Handoff Validation
Plans are written to be self-contained, so work can resume after context is cleared.
Use `/check-plan` to verify handoff viability.

### Hooks (Windows)
- **cleanup-nul.ps1**: Prevents Windows NUL file accumulation (PostToolUse: Write|Edit)
- **notify-complete.ps1**: Audio notification on task completion (Stop)
- **notify-question.ps1**: Audio notification when Claude asks a question (Notification)

### Plugin System
This template can be distributed as a Claude Code plugin. The plugin manifest (`.claude-plugin/plugin.json`) declares all skills, agents, and hooks. Users can install it via `/plugin install` for automatic updates.

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
