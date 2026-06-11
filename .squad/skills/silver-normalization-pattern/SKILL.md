---
name: "silver-normalization-pattern"
description: "Normalize raw Bronze data into conformed Silver entities for the Fabric transit demo, including shared business keys, UTC timestamp normalization, quality filtering, and cross-source schema alignment. Use when implementing or reviewing Silver-layer transformations for transit, weather, and public events."
domain: "data-modeling"
confidence: "high"
source: "manual"
tools:
  - name: "Notebook"
    description: "Code-first transformation and schema normalization"
    when: "When custom parsing, conformed entity shaping, or domain-heavy transformation logic is required"
  - name: "Dataflow Gen2"
    description: "Low-code shaping and standardization"
    when: "When transformations are better demonstrated as business-friendly, low-code cleanup or enrichment steps"
  - name: "SQL"
    description: "Declarative relational shaping"
    when: "When defining reusable modeled outputs or validating conformed schemas"
---

## Context

This skill applies whenever data is being transformed from Bronze into Silver for the transit demo.

The Silver layer exists to convert raw, source-faithful Bronze data into a shared analytical foundation that can support:
- multiple transit agencies
- multiple ingestion patterns
- multiple transformation methods
- reusable KPI logic in Gold

This skill should be used whenever the squad is:
- aligning source-specific payloads into shared entities
- standardizing time semantics
- creating conformed facts and dimensions
- deciding what logic belongs in Silver versus Gold
- validating whether a transformation has crossed the boundary from technical normalization into business KPI logic

## Patterns

### 1. Silver creates shared meaning across sources
The Silver layer should harmonize different source systems into a common model.

For the transit demo, Silver should align concepts such as:
- city
- agency
- route
- stop
- trip
- vehicle
- prediction
- weather period
- event window

Do not let each source keep its own isolated business schema if a conformed model is possible.

### 2. Normalize timestamps to UTC
Silver is the canonical layer for time normalization.

Always:
- identify source-local timestamp fields
- convert canonical event timestamps to UTC
- preserve source-local time when it is useful for downstream analysis or storytelling
- distinguish clearly between different time meanings such as:
  - observation timestamp
  - predicted arrival timestamp
  - scheduled timestamp
  - ingestion timestamp

If timestamp semantics are ambiguous, record that ambiguity rather than hiding it.

### 3. Conform identifiers intentionally
Silver should define how source-native IDs map to reusable keys.

For each entity, identify:
- source-native business identifier
- whether that identifier is stable enough to reuse directly
- whether a surrogate key or conformed key is needed
- how entities from multiple agencies remain distinguishable without losing comparability

Avoid accidental key collisions across agencies or cities.

### 4. Separate normalization from KPI logic
Silver is the layer for:
- schema alignment
- cleansing
- relationship modeling
- timestamp normalization
- technical and business-grain shaping

Silver is not the layer for:
- final KPI rollups
- presentation marts
- executive summary metrics
- story-specific reporting output

If a transformation produces a directly consumable KPI summary, that logic likely belongs in Gold.

### 5. Apply quality filtering explicitly
Silver may reject or quarantine data that is malformed or analytically unusable.

Examples include:
- invalid timestamps
- missing critical business identifiers
- unparseable payload fragments
- impossible coordinate or route combinations

When filtering, document:
- why the record is filtered
- whether the decision is technical or business-driven
- whether the data should be recoverable later

### 6. Shape facts and dimensions deliberately
Silver should make it easier to create a clear Gold warehouse model later.

Typical Silver outputs may include:
- normalized dimensions such as city, agency, route, stop, trip, vehicle, weather condition, and public event
- normalized fact-like entities such as prediction snapshots, vehicle positions, weather observations, service alerts, and event windows

The exact split can evolve, but the grain of each output must be explicit.

### 7. Keep the transformation method explainable
The demo intentionally uses multiple transformation technologies.

When implementing a Silver transformation, document:
- why Notebook, Dataflow Gen2, or SQL was chosen
- what part of the normalization it is responsible for
- what assumptions it makes about Bronze inputs

The method choice should support the story, not obscure it.

## Required Inputs

Before applying this skill, gather:
- related source contract(s)
- Bronze object names and expected payload grain
- target conformed entities
- required timestamp fields and time semantics
- expected consumers of the Silver outputs
- quality constraints or known schema issues

## Expected Outputs

A good run of this skill produces:
- a conformed Silver entity design
- grain definitions for each Silver output
- UTC normalization rules
- key-mapping guidance
- filtering and quality rules
- clear statement of what is intentionally deferred to Gold

## Silver Acceptance Criteria

A Silver implementation is acceptable if:
- it aligns one or more source systems into shared entities
- canonical timestamps are normalized to UTC
- identifiers are explicit and collision-safe
- data quality rules are visible and explainable
- the result supports later Gold modeling without requiring direct Bronze access
- the transformation method is justified and demo-appropriate

## Examples

### Example prompt
"Transformation Engineer, normalize MBTA and WMATA predictions into a shared Silver prediction snapshot model."

### Example expected result
- agency-aware conformed prediction entity
- UTC-normalized arrival/departure timestamps
- route / stop / trip / vehicle references aligned
- malformed or incomplete records filtered with documented rules
- no Gold KPI aggregations embedded in the output

## Anti-Patterns

- Keeping agency-specific schemas intact when a conformed model is possible
- Converting timestamps without documenting what they represent
- Hiding source-local time entirely when it matters for later analysis
- Building final KPI summaries directly in Silver
- Using inconsistent naming across Silver entities
- Allowing Gold tables to depend directly on Bronze because Silver was underspecified

## Review Checklist

Before closing a Silver task, confirm:
- the output grain is explicit
- timestamps are normalized to UTC where appropriate
- source identity remains traceable
- identifiers are conformed or safely scoped
- quality filtering rules are documented
- the result is analytically reusable and does not bypass Gold responsibilities