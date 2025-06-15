# Claude Code PromptUI

Claude Codeのプロンプト入力を革新的に改善するPySide6ベースのデスクトップアプリケーション。  
Claude Codeの性能検証プロジェクトとして、すべてのコードがClaude Codeによって作成されています。

## 主要機能

### 📝 高度なプロンプト入力システム
- **スマート入力**: Enter改行、Shift+Enter生成&コピー
- **リアルタイムプレビュー**: 最終プロンプトをリアルタイム表示
- **トークンカウンター**: 日本語・英語対応の正確なトークン推定
- **思考レベル選択**: 14段階の思考レベル（think ～ ultrathink）

### 🗂️ テンプレート管理システム
- **プリプロンプト**: タスク開始時の定型文を自動挿入
- **ポストプロンプト**: 追加指示を自動付加
- **カスタマイズ可能**: JSONファイルで自由に編集・追加

### 📁 ワークスペース管理
- **VSCode風UI**: 複数プロジェクトを効率管理
- **ファイル補完**: `@filename`でインテリジェント補完
- **ツリービュー**: 階層表示でファイルを素早く参照
- **対応形式**: 40+のファイル形式をサポート

### 🎨 テーマシステム
- **4種類のテーマ**: Light, Dark, Cyberpunk, Nordic
- **動的切り替え**: 再起動不要でテーマ変更
- **設定保持**: テーマ選択を自動保存・復元

### 🌐 多言語対応
- **日本語・英語対応**: 環境に応じた自動言語検出
- **手動切り替え**: メニューから言語変更可能
- **混在環境対応**: 日本語UIと英語技術用語の併用

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
pip install -r ClaudeCodeUI/requirements.txt

# アプリケーションを起動
python ClaudeCodeUI/main.py
```

### WSL環境での実行
```bash
# WSL推奨: Python3を使用
python3 ClaudeCodeUI/main.py

# 依存関係のインストール
pip3 install -r ClaudeCodeUI/requirements.txt
```

## 使用方法

### 基本ワークフロー
1. **ワークスペース追加**: 「フォルダ追加」でプロジェクトを登録
2. **テンプレート選択**: プリ・ポストプロンプトを選択
3. **思考レベル設定**: 目的に応じた思考レベルを選択
4. **プロンプト作成**: 本文を入力し、`@`でファイル指定
5. **プレビュー確認**: 右パネルで最終プロンプトを確認
6. **生成&コピー**: Shift+Enterでクリップボードに出力

### 高度な機能

#### ファイル指定システム
- `@`入力で補完候補を表示
- 相対パス形式でClaude Codeに最適化
- ファイル内容を自動的にプロンプトに含める

#### テンプレート活用
- **Claude Code Best Practice**: Claude Code使用時のベストプラクティス集
- **カスタムテンプレート**: JSONファイルで独自テンプレートを追加可能
- **プリプロンプト**: タスク開始時の定型文を自動挿入
- **ポストプロンプト**: 追加指示を自動付加（将来対応予定）

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
| `Escape` | ファイル補完キャンセル |

## 思考レベル一覧

| レベル | 説明 | 用途 |
|--------|------|------|
| think | 通常思考 | 一般的なタスク |
| think harder | やや深い思考 | 複雑な問題 |
| think deeply | 深い思考 | 詳細な分析 |
| think intensely | 集中的思考 | 重要な判断 |
| think longer | 長時間思考 | 時間をかけた検討 |
| think really hard | 非常に深い思考 | 困難な課題 |
| think super hard | 超深い思考 | 専門的な問題 |
| think very hard | とても深い思考 | 慎重な判断 |
| ultrathink | 極限思考 | 最高レベルの分析 |
| think about it | 熟考 | 多角的検討 |
| think a lot | 大量思考 | 網羅的な検討 |
| think hard | 一生懸命思考 | 集中的な作業 |
| think more | 追加思考 | さらなる検討 |
| megathink | メガ思考 | 最大級の思考力 |

## プロジェクト構造

```
ClaudeCodeUI/
├── main.py                     # エントリーポイント
├── requirements.txt            # 依存関係定義
├── config/                     # 設定ファイル
│   ├── settings.json          # アプリケーション設定
│   └── workspace.json         # ワークスペース設定
├── core/                       # コア機能
│   ├── settings.py            # 設定管理システム
│   ├── workspace_manager.py   # ワークスペース管理
│   ├── file_searcher.py       # ファイル検索エンジン
│   ├── template_manager.py    # テンプレート管理
│   ├── token_counter.py       # トークンカウンター
│   ├── language_manager.py    # 言語管理
│   ├── environment_detector.py # 環境検出
│   ├── path_converter.py      # パス変換
│   ├── python_helper.py       # Python実行支援
│   └── ui_strings.py          # UI文字列管理
├── ui/                         # UI層
│   ├── main_window.py         # メインウィンドウ
│   ├── style.py               # スタイル管理
│   └── themes/                # テーマシステム
│       ├── theme_manager.py   # テーマ管理
│       ├── base_theme.py      # ベーステーマ
│       ├── light_theme.py     # ライトテーマ
│       ├── dark_theme.py      # ダークテーマ
│       ├── cyberpunk_theme.py # サイバーパンクテーマ
│       └── nordic_theme.py    # ノルディックテーマ
├── widgets/                    # ウィジェット層
│   ├── prompt_input.py        # プロンプト入力
│   ├── thinking_selector.py   # 思考レベル選択
│   ├── file_tree.py           # ファイルツリー
│   ├── template_selector.py   # テンプレート選択
│   ├── prompt_preview.py      # プロンプトプレビュー
│   └── path_mode_selector.py  # パスモード選択
├── templates/                  # テンプレートシステム
│   ├── pre/                   # プリプロンプト
│   │   └── ClaudeCodeBestPractice.json
│   └── post/                  # ポストプロンプト（カスタム追加可能）
└── resources/                  # リソース
    └── icons/                 # アイコン
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

## 設定カスタマイズ

### テンプレート追加
```json
{
  "title": "カスタムテンプレート名",
  "content": "プロンプト内容..."
}
```

### 言語設定
- メニュー: `設定 → 言語` で切り替え
- 設定ファイル: `config/settings.json` の `ui.language`

### テーマカスタマイズ
新しいテーマを追加する場合：
1. `ui/themes/` に新しいテーマクラスを作成
2. `theme_manager.py` に登録
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

- **フレームワーク**: PySide6 >= 6.5.0
- **互換性**: PyQt6 >= 6.5.0 (バックアップ)
- **ファイル監視**: watchdog >= 3.0.0
- **Python**: 3.8以上推奨
- **プラットフォーム**: Windows, WSL

## 開発情報

このプロジェクトは Claude Code の性能検証として作成されており、すべてのコードが Claude Code によって生成されています。アーキテクチャは信号駆動のMVCパターンに基づき、モジュラー設計により高い拡張性を実現しています。

### アーキテクチャ特徴
- **信号スロット通信**: Qt信号による疎結合設計
- **階層型設定管理**: ドット記法による設定アクセス
- **プラガブルテーマシステム**: 動的テーマ切り替え
- **多言語対応**: 環境自動検出と手動切り替え

## ライセンス

プロジェクト依存 - 詳細は各プロジェクトのライセンスに従います。