---
name: ue-log
description: View and filter UE log files
---

# /ue-log - UE Log Viewer

## Usage
```
/ue-log [--filter <category>] [--lines <count>]
```

## Description
View and filter Unreal Engine log files.

## Default Log Location
```
{{PROJECT_PATH}}/Saved/Logs/{{PROJECT_NAME}}.log
```

## Common Log Categories
- `LogTemp` - Temporary debug logs
- `LogBlueprintUserMessages` - Blueprint print logs
- `LogGameMode` - GameMode events
- `LogNet` - Network events

## Examples
```
/ue-log
/ue-log --filter LogTemp
/ue-log --lines 100
/ue-log --filter LogBlueprintUserMessages --lines 50
```
