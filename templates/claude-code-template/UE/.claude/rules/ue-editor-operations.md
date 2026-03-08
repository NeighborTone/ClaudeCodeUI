# UE Editor Manual Operations Rule (STRICT)

## Purpose

When code changes require manual operations in UE Editor (Blueprint creation, DataAsset configuration, etc.), those procedures MUST be strictly documented in the plan.

## Rules

| Rule | Content |
|------|---------|
| R-UE1 | Mandatory documentation of manual operations (table format) |
| R-UE2 | Step-by-step description (specific operation steps) |
| R-UE3 | Pair operations with verification (expected results) |
| R-UE4 | Specific value designation (all property values documented) |
| R-UE5 | Distinguish automatable/non-automatable (Claude Code vs User) |
| R-UE6 | Manual operation checklist at checkpoint completion |
| R-UE7 | Prevent .uasset/.umap commit omissions |

## Documentation Format

When UE Editor operations are required at a checkpoint, use this table format:

| Operation | Steps | Target/Save Path |
|-----------|-------|-----------------|
| Create DataTable | Right-click -> Miscellaneous -> Data Table -> Select row struct | `/Game/ProjectName/Data/DT_XXX` |
| Configure DataAsset | DA_Param -> Category -> Set property | `/Game/ProjectName/Data/DA_Param` |
| Create Blueprint | Right-click -> Blueprint Class -> Select parent | `/Game/ProjectName/BP/XXX/BP_XXX` |

## Violation Handling

Plans with insufficient manual operation documentation will fail `/check-plan` validation. Fixes required before committing.
