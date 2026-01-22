# VSCodeライクなコンテンツ検索機能 実装計画

## 概要

VSCodeのCtrl+Shift+F相当の「ファイル内コンテンツ検索機能」を実装する。
- 検索結果のプレビュー（前後の行を表示）
- 正規表現、大文字小文字区別、単語単位のオプション
- ripgrep優先、Pythonフォールバック

## 全体構成

| Phase | 概要 | チェックポイント数 |
|-------|------|------------------|
| Phase 1 | Core層実装（データクラス、検索エンジン、ワーカー） | 3個 |
| Phase 2 | Widgets層実装（検索パネルUI、プレビュー） | 2個 |
| Phase 3 | MainWindow統合（タブ化、シグナル接続） | 2個 |
| Phase 4 | 仕上げ（ローカライゼーション、テスト） | 2個 |

## 依存関係

```
Phase 1（Core層） → Phase 2（Widgets層） → Phase 3（統合） → Phase 4（仕上げ）
```

## 影響範囲

### 新規ファイル

| レイヤー | ファイル | 役割 |
|---------|---------|------|
| `src/core/` | `search_result.py` | 検索結果データクラス |
| `src/core/` | `content_searcher.py` | ripgrep/Pythonフォールバック検索エンジン |
| `src/core/` | `content_search_worker.py` | QThread非同期検索ワーカー |
| `src/widgets/` | `content_search_panel.py` | 検索パネルUI |

### 変更ファイル

| ファイル | 変更内容 |
|---------|---------|
| `src/ui/main_window.py` | 左パネルのタブ化、ContentSearchPanel統合 |
| `data/locales/strings.json` | 検索UI用の文字列追加 |

## リスク・注意点

- ripgrepがインストールされていない環境ではPythonフォールバック（低速）
- 大規模プロジェクトでは結果上限（1000件）に達する可能性

## 成功基準

- [ ] 左パネルでFileTree/検索タブが切り替わること
- [ ] テキスト検索で結果がツリー表示されること
- [ ] 結果クリックでプレビューが表示されること
- [ ] 正規表現/大文字小文字/単語単位オプションが機能すること
- [ ] ripgrepがない環境でもPythonフォールバックで動作すること

## 進捗管理

詳細: `XX_progress.md`
