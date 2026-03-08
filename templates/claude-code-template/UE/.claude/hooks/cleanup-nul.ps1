# cleanup-nul.ps1
# PostToolUse hook: Auto-delete nul files after Write/Edit/Bash
# Reads JSON (tool_input) from stdin, checks target directories

$ErrorActionPreference = 'SilentlyContinue'

# Read JSON from stdin
$jsonInput = [Console]::In.ReadToEnd()

$dirsToCheck = @()

try {
    $parsed = $jsonInput | ConvertFrom-Json

    # file_path present (Write/Edit) -> check that directory
    if ($parsed.tool_input.file_path) {
        $dir = Split-Path $parsed.tool_input.file_path -Parent
        if ($dir) { $dirsToCheck += $dir }
    }

    # command present (Bash) -> check CWD
    if ($parsed.tool_input.command) {
        if ($parsed.cwd) { $dirsToCheck += $parsed.cwd }
    }
}
catch {
    # Ignore JSON parse failures
}

# Always check project root
if ($env:CLAUDE_PROJECT_DIR) {
    $dirsToCheck += $env:CLAUDE_PROJECT_DIR
}

# Deduplicate
$dirsToCheck = $dirsToCheck | Select-Object -Unique

foreach ($dir in $dirsToCheck) {
    if (-not $dir) { continue }
    $uncPath = "\\?\$dir\nul"
    if ([System.IO.File]::Exists($uncPath)) {
        try {
            [System.IO.File]::Delete($uncPath)
            Write-Host "nul file deleted: $dir\nul" -ForegroundColor Yellow
        }
        catch {
            # Ignore deletion failures (will be handled next cleanup)
        }
    }
}

exit 0
