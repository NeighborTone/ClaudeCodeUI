# Phase 1: [フェーズ名]（推定X-Y日）

## 目標

[このフェーズで達成すること]

例：
- テーマ切り替えの基盤ロジックを実装
- 設定の永続化を実現
- コア層の実装を完了し、UI層からの呼び出しを可能にする

---

## チェックポイント 1-1: [タスク名]（推定時間） - **⬜ 未着手**

**タスク:**
- [ ] サブタスク1
  - 変更ファイル: `path/to/file.py`
  - 実装内容: [具体的な実装内容]
- [ ] サブタスク2
  - 変更ファイル: `path/to/file2.py`
  - 実装内容: [具体的な実装内容]

例：
- [ ] SettingsManagerにdark_modeプロパティを追加
  - 変更ファイル: `src/core/settings_manager.py`
  - 実装内容: `dark_mode` キーの読み書きメソッドを追加（デフォルト: False）
- [ ] テーマ切り替えメソッドの実装
  - 変更ファイル: `src/ui/themes/theme_manager.py`
  - 実装内容: `toggle_dark_mode()` メソッドを追加し、設定を更新

**実装詳細:**

`path/to/file.py`:
```python
# 実装例
def example_function():
    # コード例を記載
    pass
```

例：

`src/core/settings_manager.py`:
```python
def get_dark_mode(self) -> bool:
    """ダークモード設定を取得"""
    return self.settings.get("dark_mode", False)

def set_dark_mode(self, enabled: bool):
    """ダークモード設定を保存"""
    self.settings["dark_mode"] = enabled
    self.save_settings()
```

`src/ui/themes/theme_manager.py`:
```python
def toggle_dark_mode(self):
    """ダークモードの切り替え"""
    current = self.settings_manager.get_dark_mode()
    self.settings_manager.set_dark_mode(not current)
    self.apply_theme()  # 既存メソッドを再利用
```

**検証:**
```bash
# 検証コマンド
python3 main.py
```

または:
```
1. アプリを起動
2. [操作手順]
3. [期待結果]
```

例：
```bash
python3 main.py
```

手動確認:
1. アプリを起動
2. Pythonコンソールで `app.theme_manager.toggle_dark_mode()` を実行
3. テーマが切り替わることを確認（ログ出力を確認）
4. `saved/settings.json` を開き、`"dark_mode": true` が保存されていることを確認
5. アプリを再起動し、設定が保持されていることを確認

**完了条件:**
- 条件1
- 条件2

例：
- `get_dark_mode()` と `set_dark_mode()` が正しく動作する
- `toggle_dark_mode()` でテーマが切り替わる
- 設定がファイルに保存され、再起動後も保持される
- 既存のテーマ切り替え機能に影響がない

**次のチェックポイント:** 1-2

---

## チェックポイント 1-2: [タスク名]（推定時間） - **⬜ 未着手**

**タスク:**
- [ ] サブタスク1
- [ ] サブタスク2

**実装詳細:**

（同様の構造）

**検証:**

（同様の構造）

**完了条件:**

（同様の構造）

**次のチェックポイント:** 2-1（Phase 2へ移行）

---

## Phase 1 完了後のチェックリスト

- [ ] 全チェックポイントが完了
- [ ] 全ての検証が成功
- [ ] Gitコミットが適切に作成されている
- [ ] XX_progress.md が更新されている
- [ ] Phase 2の準備が整っている

## メモ

- [実装中に発見した注意事項]
- [次のフェーズへの引き継ぎ事項]
