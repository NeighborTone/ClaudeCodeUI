# Phase 2: Widgets層実装

## チェックポイント 2-1: ContentSearchPanel基本UI - **✅ 完了**

**タスク:**
- [x] `src/widgets/content_search_panel.py` 作成
  - 検索入力、オプション、結果リスト

**実装詳細:**

`src/widgets/content_search_panel.py`:
- `ContentSearchPanel(QWidget)`:
  - シグナル: `file_selected`, `search_started`, `search_completed`
  - UI構成:
    - 検索入力 (`QLineEdit`) + 検索ボタン
    - オプション: 大文字小文字、正規表現、単語単位 (`QCheckBox`)
    - フィルター: 含めるパターン、除外パターン (`QComboBox`)
    - 結果サマリー (`QLabel`)
    - 結果ツリー (`QTreeWidget`)
    - プレビュー (`QTextEdit`)

**検証:**
```bash
python3 -c "from src.widgets.content_search_panel import ContentSearchPanel; print('OK')"
```

**完了条件:**
- パネルがインポート可能
- UI要素が正しく配置されている

---

## チェックポイント 2-2: プレビュー機能 - **✅ 完了**

**タスク:**
- [x] コンテキスト付きプレビュー表示
- [x] マッチハイライト

**実装詳細:**

`src/widgets/content_search_panel.py` の `_show_preview()`:
- ファイルパス表示（青色、太字）
- コンテキスト行（灰色）
- マッチ行（黒色）
- マッチ部分（黄色背景ハイライト）
- 行番号表示

**検証:**
```bash
python3 -c "from src.widgets.content_search_panel import ContentSearchPanel; p = ContentSearchPanel(); print('Preview OK')"
```

**完了条件:**
- プレビューにコンテキスト行が表示される
- マッチ部分がハイライトされる
