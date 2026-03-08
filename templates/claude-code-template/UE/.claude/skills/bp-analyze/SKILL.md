---
name: bp-analyze
description: Analyze Unreal Engine Blueprint assets
---

# /bp-analyze - Blueprint Analyzer

## Usage
```
/bp-analyze <uasset_path> [--mode <mode>]
```

## Modes
| Mode | Description |
|------|-------------|
| `hierarchy` | Show class inheritance tree |
| `references` | List asset references |
| `components` | List components |
| `variables` | List variables and properties |
| `all` | Full analysis (default) |

## Description
Analyze UE Blueprint assets (.uasset) to extract structural information.
Uses Python scripts for asset parsing.

## Requirements
- Python 3.x
- `unreal_asset_parser` or direct binary parsing

## Examples
```
/bp-analyze Content/BP/BP_MyActor.uasset
/bp-analyze Content/BP/BP_MyActor.uasset --mode hierarchy
```
