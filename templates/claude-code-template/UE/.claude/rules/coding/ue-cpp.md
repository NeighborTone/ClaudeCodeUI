# UE C++ Coding Rules

## Naming Conventions

| Type | Convention | Example |
|------|-----------|---------|
| Class | A/U/F prefix | `AMyActor`, `UMyComponent`, `FMyStruct` |
| Interface | I prefix | `IMyInterface` |
| Enum | E prefix | `EMyEnum` |
| Boolean | b prefix | `bIsVisible` |

## Required Macros

- `GENERATED_BODY()` in every UCLASS/USTRUCT
- `UPROPERTY()` for reflected properties
- `UFUNCTION()` for reflected functions

## Module Dependencies

- Add dependencies in `ProjectName.Build.cs`
- Use `PublicDependencyModuleNames` for public dependencies
- Use `PrivateDependencyModuleNames` for private dependencies

## Common Patterns

### GameInstance Usage
```cpp
// Get GameInstance
auto* GI = GetGameInstance<UMyGameInstance>();
```

### Subsystem Access
```cpp
// Get subsystem
auto* Sub = GetWorld()->GetSubsystem<UMySubsystem>();
```

### Delegate Declaration
```cpp
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnEventTriggered, FName, EventName);
```
