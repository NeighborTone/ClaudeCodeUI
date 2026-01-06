---
paths: src/**/*.py
---

# Testing Protocol

## Mandatory Testing Requirements
1. Test after EVERY code edit
2. Verify startup without errors
3. Check log output for warnings
4. Confirm existing functionality intact

## Test Execution

### Basic Startup Test
```bash
# WSL (recommended)
LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 python3 main.py

# Windows
python main.py
```

### Expected Results
- Application window appears
- No errors in console
- No warnings in log output
- All components initialize correctly

## GUI Testing Strategy

### Logging-Based Validation
Since direct GUI automation is challenging:
- Inject diagnostic logs throughout application
- Monitor component initialization
- Track signal-slot communications
- Verify state changes through log output

### Test Checklist
- [ ] Application starts without errors
- [ ] File tree loads correctly
- [ ] Theme switching works
- [ ] File completion triggers on @/!/#
- [ ] Template selection updates preview
- [ ] Token counter updates in real-time
- [ ] Settings persist across restarts

## Error Recovery Testing
Test graceful degradation for:
- Missing dependencies (watchdog)
- Corrupted configuration files
- Inaccessible workspace paths
- Invalid file patterns

## Performance Monitoring
- Startup time should be < 3 seconds
- Search response should be < 10ms
- UI should remain responsive during indexing
