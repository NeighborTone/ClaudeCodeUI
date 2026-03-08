# Claude Code Template Setup Script (PowerShell)
# Interactive setup for configuring .claude directory in your project

param(
    [string]$TargetDir = ""
)

$ErrorActionPreference = 'Stop'

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Claude Code Template Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# --- Step 1: Target Directory ---
if (-not $TargetDir) {
    $TargetDir = Read-Host "Target project directory (full path)"
}

if (-not (Test-Path $TargetDir)) {
    Write-Host "ERROR: Directory does not exist: $TargetDir" -ForegroundColor Red
    exit 1
}

$TemplateDir = $PSScriptRoot

Write-Host ""
Write-Host "Target: $TargetDir" -ForegroundColor Green
Write-Host ""

# --- Step 2: Project Info ---
$ProjectName = Read-Host "Project name"
$ProjectDesc = Read-Host "Project description (1 line)"

# Language
Write-Host ""
Write-Host "Communication language options:" -ForegroundColor Yellow
Write-Host "  1. Japanese (default)"
Write-Host "  2. English"
$langChoice = Read-Host "Select [1/2]"
$UserLang = if ($langChoice -eq "2") { "English" } else { "Japanese" }
$CommentLang = if ($langChoice -eq "2") { "English" } else { "Japanese" }

# Tech stack
$Language = Read-Host "Programming language (e.g., Python, C++, TypeScript)"
$Framework = Read-Host "Framework (e.g., PySide6, React, UE5) [optional]"

# Build command
$BuildCommand = Read-Host "Build/verify command (e.g., 'npm run build', 'python main.py')"

# Quick start
Write-Host ""
Write-Host "Quick start commands (one per line, empty line to finish):" -ForegroundColor Yellow
$quickStartLines = @()
while ($true) {
    $line = Read-Host "  >"
    if ([string]::IsNullOrEmpty($line)) { break }
    $quickStartLines += $line
}
$QuickStart = $quickStartLines -join "`n"

# --- Step 3: Copy base template ---
Write-Host ""
Write-Host "Copying base template..." -ForegroundColor Yellow

$targetClaude = Join-Path $TargetDir ".claude"

# Check existing
if (Test-Path $targetClaude) {
    $overwrite = Read-Host ".claude directory already exists. Overwrite? [y/N]"
    if ($overwrite -ne "y" -and $overwrite -ne "Y") {
        Write-Host "Aborted." -ForegroundColor Red
        exit 0
    }
}

# Copy .claude directory
Copy-Item -Path (Join-Path $TemplateDir ".claude") -Destination $TargetDir -Recurse -Force

# Process CLAUDE.md template
$claudeMdTemplate = Get-Content (Join-Path $TemplateDir "CLAUDE.md.template") -Raw -Encoding UTF8
$claudeMd = $claudeMdTemplate `
    -replace '\{\{PROJECT_NAME\}\}', $ProjectName `
    -replace '\{\{PROJECT_DESCRIPTION\}\}', $ProjectDesc `
    -replace '\{\{USER_LANGUAGE\}\}', $UserLang `
    -replace '\{\{COMMENT_LANGUAGE\}\}', $CommentLang `
    -replace '\{\{BUILD_COMMAND\}\}', $BuildCommand `
    -replace '\{\{QUICK_START_COMMANDS\}\}', $QuickStart

$claudeMd | Set-Content (Join-Path $TargetDir "CLAUDE.md") -Encoding UTF8

# Process project overview template
$overviewTemplate = Get-Content (Join-Path $targetClaude "rules\01-project-overview.md.template") -Raw -Encoding UTF8
$overview = $overviewTemplate `
    -replace '\{\{PROJECT_DESCRIPTION\}\}', $ProjectDesc `
    -replace '\{\{LANGUAGE\}\}', $Language `
    -replace '\{\{FRAMEWORK\}\}', $Framework `
    -replace '\{\{QUICK_START_COMMANDS\}\}', $QuickStart `
    -replace '\{\{BUILD_COMMAND\}\}', $BuildCommand `
    -replace '\{\{FEATURE_1\}\}', '(TODO: Add feature 1)' `
    -replace '\{\{FEATURE_2\}\}', '(TODO: Add feature 2)' `
    -replace '\{\{FEATURE_3\}\}', '(TODO: Add feature 3)'

$overview | Set-Content (Join-Path $targetClaude "rules\01-project-overview.md") -Encoding UTF8
Remove-Item (Join-Path $targetClaude "rules\01-project-overview.md.template") -ErrorAction SilentlyContinue

# Process project structure template
$structTemplate = Get-Content (Join-Path $targetClaude "rules\02-project-structure.md.template") -Raw -Encoding UTF8
$struct = $structTemplate `
    -replace '\{\{PROJECT_NAME\}\}', $ProjectName `
    -replace '\{\{SOURCE_DIR\}\}', 'src' `
    -replace '\{\{CONFIG_DIR\}\}', 'config' `
    -replace '\{\{TEST_DIR\}\}', 'tests' `
    -replace '\{\{DOC_DIR\}\}', 'docs'

$struct | Set-Content (Join-Path $targetClaude "rules\02-project-structure.md") -Encoding UTF8
Remove-Item (Join-Path $targetClaude "rules\02-project-structure.md.template") -ErrorAction SilentlyContinue

# Update settings.json language
$settingsPath = Join-Path $targetClaude "settings.json"
$settings = Get-Content $settingsPath -Raw -Encoding UTF8
if ($UserLang -eq "English") {
    $settings = $settings -replace '"language": "japanese"', '"language": "english"'
}
$settings | Set-Content $settingsPath -Encoding UTF8

# Global template variable replacement across all .md and .json files in .claude
Write-Host "Applying template variables..." -ForegroundColor Yellow
$allTemplateFiles = Get-ChildItem $targetClaude -Recurse -File -Include *.md, *.json
foreach ($f in $allTemplateFiles) {
    $content = Get-Content $f.FullName -Raw -Encoding UTF8
    if ($content -match '\{\{') {
        $content = $content `
            -replace '\{\{PROJECT_NAME\}\}', $ProjectName `
            -replace '\{\{PROJECT_DESCRIPTION\}\}', $ProjectDesc `
            -replace '\{\{BUILD_COMMAND\}\}', $BuildCommand `
            -replace '\{\{SOURCE_DIR\}\}', 'Source' `
            -replace '\{\{USER_LANGUAGE\}\}', $UserLang `
            -replace '\{\{COMMENT_LANGUAGE\}\}', $CommentLang
        $content | Set-Content $f.FullName -Encoding UTF8
    }
}

Write-Host "Base template installed." -ForegroundColor Green

# --- Step 4: Addons ---
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Available Addons" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

$addonsDir = $TemplateDir
$addonDirs = Get-ChildItem $addonsDir -Directory -ErrorAction SilentlyContinue | Where-Object { $_.Name -ne ".claude" -and $_.Name -ne ".claude-plugin" }

if ($addonDirs) {
    foreach ($addon in $addonDirs) {
        Write-Host ""
        Write-Host "  [$($addon.Name)]" -ForegroundColor Yellow

        # Show contents
        $subDirs = Get-ChildItem $addon.FullName -Directory -ErrorAction SilentlyContinue
        foreach ($sub in $subDirs) {
            $files = Get-ChildItem $sub.FullName -Recurse -File | Select-Object -ExpandProperty Name
            Write-Host "    $($sub.Name)/: $($files -join ', ')" -ForegroundColor Gray
        }
    }

    Write-Host ""
    $installAddons = Read-Host "Install addons? (comma-separated, e.g., 'ue' or 'all' or 'none')"

    if ($installAddons -ne "none" -and -not [string]::IsNullOrEmpty($installAddons)) {
        $selectedAddons = if ($installAddons -eq "all") {
            $addonDirs | Select-Object -ExpandProperty Name
        } else {
            $installAddons -split ',' | ForEach-Object { $_.Trim() }
        }

        foreach ($addonName in $selectedAddons) {
            $addonPath = Join-Path $addonsDir $addonName
            if (-not (Test-Path $addonPath)) {
                Write-Host "  Addon '$addonName' not found, skipping." -ForegroundColor Yellow
                continue
            }

            Write-Host "  Installing addon: $addonName..." -ForegroundColor Yellow

            # UE addon specific configuration
            if ($addonName -eq "ue") {
                $ueVersion = Read-Host "    UE version (e.g., 5.5)"
                $ueEnginePath = Read-Host "    UE engine path (e.g., C:\EpicGames\UE_5.5)"
                $ueProjectPath = Read-Host "    UE project path (e.g., C:\Projects\MyGame\UE)"
            }

            # Copy addon files into .claude
            $addonSubDirs = Get-ChildItem $addonPath -Directory
            foreach ($sub in $addonSubDirs) {
                $targetSubDir = Join-Path $targetClaude $sub.Name
                if (-not (Test-Path $targetSubDir)) {
                    New-Item -ItemType Directory -Path $targetSubDir -Force | Out-Null
                }

                Get-ChildItem $sub.FullName -Recurse -File | ForEach-Object {
                    $relativePath = $_.FullName.Substring($sub.FullName.Length + 1)
                    $destPath = Join-Path $targetSubDir $relativePath
                    $destDir = Split-Path $destPath -Parent

                    if (-not (Test-Path $destDir)) {
                        New-Item -ItemType Directory -Path $destDir -Force | Out-Null
                    }

                    $content = Get-Content $_.FullName -Raw -Encoding UTF8

                    # Replace placeholders for UE addon
                    if ($addonName -eq "ue") {
                        $content = $content `
                            -replace '\{\{UE_VERSION\}\}', "UE $ueVersion" `
                            -replace '\{\{UE_ENGINE_PATH\}\}', $ueEnginePath `
                            -replace '\{\{PROJECT_NAME\}\}', $ProjectName `
                            -replace '\{\{PROJECT_PATH\}\}', $ueProjectPath
                    }

                    # Remove .template extension if present
                    if ($destPath.EndsWith(".template")) {
                        $destPath = $destPath.Substring(0, $destPath.Length - 9)
                    }

                    $content | Set-Content $destPath -Encoding UTF8
                }
            }

            Write-Host "  Addon '$addonName' installed." -ForegroundColor Green
        }
    }
}

# --- Step 4.5: Final global variable replacement (covers addon files) ---
Write-Host "Applying final template variables..." -ForegroundColor Yellow
$allFinalFiles = Get-ChildItem $targetClaude -Recurse -File -Include *.md, *.json
foreach ($f in $allFinalFiles) {
    $content = Get-Content $f.FullName -Raw -Encoding UTF8
    if ($content -match '\{\{') {
        $content = $content `
            -replace '\{\{PROJECT_NAME\}\}', $ProjectName `
            -replace '\{\{PROJECT_DESCRIPTION\}\}', $ProjectDesc `
            -replace '\{\{BUILD_COMMAND\}\}', $BuildCommand `
            -replace '\{\{SOURCE_DIR\}\}', 'Source' `
            -replace '\{\{USER_LANGUAGE\}\}', $UserLang `
            -replace '\{\{COMMENT_LANGUAGE\}\}', $CommentLang
        $content | Set-Content $f.FullName -Encoding UTF8
    }
}

# Copy .gitignore template if not present
$gitignoreTemplate = Join-Path $TemplateDir ".gitignore.template"
$gitignoreTarget = Join-Path $TargetDir ".gitignore"
if ((Test-Path $gitignoreTemplate) -and -not (Test-Path $gitignoreTarget)) {
    Copy-Item $gitignoreTemplate $gitignoreTarget
    Write-Host ".gitignore installed from template." -ForegroundColor Green
}

# --- Step 5: Summary ---
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Setup Complete!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Installed to: $TargetDir" -ForegroundColor Green
Write-Host ""
Write-Host "Files created:" -ForegroundColor Yellow

$allFiles = Get-ChildItem (Join-Path $TargetDir ".claude") -Recurse -File
foreach ($f in $allFiles) {
    $rel = $f.FullName.Substring($TargetDir.Length + 1)
    Write-Host "  $rel" -ForegroundColor Gray
}

$claudeMdPath = Join-Path $TargetDir "CLAUDE.md"
if (Test-Path $claudeMdPath) {
    Write-Host "  CLAUDE.md" -ForegroundColor Gray
}

Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Review and customize CLAUDE.md" -ForegroundColor White
Write-Host "  2. Edit .claude/rules/01-project-overview.md" -ForegroundColor White
Write-Host "  3. Edit .claude/rules/02-project-structure.md" -ForegroundColor White
Write-Host "  4. Configure build commands in skills/dev/ and skills/verify/" -ForegroundColor White
Write-Host "  5. Start Claude Code in your project: cd $TargetDir && claude" -ForegroundColor White
Write-Host ""
Write-Host "Plugin installation (alternative):" -ForegroundColor Yellow
Write-Host "  The template also supports Claude Code plugin format." -ForegroundColor White
Write-Host "  See .claude-plugin/plugin.json for details." -ForegroundColor White
Write-Host ""
