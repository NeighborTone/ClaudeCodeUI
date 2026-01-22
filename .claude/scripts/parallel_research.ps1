# parallel_research.ps1
# 用途: 大規模タスクの並列調査（Windows PowerShell版）
#
# 使い方:
#   .\parallel_research.ps1
#
# カスタマイズ:
#   $prompts配列のプロンプトをタスクに合わせて編集してください

param(
    [string]$OutputDir = "$env:TEMP\claude_research",
    [switch]$Verbose
)

# 出力ディレクトリを作成
New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null

Write-Host "=== 並列調査開始 ===" -ForegroundColor Cyan
Write-Host "出力先: $OutputDir" -ForegroundColor Gray

# 並列実行するプロンプトを定義
# [カスタマイズ] 以下のプロンプトをタスクに合わせて編集してください
$prompts = @{
    "code_search" = "src/core/ディレクトリで主要なクラスと関数を列挙し、それぞれの役割を簡潔に説明"
    "pattern_analysis" = "src/内で使用されているデザインパターンを特定し、各パターンの使用箇所を報告"
    "doc_summary" = "CLAUDE.mdと.claude/rules/内のドキュメントを要約し、主要なルールを列挙"
}

$jobs = @()

# 各プロンプトを並列実行
foreach ($key in $prompts.Keys) {
    $prompt = $prompts[$key]
    $outputFile = "$OutputDir\$key.json"

    if ($Verbose) {
        Write-Host "起動: $key" -ForegroundColor Yellow
    }

    $jobs += Start-Job -ScriptBlock {
        param($prompt, $outputFile)
        claude -p $prompt --json > $outputFile 2>&1
    } -ArgumentList $prompt, $outputFile
}

# 全ジョブの完了を待機
Write-Host "調査中..." -ForegroundColor Gray
$jobs | Wait-Job | Out-Null

# エラーチェック
$failed = @()
foreach ($job in $jobs) {
    if ($job.State -eq 'Failed') {
        $failed += $job.Name
    }
}

if ($failed.Count -gt 0) {
    Write-Host "警告: 一部の調査が失敗しました" -ForegroundColor Yellow
    foreach ($name in $failed) {
        Write-Host "  - $name : 失敗" -ForegroundColor Red
    }
}

$jobs | Remove-Job

# 結果を統合
$Combined = "$OutputDir\combined_research.md"
$content = @"
# 調査結果

生成日時: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

---

"@

foreach ($key in $prompts.Keys) {
    $outputFile = "$OutputDir\$key.json"
    $content += "## $key`n`n"

    if (Test-Path $outputFile) {
        $content += "``````json`n"
        $content += (Get-Content $outputFile -Raw -ErrorAction SilentlyContinue)
        $content += "`n```````n`n"
    } else {
        $content += "*結果ファイルが見つかりません*`n`n"
    }
}

$content | Set-Content $Combined -Encoding UTF8

Write-Host "=== 調査完了 ===" -ForegroundColor Cyan
Write-Host "統合結果: $Combined" -ForegroundColor Green
Write-Host ""
Write-Host "次のステップ:" -ForegroundColor Yellow
Write-Host "  1. 結果ファイルを確認: Get-Content '$Combined'" -ForegroundColor Gray
Write-Host "  2. Claude Codeで結果を使用: 'parallel_research.ps1の結果を読み込んで分析して'" -ForegroundColor Gray
