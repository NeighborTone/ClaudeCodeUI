# /verify - Build Verification

Run build verification only.

## Usage

```
/verify
```

## Workflow

1. Execute build command
2. Check output for errors and warnings
3. Report build status

## Output Format

```
VERIFY: [SUCCESS/FAILED]
- Errors: [count]
- Warnings: [count]
- Details: [if errors, list with file:line]
```
