---
paths:
  - "{{SOURCE_DIR}}/**/*.h"
  - "{{SOURCE_DIR}}/**/*.cpp"
---

# Debug Output Guidelines

## Principle

UE Standaloneモードでは OutputLog が表示されないため、`UE_LOG` によるデバッグは非効率。
画面上のデバッグ表示またはプロジェクト固有のデバッグシステムを使用する。

## Standalone Mode Considerations

| Mode | OutputLog | On-Screen Debug |
|------|----------|-----------------|
| PIE (Play In Editor) | Visible | Visible |
| **Standalone** | Not visible | **Only way to debug** |
| Packaged Build | Not visible | **Only way to debug** |

## Recommended Debug Methods

### 1. GEngine->AddOnScreenDebugMessage
```cpp
#if !UE_BUILD_SHIPPING
if (GEngine)
{
    GEngine->AddOnScreenDebugMessage(-1, 5.f, FColor::Yellow, TEXT("Debug message"));
}
#endif
```

### 2. Project Debug Subsystem (if available)
```cpp
#if !UE_BUILD_SHIPPING
if (auto* DebugSub = GetWorld()->GetSubsystem<UMyDebugSubsystem>())
{
    DebugSub->AddText(TEXT("Category"), TEXT("Key"), TEXT("Value"));
}
#endif
```

### 3. UE_LOG (limited use)
UE_LOG is acceptable for:

| Allowed | Condition |
|---------|-----------|
| System initialization | Startup only (once) |
| Fatal errors | Before crash |
| System logs | Non-debug purpose |

## Shipping Build Exclusion

All debug code MUST be wrapped:
```cpp
#if !UE_BUILD_SHIPPING
    // debug code here
#endif
```

## UE Log File Locations

| File | Purpose |
|------|---------|
| `Saved/Logs/{{PROJECT_NAME}}.log` | Editor log |
| `Saved/Logs/{{PROJECT_NAME}}_2.log` | Standalone log |

### Log Check Commands
```powershell
# Latest 50 lines of Standalone log
powershell.exe -Command "Get-Content '{{PROJECT_PATH}}/Saved/Logs/{{PROJECT_NAME}}_2.log' -Tail 50"

# Filter by keyword
powershell.exe -Command "Select-String -Path '{{PROJECT_PATH}}/Saved/Logs/{{PROJECT_NAME}}_2.log' -Pattern 'Error|Warning' | Select-Object -Last 30"
```
