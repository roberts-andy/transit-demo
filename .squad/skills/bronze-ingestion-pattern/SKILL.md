---
name: "bronze-ingestion-pattern"
description: "Apply a consistent Bronze landing approach for the transit demo across Notebook, Pipeline, and Eventstream ingestion paths. Use when implementing or reviewing raw ingestion so source fidelity, technical metadata, and medallion boundaries stay intact."
domain: "ingestion"
confidence: "high"
source: "manual"
tools:
  - name: "Notebook"
    description: "Custom extraction and raw payload handling"
    when: "When source logic requires code-first extraction, parsing, retries, or custom storage logic"
  - name: "Pipeline"
    description: "Orchestration and parameterized ingestion flow"
    when: "When scheduling or coordinating Bronze landing tasks"
  - name: "Eventstream"
    description: "Real-time routing into Fabric destinations"
    when: "When demonstrating streaming ingestion into Eventhouse or Lakehouse"
---

## Context

This skill applies whenever data is being landed into the Bronze layer of the transit demo.

The Bronze layer exists to preserve source fidelity and establish a trustworthy raw foundation for later transformation.

This skill must be used for all Bronze implementations regardless of whether the ingestion mechanism is:
- Spark Notebook
- Data Pipeline
- Eventstream
- another demo-approved ingestion path

## Patterns

### 1. Bronze preserves source fidelity
The Bronze layer should keep the source as close to original as practical.

Always preserve:
- source-native field names where practical
- raw payload structure when feasible
- technical ingestion metadata
- extraction/source provenance

Do not apply business modeling logic in Bronze.

### 2. Add technical metadata to every Bronze object
Each Bronze record or batch must include technical metadata such as:
- source system name
- extraction timestamp
- ingestion timestamp if distinct
- source endpoint or entity type if helpful
- source record identifier if available
- optional record hash if useful for integrity or change tracking

### 3. Keep Bronze and Silver responsibilities separate
Bronze is not the place to:
- rename fields for analytics convenience
- create conformed dimensions
- normalize all timestamps into final business form
- join across sources
- derive KPI logic

Minimal technical shaping is acceptable only when needed to store or parse the raw data reliably.

### 4. Standardize Bronze target naming
Bronze object names should make the source and raw nature obvious.

Examples:
- bronze_mbta_routes_raw
- bronze_mbta_predictions_raw
- bronze_wmata_vehicle_positions_raw
- bronze_weather_hourly_raw
- bronze_public_events_raw

### 5. Support multiple ingestion mechanisms consistently
The ingestion mechanism may vary, but the Bronze contract should remain consistent.

Notebook path:
- supports custom code-first extraction
- useful for paging, retries, custom parsing

Pipeline path:
- supports orchestration, schedules, parameterization
- should still land source-faithful outputs

Eventstream path:
- supports near-real-time input
- should still preserve useful raw event structure and source metadata

### 6. Capture reliability and replay expectations
Bronze implementations for demos should explicitly state:
- whether they depend on live sources
- whether replay or cached snapshots exist
- what happens if the source is unavailable

### 7. Favor inspectability
A field engineer or customer should be able to inspect Bronze and immediately understand:
- what source it came from
- when it was ingested
- whether it is raw or transformed

## Required Inputs

Before applying this skill, gather:
- source contract or equivalent source understanding
- intended ingestion mechanism
- target Bronze object name
- expected refresh cadence or trigger
- any live-demo reliability concerns

## Expected Outputs

A good run of this skill produces:
- Bronze landing design
- target object/table names
- required technical metadata fields
- ingestion method notes
- replay/fallback notes
- explicit statement of what logic is intentionally deferred to Silver

## Bronze Acceptance Criteria

A Bronze implementation is acceptable if:
- it preserves source fidelity as closely as practical
- it adds required technical metadata
- it does not introduce business logic or Gold-style modeling
- it is clearly named and source-attributed
- it is inspectable and reproducible

## Examples

### Example prompt
"Batch Ingestion Engineer, design the Bronze landing pattern for MBTA predictions using a Spark Notebook."

### Example expected result
- target object: bronze_mbta_predictions_raw
- raw payload retained
- extraction timestamp added
- source system and endpoint captured
- no Silver-style conformed rename logic applied

## Anti-Patterns

- Renaming fields to business-friendly names in Bronze
- Joining raw transit data to weather or events in Bronze
- Computing KPIs or lateness metrics in Bronze
- Landing ambiguous raw data without extraction metadata
- Using generic table names that hide source or raw status
- Making Bronze dependent on downstream warehouse modeling decisions

## Review Checklist

Before closing a Bronze ingestion task, confirm:
- the output is clearly raw
- the source system is clearly identified
- ingestion metadata is present
- no business logic has leaked into Bronze
- replay or fallback considerations are documented if needed