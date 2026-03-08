---
name: profile
description: UE Standalone profiling - monitor memory, CPU, GPU usage
allowed-tools: Bash(powershell:*), Read
argument-hint: "[minutes|analyze|launch|insights]"
---

# /profile - UE Profiling

UE Standaloneを起動し、メモリ・CPU・GPU使用率を監視・分析する。

## Subcommands

### /profile [minutes] (default)

Standaloneを起動し、指定分数監視する。

- 引数なし: 5分間監視
- 数値: 指定分数監視（例: `/profile 10` で10分）

**実行:**
```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "{{PROJECT_PATH}}/Scripts/ProfileMonitor.ps1" -DurationMin $ARGUMENTS
```

**出力:** `{{PROJECT_PATH}}/Saved/Profiling/External_*.csv`

### /profile analyze

プロファイリングデータを分析し、診断レポートを生成する。

**出力:**
- 総合判定（OK/WARNING/CRITICAL）
- メトリクス分析
- 検出された問題
- 改善提案

### /profile launch

トレース有効でStandaloneを起動する。

**実行:**
```powershell
& "{{UE_ENGINE_PATH}}/Engine/Binaries/Win64/UnrealEditor.exe" "{{PROJECT_PATH}}/{{PROJECT_NAME}}.uproject" -game -trace=cpu,gpu,frame,memory,bookmark
```

**出力:** `{{PROJECT_PATH}}/Saved/TraceSessions/*.utrace`

### /profile insights

Unreal Insights GUIを起動する。

**実行:**
```powershell
& "{{UE_ENGINE_PATH}}/Engine/Binaries/Win64/UnrealInsights.exe"
```

## Result Format

```
## Profiling Results

| Item | Initial | Final | Change | Status |
|------|---------|-------|--------|--------|
| Memory | XXX MB | XXX MB | +XX MB | OK/NG |
| CPU | - | XX% avg | - | OK/NG |
| GPU | - | XX% avg | - | OK/NG |
| VRAM | XXX MB | XXX MB | +XX MB | - |

### Thresholds
- Memory: +100MB/hour = NG
- CPU: idle > 1% = NG
- GPU: idle > 10% = NG
```
