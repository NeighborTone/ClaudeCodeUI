# ClaudeCodeUI

PySide6-based desktop application for enhancing Claude Code's prompt input functionality.

## Rules

- 不明点はWhat/Where/Howで質問してから行動
- コード変更後は必ず動作確認（`python3 main.py`）
- 既存コードのパターンを踏襲
- 依頼された内容のみ実装、過剰な追加禁止
- 感情・意見・過剰な称賛を排除
- 事実が不確かな場合は推測せず確認し、根拠を引用

## Language Rules

| Target | Language |
|--------|----------|
| CLAUDE.md | English |
| User Communication | Japanese |
| Code | English |
| Code Comments | Japanese |
| User-facing Messages | Japanese |

## Quick Start

```bash
# WSL (recommended)
pip3 install -r requirements.txt
python3 main.py

# Windows
pip install -r requirements.txt
python main.py
```

## Build & Verify

```bash
# WSL testing (English mode for font compatibility)
LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 python3 main.py
```

## Documentation

Detailed documentation is split into `.claude/rules/`:

| Rule | Description |
|------|-------------|
| `core-rules.md` | Core principles and quality standards |
| `plan-management.md` | Task planning and progress tracking |
| `checkpoint-workflow.md` | Checkpoint-based workflow for complex tasks |
| `01-project-overview.md` | Project overview and quick start |
| `02-project-structure.md` | Directory structure and responsibilities |
| `03-architecture-core.md` | Core layer architecture (paths: src/core/**) |
| `04-architecture-ui.md` | UI layer architecture (paths: src/ui/**) |
| `05-architecture-widgets.md` | Widget layer architecture (paths: src/widgets/**) |
| `coding/patterns.md` | Coding patterns and conventions |
| `coding/testing.md` | Testing protocol and checklist |

## Plan Management

### Task Scale Classification

| Scale | Criteria | Management |
|-------|----------|------------|
| Small | 1-2 files, 1-2 commits | No plan needed, direct implementation |
| Medium | 3-5 files, 3-7 commits | Single plan file (`plan_xxx.md`) |
| Large | Checkpoint criteria met | Folder + progress file |

### Checkpoint-Based Workflow (Large Tasks)

Use checkpoint-based workflow when ANY of the following apply:
- 3+ phases required
- Multi-day work
- 5+ files changed
- 8+ commits expected
- Architecture changes

**Critical Rules:**
1. Create plan with checkpoints in `.claude/plan/task/[MAJOR]_plan_xxx/`
2. Each checkpoint = 1-2 hours of work (standard granularity)
3. **MUST stop and report after each checkpoint**
4. Update `XX_progress.md` after every checkpoint
5. Verify with `python3 main.py` after each checkpoint
6. Wait for user instruction before continuing

**Checkpoint Structure:**
```
.claude/plan/task/[MAJOR]_plan_xxx/
├── 00_overview.md        # Overall plan
├── 01_phase1_xxx.md      # Phase 1 with checkpoints
├── XX_progress.md        # Progress tracker (REQUIRED)
└── XX_testing.md         # Integration test plan
```

**User Commands:**
- "続けて" / "次のチェックポイント" - Continue to next checkpoint
- "進捗を確認" - Check current progress

**Details:** See `.claude/rules/checkpoint-workflow.md` and `.claude/rules/plan-management.md`
