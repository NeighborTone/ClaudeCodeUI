# Phase 3: MainWindow統合

## チェックポイント 3-1: 左パネルタブ化 - **⏳ 進行中**

**タスク:**
- [x] import追加: `QTabWidget`, `ContentSearchPanel`
- [x] `setup_ui()`: 左パネルを`QTabWidget`でタブ化（一部完了）
- [ ] `left_widget` 参照の修正（スプリッター同期コード）
- [ ] ワークスペース変更時の検索パス更新

**実装詳細:**

`src/ui/main_window.py`:

1. import追加（完了）:
```python
from PySide6.QtWidgets import (..., QTabWidget)
from src.widgets.content_search_panel import ContentSearchPanel
```

2. `setup_ui()` 変更（完了）:
```python
# 左側：タブウィジェット（ファイルツリー + コンテンツ検索）
self.left_tab_widget = QTabWidget()

# ファイルツリータブ
self.file_tree = FileTreeWidget(self.workspace_manager)
self.left_tab_widget.addTab(self.file_tree, tr("tab_file_tree"))

# コンテンツ検索タブ
self.content_search_panel = ContentSearchPanel()
self.left_tab_widget.addTab(self.content_search_panel, tr("tab_content_search"))

self.main_splitter.addWidget(self.left_tab_widget)
```

3. `left_widget` 参照の修正（未完了）:
```python
# log_splitter_state() などで left_widget を参照している箇所を修正
# self.file_tree.parent() → self.left_tab_widget
```

4. ワークスペース変更時の検索パス更新（未完了）:
```python
def on_workspace_changed(self):
    # ... 既存コード ...
    # 検索パネルの検索パスを更新
    workspace_paths = [ws['path'] for ws in self.workspace_manager.get_workspaces()]
    self.content_search_panel.set_search_paths(workspace_paths)
```

**検証:**
```bash
python3 main.py
# 左パネルにタブが表示されることを確認
```

**完了条件:**
- 左パネルにFileTree/検索の2つのタブが表示される
- タブ切り替えが動作する
- スプリッターのリサイズが正常に動作する

---

## チェックポイント 3-2: シグナル接続・ショートカット追加 - **⬜ 未着手**

**タスク:**
- [ ] `setup_connections()`: ContentSearchPanelのシグナル接続
- [ ] `setup_shortcuts()`: Ctrl+Shift+Fショートカット追加
- [ ] `_on_language_changed()`: ContentSearchPanelの言語更新

**実装詳細:**

`src/ui/main_window.py`:

1. `setup_connections()` に追加:
```python
# コンテンツ検索
self.content_search_panel.file_selected.connect(self.on_content_search_file_selected)
self.content_search_panel.search_completed.connect(self.on_content_search_completed)
```

2. `setup_shortcuts()` に追加:
```python
# Ctrl+Shift+F: コンテンツ検索にフォーカス
content_search_shortcut = QShortcut(QKeySequence("Ctrl+Shift+F"), self)
content_search_shortcut.activated.connect(self.focus_content_search)
```

3. 新規メソッド追加:
```python
def focus_content_search(self):
    """コンテンツ検索にフォーカス"""
    self.left_tab_widget.setCurrentWidget(self.content_search_panel)
    self.content_search_panel.focus_search_input()

def on_content_search_file_selected(self, file_path: str, line_number: int):
    """コンテンツ検索でファイルが選択されたとき"""
    self.statusBar().showMessage(
        tr("status_content_search_selected", filename=os.path.basename(file_path), line=line_number),
        2000
    )

def on_content_search_completed(self, matches: int, files: int, time: float):
    """コンテンツ検索完了時"""
    self.statusBar().showMessage(
        tr("content_search_result_summary", matches=matches, files=files, time=f"{time:.2f}"),
        3000
    )
```

4. `_on_language_changed()` に追加:
```python
self.content_search_panel.update_language()

# タブテキストを更新
self.left_tab_widget.setTabText(0, tr("tab_file_tree"))
self.left_tab_widget.setTabText(1, tr("tab_content_search"))
```

**検証:**
```bash
python3 main.py
# Ctrl+Shift+F で検索タブに切り替わることを確認
# 検索結果クリック時にステータスバーに表示されることを確認
```

**完了条件:**
- Ctrl+Shift+Fで検索タブに切り替わる
- 検索結果をクリックするとステータスバーに表示される
- 言語切り替え時にタブ名が更新される
