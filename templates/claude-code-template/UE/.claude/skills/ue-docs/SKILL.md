---
name: ue-docs
description: Search UE documentation and engine source
---

# /ue-docs - UE Documentation Search

## Usage
```
/ue-docs <search_query>
```

## Description
Search Unreal Engine documentation and source code for API references,
implementation patterns, and best practices.

## Workflow
1. Launch `ue-explore` agent with the search query
2. Agent searches engine source and documentation
3. Return findings with code references

## Agent
Uses: `ue-explore` agent

## Examples
```
/ue-docs FTimerManager usage
/ue-docs how to create custom subsystem
/ue-docs SetWindowPos transparent window
```
