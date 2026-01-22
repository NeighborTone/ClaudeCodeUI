# 統合テスト計画

## テスト環境

| 環境 | コマンド |
|------|---------|
| WSL | `python3 main.py` |
| Windows | `python main.py` |
| WSL (英語モード) | `LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 python3 main.py` |

## 単体テスト

### Core層

```bash
# データクラス
python3 -c "from src.core.search_result import SearchMatch, FileSearchResult, SearchResults, SearchOptions; print('OK')"

# 検索エンジン
python3 -c "from src.core.content_searcher import ContentSearcher; s = ContentSearcher(); print(f'ripgrep: {s.ripgrep_available}')"

# ワーカー
python3 -c "from src.core.content_search_worker import ContentSearchManager; print('OK')"
```

### Widgets層

```bash
# 検索パネル
python3 -c "from src.widgets.content_search_panel import ContentSearchPanel; print('OK')"
```

## 機能テスト

### 基本操作

| ID | テスト項目 | 手順 | 期待結果 | 結果 |
|----|-----------|------|---------|------|
| T1 | アプリ起動 | `python3 main.py` | エラーなく起動 | ⬜ |
| T2 | タブ表示 | 左パネルを確認 | ファイル/検索タブが表示 | ⬜ |
| T3 | タブ切り替え | タブをクリック | 切り替わる | ⬜ |
| T4 | Ctrl+Shift+F | ショートカット押下 | 検索タブにフォーカス | ⬜ |

### 検索機能

| ID | テスト項目 | 手順 | 期待結果 | 結果 |
|----|-----------|------|---------|------|
| T5 | テキスト検索 | "def" と入力してEnter | 結果がツリー表示 | ⬜ |
| T6 | 結果クリック | 検索結果をクリック | プレビュー表示 | ⬜ |
| T7 | 正規表現 | `def\s+\w+` で検索（正規表現ON） | 関数定義がマッチ | ⬜ |
| T8 | 大文字小文字 | "DEF" で検索（オプションON/OFF） | 結果が変わる | ⬜ |
| T9 | 単語単位 | "def" で検索（オプションON） | "define" がマッチしない | ⬜ |
| T10 | ファイルフィルタ | `*.py` で絞り込み | Pythonファイルのみ | ⬜ |

### ローカライゼーション

| ID | テスト項目 | 手順 | 期待結果 | 結果 |
|----|-----------|------|---------|------|
| T11 | 日本語表示 | 日本語モードで起動 | 日本語で表示 | ⬜ |
| T12 | 英語表示 | 設定から英語に変更 | 英語で表示 | ⬜ |
| T13 | 言語切り替え | 言語を切り替え | タブ名等が更新 | ⬜ |

### 既存機能への影響

| ID | テスト項目 | 手順 | 期待結果 | 結果 |
|----|-----------|------|---------|------|
| T14 | ファイルツリー | ファイルを選択 | プレビューに表示 | ⬜ |
| T15 | @補完 | `@`を入力 | 補完リスト表示 | ⬜ |
| T16 | テーマ切り替え | テーマを変更 | 検索パネルにも適用 | ⬜ |
| T17 | スプリッター | パネルをリサイズ | 正常に動作 | ⬜ |

## パフォーマンステスト

| ID | テスト項目 | 条件 | 期待結果 | 結果 |
|----|-----------|------|---------|------|
| P1 | ripgrep検索 | 1000+ファイル | 1秒以内 | ⬜ |
| P2 | Python検索 | 100ファイル | 5秒以内 | ⬜ |
| P3 | 結果表示 | 1000件 | スムーズにスクロール | ⬜ |

## 回帰テスト

- [ ] 既存の全テーマで正しく表示される
- [ ] インデックス構築が正常に動作する
- [ ] プロンプト生成が正常に動作する
- [ ] 設定が正しく保存・復元される
