# Phase 1: Core層実装

## チェックポイント 1-1: データクラス定義 - **✅ 完了**

**タスク:**
- [x] `src/core/search_result.py` 作成
  - SearchMatch: 個々のマッチ結果
  - FileSearchResult: ファイル単位の検索結果
  - SearchResults: 検索結果全体
  - SearchOptions: 検索オプション

**実装詳細:**

`src/core/search_result.py`:
- `@dataclass` を使用した型安全なデータ構造
- `SearchMatch`: line_number, line_content, match_start, match_end, context_before, context_after
- `FileSearchResult`: file_path, relative_path, matches
- `SearchResults`: query, file_results, search_time, is_regex, is_case_sensitive, is_word_match, truncated, error_message
- `SearchOptions`: query, is_regex, is_case_sensitive, is_word_match, include_patterns, exclude_patterns, max_results, context_lines, max_file_size

**検証:**
```bash
python3 -c "from src.core.search_result import SearchMatch, FileSearchResult, SearchResults, SearchOptions; print('OK')"
```

**完了条件:**
- データクラスがインポート可能
- 型ヒントが正しい

---

## チェックポイント 1-2: ContentSearcher実装 - **✅ 完了**

**タスク:**
- [x] `src/core/content_searcher.py` 作成
  - ripgrep検出・実行
  - Pythonフォールバック
  - キャンセル機能

**実装詳細:**

`src/core/content_searcher.py`:
- `ContentSearcher` クラス
- `ripgrep_available` プロパティでripgrep検出
- `_search_with_ripgrep()`: JSON出力モードでripgrep実行
- `_search_with_python()`: 正規表現ベースのPython検索
- `cancel()` / `reset_cancel()`: キャンセル制御
- デフォルト除外パターン: node_modules, __pycache__, .git, etc.

**検証:**
```bash
python3 -c "from src.core.content_searcher import ContentSearcher; s = ContentSearcher(); print(f'ripgrep: {s.ripgrep_available}')"
```

**完了条件:**
- ripgrep検出が動作する
- Python検索が動作する

---

## チェックポイント 1-3: ContentSearchWorker実装 - **✅ 完了**

**タスク:**
- [x] `src/core/content_search_worker.py` 作成
  - QThread + Signal パターン
  - ContentSearchManager

**実装詳細:**

`src/core/content_search_worker.py`:
- `ContentSearchWorker(QThread)`:
  - シグナル: `progress_updated`, `search_completed`, `search_failed`
  - `run()`: 検索実行
  - `stop()`: キャンセル

- `ContentSearchManager(QObject)`:
  - シグナル: `search_started`, `search_progress`, `search_completed`, `search_failed`
  - `set_search_paths()`: 検索パス設定
  - `start_search()`: 検索開始
  - `cancel_search()`: キャンセル

**検証:**
```bash
python3 -c "from src.core.content_search_worker import ContentSearchManager; print('OK')"
```

**完了条件:**
- ワーカーがインポート可能
- シグナルが定義されている
