---
name: build-upload
description: Build all targets and upload binaries
allowed-tools: Bash(Build.bat:*), Bash(powershell:*), Read, AskUserQuestion
---

# Build & Upload

## Usage
```
/build-upload
```

## Description
全ターゲットのビルド → バイナリアップロードを実行する。

## Workflow

### Phase 1: Full Build

全ターゲットをビルド:

```powershell
# ビルドスクリプトを実行（プロジェクトに応じてカスタマイズ）
powershell.exe -File "{{PROJECT_PATH}}/Scripts/Build_All.ps1"
```

**ターゲット例:**
- {{PROJECT_NAME}}Editor Win64 Development
- {{PROJECT_NAME}} Win64 Development
- {{PROJECT_NAME}} Win64 DebugGame
- {{PROJECT_NAME}} Win64 Shipping

**ビルド失敗時**: エラーログを報告して停止。アップロードは実行しない。

**ビルドログ確認（失敗時）:**
```powershell
powershell.exe -Command "Get-ChildItem '{{PROJECT_PATH}}/Saved/Logs/Build' | Sort-Object LastWriteTime -Descending | Select-Object -First 4 | ForEach-Object { Write-Host $_.Name; Get-Content $_.FullName | Select-Object -Last 10; Write-Host '' }"
```

### Phase 2: Upload (ビルド成功後、ユーザー確認後に実行)

ビルド成功後、`AskUserQuestion` でアップロードするか確認する。

```bash
# アップロードコマンド（プロジェクトに応じてカスタマイズ）
# 例: Dropbox, S3, ネットワークドライブなど
```

## Important Notes
- UEエディタが起動中の場合、Editorビルドが失敗する可能性がある
- ビルドスクリプトのパスはプロジェクトに応じて調整すること
