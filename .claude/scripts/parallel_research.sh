#!/bin/bash
# parallel_research.sh
# 用途: 大規模タスクの並列調査（Bash版 - WSL/Linux/macOS）
#
# 使い方:
#   bash .claude/scripts/parallel_research.sh
#
# カスタマイズ:
#   PROMPTS配列のプロンプトをタスクに合わせて編集してください

set -e

OUTPUT_DIR="${CLAUDE_RESEARCH_DIR:-/tmp/claude_research}"
mkdir -p "$OUTPUT_DIR"

echo "=== 並列調査開始 ==="
echo "出力先: $OUTPUT_DIR"

# 並列実行するプロンプトを定義
# [カスタマイズ] 以下のプロンプトをタスクに合わせて編集してください

# プロンプト1: コード構造の調査
claude -p "src/core/ディレクトリで主要なクラスと関数を列挙し、それぞれの役割を簡潔に説明" \
  --json > "$OUTPUT_DIR/code_search.json" &
PID1=$!

# プロンプト2: パターン分析
claude -p "src/内で使用されているデザインパターンを特定し、各パターンの使用箇所を報告" \
  --json > "$OUTPUT_DIR/pattern_analysis.json" &
PID2=$!

# プロンプト3: ドキュメント要約
claude -p "CLAUDE.mdと.claude/rules/内のドキュメントを要約し、主要なルールを列挙" \
  --json > "$OUTPUT_DIR/doc_summary.json" &
PID3=$!

# 全プロセスの完了を待機
echo "調査中..."
wait $PID1
STATUS1=$?
wait $PID2
STATUS2=$?
wait $PID3
STATUS3=$?

# エラーチェック
FAILED=0
if [ $STATUS1 -ne 0 ]; then
    echo "警告: code_search が失敗しました"
    FAILED=1
fi
if [ $STATUS2 -ne 0 ]; then
    echo "警告: pattern_analysis が失敗しました"
    FAILED=1
fi
if [ $STATUS3 -ne 0 ]; then
    echo "警告: doc_summary が失敗しました"
    FAILED=1
fi

# 結果を統合
COMBINED="$OUTPUT_DIR/combined_research.md"
cat > "$COMBINED" << 'HEADER'
# 調査結果

HEADER

echo "生成日時: $(date '+%Y-%m-%d %H:%M:%S')" >> "$COMBINED"
echo "" >> "$COMBINED"
echo "---" >> "$COMBINED"
echo "" >> "$COMBINED"

# 各結果を追加
echo "## code_search" >> "$COMBINED"
echo "" >> "$COMBINED"
echo '```json' >> "$COMBINED"
cat "$OUTPUT_DIR/code_search.json" >> "$COMBINED" 2>/dev/null || echo "*結果なし*" >> "$COMBINED"
echo '```' >> "$COMBINED"
echo "" >> "$COMBINED"

echo "## pattern_analysis" >> "$COMBINED"
echo "" >> "$COMBINED"
echo '```json' >> "$COMBINED"
cat "$OUTPUT_DIR/pattern_analysis.json" >> "$COMBINED" 2>/dev/null || echo "*結果なし*" >> "$COMBINED"
echo '```' >> "$COMBINED"
echo "" >> "$COMBINED"

echo "## doc_summary" >> "$COMBINED"
echo "" >> "$COMBINED"
echo '```json' >> "$COMBINED"
cat "$OUTPUT_DIR/doc_summary.json" >> "$COMBINED" 2>/dev/null || echo "*結果なし*" >> "$COMBINED"
echo '```' >> "$COMBINED"
echo "" >> "$COMBINED"

echo "=== 調査完了 ==="
echo "統合結果: $COMBINED"
echo ""
echo "次のステップ:"
echo "  1. 結果ファイルを確認: cat '$COMBINED'"
echo "  2. Claude Codeで結果を使用: 'parallel_research.shの結果を読み込んで分析して'"

if [ $FAILED -ne 0 ]; then
    exit 1
fi
