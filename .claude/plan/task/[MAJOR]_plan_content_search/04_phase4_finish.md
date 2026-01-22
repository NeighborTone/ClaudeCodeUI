# Phase 4: 仕上げ

## チェックポイント 4-1: ローカライゼーション - **⬜ 未着手**

**タスク:**
- [ ] `data/locales/strings.json` に検索UI用の文字列追加

**実装詳細:**

`data/locales/strings.json` に以下を追加:

```json
"tab_file_tree": {
  "ja": "ファイル",
  "en": "Files"
},
"tab_content_search": {
  "ja": "検索",
  "en": "Search"
},
"content_search_placeholder": {
  "ja": "検索キーワードを入力...",
  "en": "Enter search keyword..."
},
"content_search_case_sensitive": {
  "ja": "Aa",
  "en": "Aa"
},
"content_search_case_sensitive_tooltip": {
  "ja": "大文字/小文字を区別",
  "en": "Match case"
},
"content_search_regex": {
  "ja": ".*",
  "en": ".*"
},
"content_search_regex_tooltip": {
  "ja": "正規表現を使用",
  "en": "Use regular expression"
},
"content_search_word_match": {
  "ja": "\\b",
  "en": "\\b"
},
"content_search_word_match_tooltip": {
  "ja": "単語単位でマッチ",
  "en": "Match whole word"
},
"content_search_include_files": {
  "ja": "対象:",
  "en": "Include:"
},
"content_search_include_tooltip": {
  "ja": "検索対象ファイルパターン（例: *.py,*.js）",
  "en": "File patterns to include (e.g., *.py,*.js)"
},
"content_search_exclude_files": {
  "ja": "除外:",
  "en": "Exclude:"
},
"content_search_exclude_tooltip": {
  "ja": "除外するパターン（例: node_modules,dist）",
  "en": "Patterns to exclude (e.g., node_modules,dist)"
},
"content_search_ready": {
  "ja": "検索キーワードを入力してください",
  "en": "Enter a search keyword"
},
"content_search_searching": {
  "ja": "検索中...",
  "en": "Searching..."
},
"content_search_no_workspace": {
  "ja": "ワークスペースが登録されていません",
  "en": "No workspace registered"
},
"content_search_result_summary": {
  "ja": "{matches}件 ({files}ファイル) {time}秒",
  "en": "{matches} matches in {files} files ({time}s)"
},
"content_search_truncated": {
  "ja": "(結果が上限に達しました)",
  "en": "(Results truncated)"
},
"content_search_preview_placeholder": {
  "ja": "検索結果をクリックするとプレビューが表示されます",
  "en": "Click a search result to preview"
},
"status_content_search_selected": {
  "ja": "選択: {filename}:{line}",
  "en": "Selected: {filename}:{line}"
}
```

**検証:**
```bash
python3 main.py
# 日本語UIで検索パネルが正しく表示されることを確認
# 英語に切り替えて正しく表示されることを確認
```

**完了条件:**
- 全ての文字列が日本語/英語両方で定義されている
- 言語切り替え時に正しく表示される

---

## チェックポイント 4-2: 最終テスト - **⬜ 未着手**

**タスク:**
- [ ] 起動テスト
- [ ] 機能テスト
- [ ] パフォーマンステスト

**検証手順:**

### 1. 起動テスト
```bash
# WSL
python3 main.py

# Windows
python main.py
```

### 2. 機能テスト

| テスト項目 | 手順 | 期待結果 |
|-----------|------|---------|
| タブ切り替え | 左パネルのタブをクリック | FileTree/検索が切り替わる |
| Ctrl+Shift+F | ショートカット押下 | 検索タブに切り替わり、入力にフォーカス |
| テキスト検索 | "def" と入力して検索 | 結果がツリー表示される |
| 結果クリック | 検索結果をクリック | プレビューが表示される |
| 正規表現 | `def\s+\w+` で検索 | 正規表現がマッチする |
| 大文字小文字 | "DEF" で検索（オプションON/OFF） | 結果が変わる |
| 単語単位 | "def" で検索（オプションON/OFF） | "define" がマッチしなくなる |
| ファイルフィルタ | `*.py` で絞り込み | Pythonファイルのみ表示 |

### 3. パフォーマンステスト

- 大規模プロジェクト（10000+ファイル）で検索
- 結果表示が1秒以内に完了すること（ripgrep使用時）

**完了条件:**
- 全テスト項目がパス
- エラーなく起動・終了
- 既存機能に影響なし
