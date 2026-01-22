# Core Rules

## Principles
- R1: Question First - 不明点はWhat/Where/Howで質問してから行動 (AskUserQuestionツール使用)
- R2: Verify Always - コード変更後は必ず動作確認（Windows: `run_claudeui.bat` / WSL: `python3 main.py`）
- R3: Follow Patterns - 既存コードのパターンを踏襲
- R4: Strict Scope - 依頼された内容のみ実装、過剰な追加禁止
- R5: Objective Response - 感情・意見・過剰な称賛を排除
- R6: Maximum Efficiency - 独立した操作は並列実行
- R7: Clean Code - 作業後は一時ファイルを削除
- R8: No Ad-Hoc Fixes - エラー抑制のためのハードコード禁止
- R9: Build After Edit - コード編集後は必ずビルド実行
- R10: Plan Before Implement - 複雑タスクは計画→承認→実装

## Language Rules
| Target | Language |
|--------|----------|
| CLAUDE.md | English |
| User Communication | Japanese |
| Code | English |
| Code Comments | Japanese |
| User-facing Messages | Japanese |

## Quality Standards
- Production-level, maintainable solutions
- No unnecessary complexity, extensibility, or features
- Test functionality before completion
- Handle runtime errors appropriately

## UI Design Standards
- NO EMOJIS in UI text (professional standard)
- NO DUPLICATE MENUS
- All UI text must use localization (tr() function)
- Clear, descriptive menu item names
