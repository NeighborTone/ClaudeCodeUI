---
paths:
  - "Source/**/*.h"
  - "Source/**/*.cpp"
---

# No Tick/Timer/Polling Rule

## Principle

Tick, Timer, and polling-based periodic execution are prohibited unless there is no alternative.
Use event-driven patterns (delegates, callbacks, message handlers) whenever possible.

## Prohibited Patterns

| Prohibited | Alternative |
|-----------|-------------|
| `NativeTick` to check state changes | Delegate/callback to notify changes |
| `FTimerHandle` for periodic polling | Event-based, process only when needed |
| `SetTimer` + loop for monitoring | OS message handler / UE delegate |
| Per-frame `GetXxx()` value comparison | Fire `OnXxxChanged` from the change source |

## Allowed Exceptions

The following cases permit Tick/Timer usage:

1. **Physics simulation**: Per-frame position/velocity updates are required
2. **Animation interpolation**: Frame-based Lerp/InterpTo operations
3. **Third-party API integration**: When no delegate/callback is provided
4. **Debug visualization**: On-screen debug drawing (excluded from Shipping builds)

## Decision Criteria

Before implementation, verify:

1. Does the change source have a delegate/event? → Use it
2. Can it be detected via OS-level events (Windows messages, etc.)? → Use it
3. Can it be detected via UE callbacks (`OnXxx` delegates)? → Use it
4. Only consider Timer if ALL of the above are impossible

## Bad Example: Timer-based monitoring

```cpp
// NG: Polling every second
World->GetTimerManager().SetTimer(Handle, this, &ThisClass::CheckSomethingChanged, 1.0f, true);
```

## Good Example: Event-driven detection

```cpp
// OK: Handle delegate and respond to actual change
SomeSubsystem->OnSomethingChanged.AddDynamic(this, &ThisClass::HandleSomethingChanged);
```
