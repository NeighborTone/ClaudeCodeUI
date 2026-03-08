# nul File Cleanup

## Problem

On Windows, redirecting Bash output to `nul` can create an actual file named `nul` instead of the NUL device.
This file cannot be deleted through normal methods due to Windows reserved name restrictions.

## Prevention Rules (MUST FOLLOW)

### Output Suppression in Bash Tool

| Prohibited | Correct | Reason |
|-----------|---------|--------|
| `> nul` | `> /dev/null` | Use Unix-style in bash |
| `2> nul` | `2> /dev/null` | Same for stderr |
| `> nul 2>&1` | `> /dev/null 2>&1` | Same |

### PowerShell Usage

| Prohibited | Correct | Reason |
|-----------|---------|--------|
| `> nul` | `> $null` | Use PowerShell's `$null` |
| `2> nul` | `2> $null` | Same for stderr |
| `command > nul` | `command | Out-Null` | PowerShell style |

## Auto Cleanup

### PostToolUse Hook

Configured in `.claude/settings.json`. Automatically checks and deletes nul files after Write/Edit tool execution.

### Manual Cleanup

```powershell
# Delete nul file using UNC path
[System.IO.File]::Delete("\\?\$(Get-Location)\nul")
```

## File Structure

| File | Role |
|------|------|
| `.claude/hooks/cleanup-nul.ps1` | PostToolUse hook script |
