# Claude Code PromptUI

Claude Codeのプロンプト入力欄を改善するPySide6ベースのデスクトップアプリケーション

## 特徴

- **改良されたプロンプト入力**: Enterで改行、Shift+Enterで生成&コピー
- **思考レベル選択**: 小〜極限まで14段階の思考レベル
- **ファイル指定機能**: @でファイルを指定、Claude Code標準の検索機能と同等
- **ワークスペース管理**: VSCodeライクな複数プロジェクト管理
- **ファイルエクスプローラー**: ツリービューでファイルを参照・選択

## セットアップ

### 1. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 2. アプリケーションの起動

```bash
python main.py
```

## 使用方法

### 基本操作

1. **ワークスペース追加**: 左上の「フォルダ追加」ボタンでプロジェクトフォルダを追加
2. **思考レベル選択**: 右上のドロップダウンで思考レベルを選択
3. **プロンプト入力**: 
   - Enterで改行
   - Shift+Enterで生成&クリップボードにコピー
4. **ファイル指定**: `@filename`と入力すると補完候補が表示される

### ファイル指定機能

- `@`を入力すると、ファイル名の補完候補が表示されます
- 矢印キーで候補を選択、Enterで確定
- Escapeで補完をキャンセル
- 選択されたファイルの内容がプロンプトに自動挿入されます

### ショートカットキー

- `Ctrl+O`: ワークスペース追加
- `F5`: ファイルツリー更新
- `Ctrl+Shift+C`: プロンプトクリア
- `Shift+Enter`: 生成&コピー
- `Ctrl+Q`: アプリケーション終了

### 思考レベル一覧

- **think** - 通常
- **think harder** - 少し深く
- **think deeply** - 深く
- **think intensely** - 集中的に
- **think longer** - 長時間
- **think really hard** - 非常に深く
- **think super hard** - 超深く
- **think very hard** - とても深く
- **ultrathink** - 極限
- **think about it** - 考え込む
- **think a lot** - たくさん考える
- **think hard** - 一生懸命
- **think more** - もっと考える
- **megathink** - メガ思考

## プロジェクト構造

```
ClaudeCodeUI/
├── main.py                    # メインアプリケーション
├── requirements.txt           # 依存関係
├── core/                     # コア機能
│   ├── settings.py           # 設定管理
│   ├── workspace_manager.py  # ワークスペース管理
│   └── file_searcher.py      # ファイル検索
├── ui/                       # UI関連
│   └── main_window.py        # メインウィンドウ
└── widgets/                  # ウィジェット
    ├── prompt_input.py       # プロンプト入力エリア
    ├── thinking_selector.py  # 思考レベル選択
    └── file_tree.py          # ファイルツリー
```

## 設定ファイル

設定は自動的に`config/`フォルダに保存されます：

- `config/settings.json` - アプリケーション設定
- `config/workspace.json` - ワークスペース設定

## 対応ファイル形式

以下の形式のファイルがツリービューに表示されます：

- プログラミング言語: `.py`, `.cpp`, `.h`, `.hpp`, `.js`, `.ts`, `.jsx`, `.tsx`, `.cs`, `.java`, `.php`, `.go`, `.rs`
- 設定ファイル: `.json`, `.yaml`, `.yml`, `.xml`, `.ini`, `.cfg`, `.config`
- ドキュメント: `.md`, `.txt`

## トラブルシューティング

### フォントが正しく表示されない場合

- Windowsの場合、Consolasフォントが自動選択されます
- Consolasが利用できない場合、Courier Newが使用されます

### ファイル検索が動作しない場合

- ワークスペースが正しく追加されているか確認してください
- ファイルが対応形式に含まれているか確認してください

## 開発情報

- **フレームワーク**: PySide6
- **Python**: 3.8以上推奨
- **ライセンス**: プロジェクト依存