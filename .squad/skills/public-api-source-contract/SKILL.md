---
name: "public-api-source-contract"
description: "Define a repeatable source contract for public API datasets used in the transit demo, including entities, keys, timestamps, throttling concerns, schema risks, and mapping expectations into Bronze and Silver. Use when onboarding or reviewing MBTA, WMATA, weather, or public events sources."
domain: "source-modeling"
confidence: "high"
source: "manual"
tools:
  - name: "HTTP/REST client"
    description: "Fetch source payloads and inspect endpoint behavior"
    when: "When evaluating public APIs, payload schemas, pagination, and response patterns"
  - name: "Notebook"
    description: "Inspect, parse, and prototype source extraction logic"
    when: "When source contracts require JSON, GTFS, or custom parsing analysis"
---

## Context

This skill applies whenever a new public source is added to the transit demo or an existing source contract changes.

The transit demo relies on multiple public-source systems with different shapes and behaviors:
- transit APIs
- weather APIs
- public events APIs

These sources vary in:
- entity naming
- response structure
- timestamp formats
- identifiers
- paging/rate-limit behavior
- reliability

This skill exists to make source onboarding systematic and reusable.

## Patterns

### 1. Treat every source as a contract, not just an endpoint
When evaluating a source, define:
- what business purpose it serves in the demo
- which entities it provides
- which fields are essential
- how records will be keyed
- how timestamps will be interpreted
- what constraints might affect extraction or normalization

Do not proceed with ingestion logic until the contract is described clearly.

### 2. Separate raw source understanding from normalized model design
First document the source in its own terms:
- source endpoint names
- source-native entity names
- response format
- source field names
- source update cadence if known

Only after that should you define how the source maps into shared Bronze and Silver entities.

### 3. Always capture identity and time semantics
For each source entity, identify:
- source record identifier
- parent/child relationships if visible
- event timestamp fields
- local time vs UTC semantics
- whether timestamps represent observation time, schedule time, predicted time, or extraction time

If the source is ambiguous about time semantics, record that ambiguity explicitly.

### 4. Record extraction constraints early
Document any extraction concerns such as:
- API key requirements
- paging
- rate limits
- throttling
- unstable fields
- occasionally sparse or missing records
- schema fields that are conditional or optional

### 5. Design Bronze mapping expectations
Each source contract should specify:
- target Bronze landing object(s)
- whether raw payloads are stored as-is or minimally structured
- required ingestion metadata
- whether raw arrays need minimal technical flattening for storage

### 6. Design Silver mapping expectations
For each source, define likely Silver targets:
- dimension candidates
- fact candidates
- conformed key candidates
- join expectations
- expected normalization work

### 7. Capture demo-specific usefulness
This demo is storytelling-oriented, so every source contract should explain:
- why the source is in the demo
- which KPI or narrative it supports
- whether it is core-path or optional enrichment

## Source Contract Template

For each source, capture the following:

### Source Overview
- source name
- source type
- city or geographic scope
- purpose in the demo

### Entities
For each major entity:
- source entity name
- endpoint or retrieval path
- business meaning
- expected grain
- likely Bronze target
- likely Silver target

### Key Fields
- business identifiers
- timestamp fields
- geographic fields
- relationship fields
- quality-sensitive fields

### Extraction Considerations
- auth required?
- paging?
- rate limit?
- expected refresh cadence?
- live-demo reliability risk?

### Mapping Considerations
- source-native naming issues
- UTC normalization needs
- conformed model alignment needs
- likely join paths to other demo data

## Required Inputs

Before applying this skill, gather:
- source name
- source purpose in the demo
- intended ingestion pattern
- at least one representative payload or endpoint sample if available

## Expected Outputs

A good run of this skill produces:
- source contract summary
- entity inventory
- key/time semantics summary
- extraction risk notes
- Bronze/Silver mapping notes
- open assumptions or unresolved ambiguities

## Examples

### Example source list
- MBTA routes, stops, vehicles, predictions
- WMATA routes, stops, vehicle positions, predictions
- hourly weather
- public event calendars

### Example prompt
"Transformation Engineer, create a source contract for WMATA vehicle positions and predictions."

## Anti-Patterns

- Jumping straight into code without documenting the source contract
- Assuming all transit systems use equivalent identifiers
- Assuming local timestamps are already UTC
- Mixing Bronze landing rules with Silver business logic in the same source note
- Treating enrichment sources as self-evident rather than documenting their narrative value
- Ignoring rate limits or live-demo reliability concerns

## Review Checklist

Before closing a source contract, confirm:
- all core entities are identified
- key and timestamp semantics are explicitly described
- Bronze target objects are known
- likely Silver mappings are documented
- unresolved ambiguities are visible rather than hidden
``