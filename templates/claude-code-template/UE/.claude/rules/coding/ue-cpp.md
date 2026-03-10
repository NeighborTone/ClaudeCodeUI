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

## UHT (Unreal Header Tool) Rules (MUST FOLLOW)

| Rule | Requirement | Reason |
|------|-------------|--------|
| `GENERATED_BODY()` position | First line in public section of UCLASS/USTRUCT | UHT code generation depends on this position |
| `.generated.h` include | **Must be the last #include** in the header file | UHT inserts generated code after this include |
| Never move `.generated.h` | Do not reorder to file top or among other includes | Causes compilation failure |
| Never delete `GENERATED_BODY()` | Do not remove or comment out | Breaks UHT reflection system |

### Correct Pattern
```cpp
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "MyActor.generated.h"  // MUST be last include

UCLASS()
class MYPROJECT_API AMyActor : public AActor
{
    GENERATED_BODY()  // MUST be first in class body

public:
    // ...
};
```

## Memory Management (GC)

| Rule | Detail |
|------|--------|
| UObject pointers | Must have `UPROPERTY()` to prevent GC collection |
| Raw UObject pointers without UPROPERTY | **Prohibited** - will be garbage collected silently |
| Non-UObject shared ownership | Use `TSharedPtr` / `TWeakPtr` |
| Container members | `TArray`, `TMap`, `TSet` holding UObject* must have `UPROPERTY()` |

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
