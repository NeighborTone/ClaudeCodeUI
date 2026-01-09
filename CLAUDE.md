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
| `01-project-overview.md` | Project overview and quick start |
| `02-project-structure.md` | Directory structure and responsibilities |
| `03-architecture-core.md` | Core layer architecture (paths: src/core/**) |
| `04-architecture-ui.md` | UI layer architecture (paths: src/ui/**) |
| `05-architecture-widgets.md` | Widget layer architecture (paths: src/widgets/**) |
| `coding/patterns.md` | Coding patterns and conventions |
| `coding/testing.md` | Testing protocol and checklist |

## Plan Management

1. Create plan in `.claude/plan/task` for complex tasks
2. Wait for user approval
3. Do not implement until approved
