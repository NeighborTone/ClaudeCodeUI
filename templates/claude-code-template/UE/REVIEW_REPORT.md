# Claude Code Template for UE - Evaluation Report

**Date**: 2026-03-10
**Reviewers**: Claude Opus 4.6 + Gemini 3.1 Pro Preview (Dialogue-based review)
**Target**: `templates/claude-code-template/UE/`

---

## Summary

| Item | Score | Consensus Comment |
| :--- | :---: | :--- |
| 1. Structure Design | **8.5/10** | Excellent base structure, but `.claudeignore` for UE's massive generated folders is essential |
| 2. Rule Quality | **8.0/10** | UHT constraints (`.generated.h` position, `GENERATED_BODY()` placement) must be documented |
| 3. Skill Design | **8.0/10** | Existing skills work, but UE Automation Test framework strategy/skill is missing |
| 4. Agent Design | **8.5/10** | Good responsibility separation, but hook failure fallback definitions are weak |
| 5. Workflow Design | **8.5/10** | Refined overall flow, but async error handling asymmetry remains |
| 6. Cross-Platform | **8.0/10** | Windows path length is hard to fully solve; operational warning in CLAUDE.md is pragmatic |
| 7. Template Variables | **9.0/10** | Sufficient customizability through variable expansion |
| 8. Plugin Support | **9.0/10** | Extensible plugin structure is highly commendable |
| 9. Practicality | **8.5/10** | Works as-is, but index optimization and C++ compile error prevention rules needed for production |
| **10. Overall** | **8.5/10** | **Strong foundation; needs defensive design reinforcement for UE-specific pitfalls** |

---

## Detailed Evaluation

### 1. Structure Design (8.5/10)

**Strengths (Both agree):**
- Follows Claude Code's recommended directory structure (`agents`, `commands`, `rules`, `skills`) precisely
- Clean separation of project-specific settings (`01-project-overview.md`) and universal rules (`core-rules.md`)
- `plan/task/done/` archive pattern prevents directory clutter

**Issues identified:**

| Issue | Identified by | Severity |
|-------|--------------|----------|
| Core/UE-Specific not fully separated; manual deletion needed for Core-only use | Claude | Medium |
| `settings.json` hooks hardcoded; no merge logic when adding addons | Claude | Medium |
| Missing `.claudeignore` for UE build artifacts (Intermediate, Saved, DerivedDataCache = multi-GB) | Gemini | **Critical** |

### 2. Rule Quality (8.0/10)

**Strengths (Both agree):**
- "Banned Phrases" in core-rules.md reduces wasted LLM tokens
- `no-tick-polling.md` and `debug-output.md` block common AI anti-patterns in UE
- `ue-editor-operations.md` forces documentation of GUI operations, preventing asset commit omissions

**Issues identified:**

| Issue | Identified by | Severity |
|-------|--------------|----------|
| `ue-cpp.md` too basic; missing GC rules (`UPROPERTY()` on UObject pointers) | Gemini | High |
| Missing Blueprint Interface usage guidelines and UCLASS specifier selection criteria | Claude | High |
| UHT boilerplate protection missing (`.generated.h` must be last include, `GENERATED_BODY()` in public) | Gemini + Claude | **Critical** |
| R11 (No Plan Mode) is Claude Code-specific; reduces template generality | Claude | Low |
| Checkpoint granularity contradiction between `checkpoint-workflow.md` and `plan-management.md` | Claude | Medium |

### 3. Skill Design (8.0/10)

**Strengths (Both agree):**
- `checkin` forces build verification before commit
- `drawio-verify` enables visual self-verification via PNG export
- `ue-docs` searches engine source for latest UE5 API patterns

**Issues identified:**

| Issue | Identified by | Severity |
|-------|--------------|----------|
| `verify`/`dev` skills have no actual build command implementation | Claude | High |
| `bp-analyze` depends on `unreal_asset_parser` with no fallback | Gemini | Medium |
| `read-excel` lacks context explanation (DataTable import use case) | Claude | Low |
| No UE Automation Test framework integration skill | Claude | Medium |

### 4. Agent Design (8.5/10)

**Strengths (Both agree):**
- Appropriate model selection by task complexity: `haiku` for build/QA, `sonnet` for debugging/research
- `plan-continuity-checker` agent for self-reviewing plan completeness is excellent
- Cost-performance optimization through model tiering

**Issues identified:**

| Issue | Identified by | Severity |
|-------|--------------|----------|
| Model aliases (`haiku`, `sonnet`) may break on future API changes | Gemini | Low |
| Hook failure fallback behavior undefined | Claude | Medium |

### 5. Workflow Design (8.5/10)

**Strengths (Both agree):**
- `XX_progress.md` state management enables context-loss recovery (Handoff)
- R16 (user permission before commit) prevents runaway behavior
- Structured checkpoint completion reports with implementation summaries

**Issues identified:**

| Issue | Identified by | Severity |
|-------|--------------|----------|
| `XX_progress.md` can bloat over long tasks, increasing token cost | Gemini | Medium |
| Checkpoint granularity guidelines contradict between two docs | Claude | Medium |

### 6. Cross-Platform Support (8.0/10)

**Strengths (Both agree):**
- Windows NUL file cleanup hook is a battle-tested solution
- Dual setup scripts (`.ps1` + `.sh`)
- Cross-platform hook scripts (`.ps1` + `.sh` variants)

**Issues identified:**

| Issue | Identified by | Severity |
|-------|--------------|----------|
| Build commands in rules/config assume `Build.bat` (Windows-only) | Gemini | Medium |
| `setup.sh` uses `sed -i` incompatible with macOS BSD sed | Claude | **Critical** |
| `plugin.json` hooks specify PowerShell only; no OS branching | Claude | High |
| Windows MAX_PATH (260 chars) risk with deep plan directory nesting | Gemini | Low |

### 7. Template Variable Design (9.0/10)

**Strengths (Both agree):**
- Comprehensive variable set covering project name, build commands, language preferences
- Interactive setup prompts for smooth configuration

**Issues identified:**

| Issue | Identified by | Severity |
|-------|--------------|----------|
| `setup.ps1` replaces all `.md`/`.json` files indiscriminately; risk of false matches on `{{...}}` | Gemini | Medium |
| `SOURCE_DIR` hardcoded to `src` in setup.ps1, but `Source` in global replacement - **inconsistency/bug** | Claude | **Critical** |

### 8. Plugin Support (9.0/10)

**Strengths (Both agree):**
- `.claude-plugin/plugin.json` enables `/plugin install` distribution
- Well-structured manifest declaring all skills, agents, and hooks

**Issues identified:**

| Issue | Identified by | Severity |
|-------|--------------|----------|
| `CLAUDE_PLUGIN_ROOT` path resolution needs testing documentation | Gemini | Low |

### 9. Practicality (8.5/10)

**Strengths (Both agree):**
- Extracted from production UE project - battle-tested patterns
- Core/Addon separation allows reuse for non-UE projects
- Comprehensive command reference in CLAUDE.md

**Issues identified:**

| Issue | Identified by | Severity |
|-------|--------------|----------|
| High rule file count increases startup token consumption | Gemini | Medium |
| Missing test strategy (UE Automation Test integration) | Claude | Medium |

---

## Critical Bugs Found

| # | Bug | Location | Fix |
|---|-----|----------|-----|
| 1 | `SOURCE_DIR` set to `src` instead of `Source` | `setup.ps1:112` | Change `'src'` to `'Source'` |
| 2 | `sed -i` incompatible with macOS BSD sed | `setup.sh:113,117-121,127-136,229-238` | Use `sed -i.bak` + cleanup, or use perl |
| 3 | Checkpoint granularity contradiction | `plan-management.md` vs `checkpoint-workflow.md` | Unify to single source of truth |

---

## Priority Action Items (Impact x Effort)

### P1: Critical & Quick Wins (High Impact, Low Effort)

1. **Fix `SOURCE_DIR` bug in `setup.ps1`** - Change `'src'` to `'Source'` (1-line fix)
2. **Fix `sed -i` cross-platform issue in `setup.sh`** - Use `sed -i.bak` or perl alternative
3. **Unify checkpoint granularity guidelines** - Single source of truth in one file
4. **Add UHT header rules to `ue-cpp.md`** - `.generated.h` position, `GENERATED_BODY()` rules

### P2: Core Infrastructure (High Impact, Medium Effort)

5. **Add `.claudeignore` with UE exclusions** - `Intermediate/`, `Saved/`, `DerivedDataCache/`, `Binaries/`
6. **OS-specific plugin hook branching** - Cross-platform entry point or conditional hook commands
7. **Blueprint/C++ boundary rules** - UCLASS specifiers, Blueprint Interface guidelines
8. **`settings.json` safe merge mechanism** - JSON parser-based merge in setup scripts

### P3: Architecture & Polish (Medium Impact, Higher Effort)

9. **Complete Core/UE-Specific separation** - Independent core template + UE addon
10. **Implement `verify`/`dev` skill build commands** - UnrealBuildTool invocation scripts
11. **Add UE Automation Test strategy/skill** - `FAutomationTestBase` integration guidelines
12. **Token optimization** - Lazy-load secondary rules, compress completed phases in progress files
13. **Add Excel reader context** - Document DataTable import use case in skill description

---

## Dialogue Highlights

### On Structure (Gemini initial: 5/5 -> Consensus: 8.5/10)

> **Gemini (Round 1):** "Ideal module composition. No issues found."
>
> **Claude (Round 2):** "Core/UE separation is incomplete. settings.json has no merge logic for addons."
>
> **Gemini (Round 2):** "Fully agree. The 'all-in-one' approach is easy for initial setup but lacks scalability. JSON merge via jq or PowerShell's ConvertFrom-Json is needed."
>
> **Claude (Round 3):** "Also, .claudeignore is critical - UE Intermediate alone is multi-GB."
>
> **Gemini (Round 3):** "Agreed. This is the highest priority infrastructure fix."

### On SOURCE_DIR Bug (Claude discovery)

> **Claude (Round 2):** "setup.ps1 sets SOURCE_DIR to 'src', but global replacement uses 'Source'. This is clearly a bug for UE projects."
>
> **Gemini (Round 2):** "Excellent code reading. This is a critical bug that directly causes C++ module recognition failure."

### On Cross-Platform sed (Claude discovery)

> **Claude (Round 2):** "macOS sed requires backup extension with -i. This is a cross-platform defect."
>
> **Gemini (Round 2):** "Strongly agree. Classic pitfall in cross-platform scripts. Must fix."

### On UHT Rules (Gemini discovery)

> **Gemini (Round 2):** "LLMs frequently move .generated.h to file top or delete GENERATED_BODY(). Missing strong absolute rules for these."
>
> **Claude (Round 3):** "Strongly agree. Add: 'GENERATED_BODY() must be first in public section' and '.generated.h must be last include'."

---

## Conclusion

This template represents a **mature, production-extracted engineering solution** for integrating Claude Code with Unreal Engine projects. The checkpoint workflow, handoff validation, and NUL file cleanup demonstrate deep practical experience.

The primary gaps are:
1. **UE-specific defensive rules** (UHT, GC, Blueprint boundaries)
2. **Cross-platform reliability** (sed, plugin hooks, build commands)
3. **Index/context management** (.claudeignore for multi-GB artifacts)

Addressing the 4 P1 items and 4 P2 items would elevate this from an **8.5/10 strong template** to a **production-grade industry reference**.
