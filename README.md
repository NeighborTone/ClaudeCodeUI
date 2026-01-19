# Claude Code PromptUI

Claude Code向けのプロンプト入力機能を提供するPySide6ベースのデスクトップアプリケーション。
Claude Codeによって開発されたプロジェクトです。

## 主要機能

### プロンプト入力システム
- Enter改行、Shift+Enter生成&コピー機能
- 最終プロンプトのリアルタイムプレビュー
- 日本語・英語対応のトークン推定

### テンプレート管理システム
- プリプロンプトテンプレートの自動適用
- ポストプロンプトテンプレートの追加指示機能
- YAMLファイルベースのテンプレート編集・追加

### ワークスペース管理
- 複数プロジェクトのワークスペース管理
- ファイル補完機能：`@filename`（全て）、`!filename`（ファイルのみ）、`#foldername`（フォルダのみ）
- 階層表示のファイルツリービュー
- 40種類以上のファイル形式対応

### テーマシステム
- 9種類のテーマ：Light, Dark, Cyberpunk, Nordic, Electric, Material, Retro, Sci-Fi
- 再起動不要の動的テーマ切り替え
- ユーザー設定の自動保存・復元

### 多言語対応
- 日本語・英語対応
- システム環境による自動言語検出
- メニューからの手動言語切り替え

## セットアップ

### 前提条件
- Python 3.8以上
- Windows または WSL環境

### インストール
```bash
# リポジトリをクローン
git clone [repository-url]
cd ClaudeCodeUI

# 依存関係をインストール
pip install -r requirements.txt

# アプリケーションを起動
python main.py
```

### WSL環境での実行
```bash
# WSL環境でのPython実行
python3 main.py

# 依存関係のインストール
pip3 install -r requirements.txt
```

## 使用方法

### 基本ワークフロー
1. **ワークスペース追加**: 「フォルダ追加」でプロジェクトを登録
2. **テンプレート選択**: プリ・ポストプロンプトを選択
3. **プロンプト作成**: 本文を入力し、`@` `!` `#`でスマートファイル指定
4. **プレビュー確認**: 右パネルで最終プロンプトを確認
5. **生成&コピー**: Shift+Enterでクリップボードに出力

### 高度な機能

#### スマートファイル指定システム
- `@filename` : ファイル・フォルダ両方を検索
- `!filename` : ファイルのみを検索
- `#foldername` : フォルダのみを検索
- 相対パス形式でClaude Codeに最適化
- 選択後は自動的に`@`形式で挿入
- ファイル内容を自動的にプロンプトに含める

#### テンプレート活用
- **Claude Code Best Practice**: Claude Code使用時のベストプラクティス集
- **サンプルテンプレート**: プリ・ポストプロンプトのシンプルな使用例
- **カスタムテンプレート**: JSONファイルで独自テンプレートを追加可能

#### トークンカウンター
- 日本語と英語で異なる文字/トークン比率を適用
- URLやコードブロックの特殊パターンを考慮
- リアルタイムでトークン数を表示

## ショートカットキー

| キー | 機能 |
|------|------|
| `Ctrl+O` | ワークスペース追加 |
| `F5` | ファイルツリー更新 |
| `Ctrl+Shift+C` | プロンプトクリア |
| `Shift+Enter` | 生成&コピー |
| `Ctrl+Q` | アプリケーション終了 |
| `Escape` | ファイル補完キャンセル (すべてのモード) |

## プロジェクト構造

```
ClaudeCodeUI/
├── main.py                     # エントリーポイント
├── requirements.txt            # 依存関係定義
├── src/                        # ソースコード
│   ├── core/                  # コア機能（19ファイル）
│   │   ├── settings.py        # 設定管理システム
│   │   ├── workspace_manager.py # ワークスペース管理
│   │   ├── file_searcher.py   # ファイル検索エンジン
│   │   ├── fast_sqlite_searcher.py # SQLite検索エンジン
│   │   ├── template_manager.py # テンプレート管理
│   │   ├── token_counter.py   # トークンカウンター
│   │   ├── language_manager.py # 言語管理
│   │   ├── environment_detector.py # 環境検出
│   │   ├── path_converter.py  # パス変換
│   │   ├── python_helper.py   # Python実行支援
│   │   └── ui_strings.py      # UI文字列管理
│   ├── ui/                    # UI層
│   │   ├── main_window.py     # メインウィンドウ
│   │   ├── style.py           # スタイル管理
│   │   └── themes/            # テーマシステム（11ファイル）
│   │       ├── theme_manager.py # テーマ管理
│   │       ├── base_theme.py  # ベーステーマ
│   │       ├── light_theme.py # ライトテーマ
│   │       ├── dark_theme.py  # ダークテーマ
│   │       ├── cyberpunk_theme.py # サイバーパンクテーマ
│   │       ├── nordic_theme.py # ノルディックテーマ
│   │       ├── electric_theme.py # エレクトリックテーマ
│   │       ├── material_theme.py # マテリアルテーマ
│   │       ├── retro_theme.py # レトロテーマ
│   │       └── scifi_theme.py # サイファイテーマ
│   └── widgets/               # ウィジェット層
│       ├── prompt_input.py    # プロンプト入力
│       ├── file_tree.py       # ファイルツリー
│       ├── template_selector.py # テンプレート選択
│       ├── prompt_preview.py  # プロンプトプレビュー
│       └── prompt_history.py  # プロンプト履歴
├── data/                       # アプリケーションデータ
│   ├── locales/               # 多言語対応
│   │   └── strings.json       # UI文字列定義
│   └── file_filters.json      # ファイルタイプ設定
├── saved/                      # ユーザー固有データ
│   ├── settings.json          # アプリケーション設定
│   ├── workspace.json         # ワークスペース設定
│   ├── prompt_history.json    # プロンプト履歴
│   └── file_index.db          # SQLiteインデックス
├── templates/                  # テンプレートシステム
│   ├── pre/                   # プリプロンプト
│   │   ├── Comprehensive_Guidelines.yaml
│   │   ├── Check CLAUDE.md_Rules.yaml
│   │   └── Sample_Pre.yaml
│   └── post/                  # ポストプロンプト
│       ├── Comprehensive_Guidelines.yaml
│       ├── MergeWithCLAUDE.md.yaml
│       └── Sample_Post.yaml
└── assets/                     # アプリケーションアセット
    └── icons/                 # テーマ別アイコン
```

## 対応ファイル形式

### プログラミング言語
Python, C/C++, JavaScript/TypeScript, Java, C#, PHP, Go, Rust, Swift, Kotlin

### 設定・データ
JSON, YAML, XML, INI, Config, TOML

### ドキュメント
Markdown, Text, CSV

### ゲーム開発
Unreal Engine (.ue, .umap, .uasset)

### Web開発
HTML, CSS, Vue, React (JSX/TSX)

**注記**: ファイルタイプ設定は `data/file_filters.json` で管理されており、カスタマイズが可能です。

## 設定カスタマイズ

### ファイルフィルター設定
`data/file_filters.json` でファイルタイプ設定をカスタマイズ可能：
```json
{
  "allowed_extensions": [".py", ".js", ".ts", ...],
  "important_files": ["readme", "license", "makefile", ...],
  "excluded_dirs": ["node_modules", "__pycache__", ".git", ...]
}
```

### テンプレート追加
```yaml
title: "カスタムテンプレート名"
content: |
  プロンプト内容...
```

### 言語設定
- メニュー: `設定 → 言語` で切り替え
- 設定ファイル: `saved/settings.json` の `ui.language`

### テーマカスタマイズ
新しいテーマを追加する場合：
1. `src/ui/themes/` に新しいテーマクラスを作成
2. `src/ui/themes/theme_manager.py` に登録
3. `BaseTheme` を継承して実装

## トラブルシューティング

### WSL環境での実行エラー
```bash
# Python環境の確認
python3 --version

# 依存関係の再インストール
pip3 uninstall PySide6 PyQt6 -y
pip3 install -r requirements.txt

# WSLからの実行
wsl python3 /mnt/c/.../ClaudeCodeUI/main.py
```

### フォント表示問題
- Windows: Consolas → Courier New の順で自動選択
- WSL: システムフォントを自動検出

### ファイル検索が動作しない
1. ワークスペースが正しく追加されているか確認
2. 対応ファイル形式に含まれているか確認
3. F5でファイルツリーを更新

## 技術仕様

### 依存関係
- **PySide6** >= 6.5.0 (メインUIフレームワーク)
- **PyQt6** >= 6.5.0 (フォールバック)
- **watchdog** >= 3.0.0 (ファイル監視)
- **PyYAML** >= 6.0 (テンプレート管理)

### 実行環境
- **Python**: 3.8以上推奨
- **プラットフォーム**: Windows, WSL

## 開発情報

Claude Code によって開発されたプロジェクトです。アーキテクチャは信号駆動のMVCパターンとモジュラー設計を採用しています。

### アーキテクチャ特徴
- 信号スロット通信によるコンポーネント間連携
- ドット記法による階層型設定管理
- モジュラーテーマシステム
- 日本語・英語の多言語対応

## ライセンス

プロジェクト依存 - 詳細は各プロジェクトのライセンスに従います。