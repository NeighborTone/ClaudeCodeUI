# 並列ヘッドレスモードによるサブエージェント活用

## 概要

大規模な情報収集や並列処理が必要なタスクでは、**ヘッドレスモード(`claude -p`)を使用してサブエージェントを並列起動**することを推奨する。

## 適用対象タスク

| タスク種別 | 例 |
|-----------|-----|
| コードベース検索 | 特定パターンのファイル検索、関数一覧の抽出 |
| ウェブリサーチ | ベストプラクティス調査、API仕様確認 |
| ドキュメント探索 | プロジェクト内ドキュメントの要約 |
| 単純な並列作業 | リネーム、フォーマット変換、一括置換 |

## ヘッドレスモードの特徴

### コンテキスト分離
- 各ヘッドレスインスタンスは**独立したコンテキスト**を持つ
- メインのコンテキストは**自動共有されない**
- 必要な情報は**プロンプトで明示的に渡す**

### 結果の統合
- `--json`オプションで構造化された出力を取得
- 結果ファイルを統合してメインClaudeに渡す

### エラーハンドリング
- 各プロセスの終了ステータスを確認
- 失敗時の代替処理をスクリプトで定義

## スクリプトテンプレート

プロジェクト内にスクリプトテンプレートを用意:

| スクリプト | 環境 | 場所 |
|-----------|------|------|
| `parallel_research.ps1` | Windows PowerShell | `.claude/scripts/` |
| `parallel_research.sh` | WSL/Linux/macOS | `.claude/scripts/` |

### 実行方法

#### Windows (PowerShell)
```powershell
cd C:\Users\owner\Desktop\PythonTools\ClaudeCodeUI
.\\.claude\scripts\parallel_research.ps1
```

#### WSL/Linux/macOS
```bash
cd /path/to/ClaudeCodeUI
bash .claude/scripts/parallel_research.sh
```

### カスタマイズ

スクリプト内のプロンプト定義を編集:

```powershell
# PowerShell版
$prompts = @{
    "code_search" = "src/core/で主要なクラスを列挙"
    "pattern_analysis" = "デザインパターンを特定"
    "doc_summary" = "ドキュメントを要約"
}
```

```bash
# Bash版
claude -p "プロンプト1" --json > "$OUTPUT_DIR/result1.json" &
claude -p "プロンプト2" --json > "$OUTPUT_DIR/result2.json" &
```

## プロンプト設計のベストプラクティス

### 1. 具体的な指示

```
❌ 悪い例: "認証関連を調べて"
✅ 良い例: "src/auth/ディレクトリ内で、JWTトークンの検証を行う関数を列挙し、各関数の引数と戻り値を記載"
```

### 2. 出力形式の明示

```
❌ 悪い例: "結果を教えて"
✅ 良い例: "結果をJSON形式で出力。形式: {files: [{path, functions: [{name, params, returns}]}]}"
```

### 3. スコープの限定

```
❌ 悪い例: "プロジェクト全体を分析"
✅ 良い例: "src/widgets/ディレクトリのみを対象に、Signalを定義しているクラスを特定"
```

## 使用シナリオ例

### シナリオ1: 新機能実装前の調査

```powershell
# カスタムスクリプトを作成
$prompts = @{
    "existing_impl" = "src/内で類似機能の実装パターンを検索"
    "dependencies" = "requirements.txtから関連ライブラリを特定"
    "best_practices" = "PySide6での[機能名]実装のベストプラクティスを調査"
}
```

### シナリオ2: リファクタリング影響調査

```bash
claude -p "src/core/settings.pyを使用している全ファイルを列挙" --json &
claude -p "settings.pyの公開APIを抽出" --json &
claude -p "設定値の依存関係を図式化" --json &
```

### シナリオ3: コードレビュー支援

```powershell
$prompts = @{
    "security" = "変更されたファイルのセキュリティ問題を検出"
    "patterns" = "既存パターンとの整合性を確認"
    "performance" = "パフォーマンス上の懸念点を特定"
}
```

## 注意事項

1. **APIレート制限**: 並列実行数が多すぎるとレート制限に達する可能性あり
2. **コスト管理**: 各ヘッドレス呼び出しはAPIコストが発生
3. **タイムアウト**: 長時間実行タスクにはタイムアウト設定を追加
4. **結果の検証**: 統合前に各出力ファイルの内容を検証

## 結果の活用

### Claude Codeでの読み込み

```
parallel_research.ps1を実行した結果を読み込んで、
src/core/の構造を分析し、リファクタリング提案を作成して
```

### 結果ファイルの場所

| OS | デフォルト出力先 |
|-----|-----------------|
| Windows | `%TEMP%\claude_research\` |
| WSL/Linux/macOS | `/tmp/claude_research/` |

### 統合結果ファイル

`combined_research.md` に全結果が統合される。
