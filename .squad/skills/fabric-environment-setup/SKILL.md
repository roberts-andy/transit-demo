---
name: "fabric-environment-setup"
description: "Define and validate the Microsoft Fabric environment for the transit demo, including capacity choice, workspace setup, item naming, Git alignment, parameterization, and demo-readiness constraints. Use when standing up or reviewing the foundational environment before implementation work begins."
domain: "platform-setup"
confidence: "high"
source: "manual"
tools:
  - name: "Git"
    description: "Version control and repo initialization"
    when: "When aligning workspace artifacts, repo structure, and source control expectations"
  - name: "Fabric"
    description: "Microsoft Fabric workspace and item platform"
    when: "When defining workspace, Lakehouse, Warehouse, Eventhouse, Dataflow Gen2, Pipelines, Notebooks, and Eventstream setup"
---

## Context

This skill applies whenever the squad needs to define, review, or stabilize the Microsoft Fabric environment for the transit demo.

The transit demo is not a production system. The environment should therefore optimize for:
- clarity of the demo story
- repeatability
- low setup friction
- portability across demo environments
- minimal hardcoded assumptions

This skill should be used before major implementation begins and whenever environment drift or ambiguity appears.

## Patterns

### 1. Treat environment setup as an explicit design activity
Before implementation, define:
- the intended Fabric capacity choice
- the workspace name
- the required Fabric item types
- the naming convention for artifacts
- the source control strategy
- the parameterization strategy

Do not allow implementation to proceed with vague environment assumptions.

### 2. Optimize for demo simplicity, not production over-engineering
Prefer a setup that is:
- easy for another field engineer to reproduce
- easy to explain to a customer
- small enough to maintain
- clear enough that each Fabric workload has a visible role

Do not introduce unnecessary complexity such as multi-workspace segmentation, advanced deployment topology, or production-style hardening unless explicitly requested.

### 3. Define the required Fabric artifacts up front
At minimum, identify and document:
- Bronze Lakehouse
- Silver Lakehouse
- Gold Warehouse
- Eventhouse or equivalent real-time store if required by the real-time demo path
- Notebook items
- Data Pipeline items
- Dataflow Gen2 items
- Eventstream items
- Materialized Lake View target objects

### 4. Parameterize environment-specific values
All environment-specific values must be externalized into config or parameter files rather than embedded in implementation logic.

Parameterize items such as:
- workspace ID
- workspace name
- Lakehouse names
- Warehouse name
- Eventhouse name
- source endpoint roots
- environment mode (live vs cached)

### 5. Keep naming predictable and demo-friendly
Use names that are:
- obvious to a customer or field engineer
- aligned to the Bronze / Silver / Gold story
- stable across assets

Preferred naming style:
- lh_transit_bronze
- lh_transit_silver
- wh_transit_gold
- eh_transit_realtime
- pl_batch_ingestion
- df_weather_standardization
- nb_ingest_mbta_predictions

### 6. Git alignment is part of environment setup
Ensure the environment plan includes:
- which repo is the source of truth
- whether Fabric artifacts are expected to be Git-backed
- how item names map to repo structure
- what should and should not be committed

### 7. Design for demo fallback
For every live dependency, determine whether a fallback path is required.

At minimum, document:
- whether cached Bronze snapshots exist
- what happens if a live public API fails
- how the demo continues if Eventstream input is unavailable

## Required Inputs

Before applying this skill, gather:
- target demo scenario and audience
- expected Fabric workloads to demonstrate
- intended repo location
- whether Git integration is in scope now or later
- expected data sources
- whether live APIs will be used during demos

## Expected Outputs

A good run of this skill produces:
- environment design summary
- setup checklist
- naming convention list
- parameter/config file expectations
- unresolved risks or assumptions
- recommendation on demo fallback path

## Examples

### Example prompt
"Architect, define the Fabric environment for this repo using the demo architecture as the source of truth."

### Example output shape
- Capacity recommendation
- Workspace naming recommendation
- Required artifact list
- Parameter file requirements
- Git integration notes
- Risks and open questions

## Anti-Patterns

- Starting implementation before the workspace/item design is clear
- Hardcoding workspace IDs or artifact names into notebooks or pipelines
- Mixing production concerns into a field demo without explicit need
- Treating Git integration as an afterthought
- Assuming live public APIs are always reliable during a demo
- Using unclear artifact names like `Pipeline1`, `Notebook-New`, or `LakehouseTest`

## Review Checklist

Before closing environment setup, confirm:
- the environment supports every required demo workload
- artifact names are consistent and explainable
- all environment-specific values are parameterized
- fallback strategy is documented
- the repo remains the source of truth for reusable demo assets