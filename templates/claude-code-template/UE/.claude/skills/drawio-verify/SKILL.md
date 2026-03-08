---
name: drawio-verify
description: Export draw.io to PNG and visually verify
context: current
---

# draw.io Verify

## Usage
```
/drawio-verify <drawio_file_path>
```

## Description
Export draw.io files to PNG and perform visual verification.
Suggest fixes if layout issues are detected.

## Prerequisites

**Must read `.claude/refs/drawio-rules.md` first and follow its rules.**

## Workflow

```
1. Read .claude/refs/drawio-rules.md
2. Get drawio file path from argument
3. Execute PNG export
4. Read image for visual verification
5. Check against drawio-rules.md checklist
6. Report issues if any
7. Report completion if no issues
```

## Export Command

```powershell
powershell.exe -Command "& 'C:\Program Files\draw.io\draw.io.exe' --export --format png --output '<output_path>.png' '<input_path>.drawio'"
```

## Check Points

| Item | Verification |
|------|-------------|
| Font | Japanese text displays correctly |
| Arrows | Correct positions, not overlapping elements |
| Layout | Clear hierarchy, logical element placement |
| Text | No unintended line breaks |
| Connections | Parent-child relationships visually correct |

## Output
- PNG file path
- Visual verification results
- Issue list (if any)

## Rules Reference
- `.claude/refs/drawio-rules.md` - draw.io authoring rules (required reference)
