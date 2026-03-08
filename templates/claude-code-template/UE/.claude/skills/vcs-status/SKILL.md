---
name: vcs-status
description: Show version control status and pending changes
allowed-tools: Bash(git:*)
---

# VCS Status

## Usage
```
/vcs-status
```

## Description
バージョン管理の状態と保留中の変更を表示します。

## Commands

### Quick Status
```bash
git status
```

### Detailed Status
```bash
# Show all changes with details
git status -v

# Show specific path
git status -- "{{SOURCE_DIR}}/"
```

### Show Diff
```bash
# All unstaged changes
git diff

# All staged changes
git diff --cached

# Specific file
git diff "path/to/file"
```

### History
```bash
# Recent commits (last 7 days)
git log --oneline --since="7 days ago"

# File history
git log --oneline -- "path/to/file"
```

### Branch Info
```bash
git branch -v
git log --oneline -5
```

## Output Interpretation
- `M ` - Modified (staged)
- ` M` - Modified (unstaged)
- `A ` - Added (staged)
- `D ` - Deleted
- `??` - Untracked (新規)
- `R ` - Renamed
