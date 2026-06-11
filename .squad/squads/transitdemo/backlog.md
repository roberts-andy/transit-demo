---
title: "Transit Demo — Squad Backlog"
description: "Sequenced development backlog for the Fabric Transit Demo, organized by epic and feature with explicit skill invocations, ownership, and MVP sequencing."
---

## How to use this backlog

- Items are sequenced in MVP-first order across six phases.
- `skill:` annotations on a task mean the named skill **must be consulted** before starting or reviewing that work.
- Ownership abbreviations: **Lead**, **Arch** (Solution Architect), **Batch** (Batch Ingestion Engineer), **Stream** (Streaming Engineer), **Transform** (Transformation Engineer), **SQL** (SQL/Warehouse Engineer), **DemoOps**, **Scribe**.
- Source contract tasks (T-SC-x) are a new layer added after skill review. They are required inputs before any Bronze ingestion code is written.
- Status values: `[ ]` not started · `[~]` in progress · `[x]` complete · `[!]` blocked.
- Five skills now govern this backlog: `fabric-environment-setup`, `public-api-source-contract`, `bronze-ingestion-pattern`, `silver-normalization-pattern`, `demo-readiness-and-fallback`.

---

## Phase 0 — Critical Path (block everything downstream)

These must be resolved before any Fabric implementation work begins.

- [ ] **CP-1** Provision Fabric workspace and confirm capacity (F-SKU or Trial) — `skill: fabric-environment-setup` — **Lead + Arch**
- [ ] **CP-2** Create four Fabric items: `lh_transit_bronze`, `lh_transit_silver`, `eh_transit_realtime`, `wh_transit_gold` — `skill: fabric-environment-setup` — **Arch**
- [ ] **CP-3** Connect this repo to Fabric via Git integration; define branch mapping — `skill: fabric-environment-setup` — **DemoOps**
- [ ] **CP-4** Obtain and vault API keys: MBTA, WMATA, Open-Meteo, Ticketmaster — `skill: public-api-source-contract` (extraction constraints section) — **Batch + Lead**
- [ ] **CP-5** Populate `infra/parameters.dev.yml` from the example file — `skill: fabric-environment-setup` — **DemoOps**

---

## Phase 1 — Foundation

### E1 — Infrastructure and Environment Setup

> Skill governing all E1 work: **`fabric-environment-setup`**
>
> Required output from this epic before E2 begins: environment design summary, setup checklist, and naming convention list (per skill expected outputs).

#### F1.1 — Workspace and Capacity

- [ ] **T1.1.1** Document workspace and capacity provisioning steps in `docs/runbook.md` — `skill: fabric-environment-setup` (Pattern 1, 2) — **DemoOps**
- [ ] **T1.1.2** Decide: shared vs. dedicated capacity; record as decision in `decisions.md` — `skill: fabric-environment-setup` (Pattern 2) — **Lead**

#### F1.2 — Git Integration

- [ ] **T1.2.1** Document Fabric Git integration steps: connect workspace to GitHub repo and set branch mapping — `skill: fabric-environment-setup` (Pattern 6) — **DemoOps**
- [ ] **T1.2.2** Define `main` vs. `dev` branch policy for Fabric sync; record as decision — `skill: fabric-environment-setup` (Pattern 6) — **Lead**

#### F1.3 — Fabric Item Creation

- [ ] **T1.3.1** Create `lh_transit_bronze` Lakehouse — `skill: fabric-environment-setup` (Pattern 3, 5) — **Arch**
- [ ] **T1.3.2** Create `lh_transit_silver` Lakehouse — `skill: fabric-environment-setup` (Pattern 3, 5) — **Arch**
- [ ] **T1.3.3** Create `wh_transit_gold` Fabric Warehouse — `skill: fabric-environment-setup` (Pattern 3, 5) — **SQL**
- [ ] **T1.3.4** Create `eh_transit_realtime` Eventhouse and KQL Database — `skill: fabric-environment-setup` (Pattern 3, 5) — **Stream**
- [ ] **T1.3.5** Create `es_transit_realtime` Eventstream item — `skill: fabric-environment-setup` (Pattern 3, 5) — **Stream**
- [ ] **T1.3.6** Provision Event Hub namespace or confirm Fabric-native stream source — **Stream**

#### F1.4 — API Key Management

- [ ] **T1.4.1** Document key acquisition steps for all four APIs in `docs/runbook.md` — `skill: public-api-source-contract` (extraction constraints) — **DemoOps**
- [ ] **T1.4.2** Create `.env.template` with all required environment variable names (no values) — **DemoOps**
- [ ] **T1.4.3** Document how keys are injected into Fabric Notebooks via Key Vault or Notebook parameters — **Batch**
- [ ] **T1.4.4** Evaluate Ticketmaster availability; decide fallback public events source — `skill: public-api-source-contract` (demo-specific usefulness) — **Lead**

#### F1.5 — Parameter Files

- [ ] **T1.5.1** Create `infra/parameters.dev.yml` with all workspace and item IDs filled in — `skill: fabric-environment-setup` (Pattern 4) — **DemoOps**
- [ ] **T1.5.2** Add parameter loading utility for workspace, Lakehouse, and Warehouse IDs — `skill: fabric-environment-setup` (Pattern 4) — **Batch**

#### F1.6 — Environment Design Summary (new — required by skill)

- [ ] **T1.6.1** Produce environment design summary covering capacity, workspace, item inventory, naming, Git alignment, and fallback strategy — `skill: fabric-environment-setup` (expected outputs) — **Arch + DemoOps**
- [ ] **T1.6.2** Produce setup checklist and naming convention list as a companion to `docs/runbook.md` — `skill: fabric-environment-setup` (expected outputs) — **Scribe**

---

### Phase 1 (continued) — Source Contracts (new epic, required before E2)

> Skill governing all source contract work: **`public-api-source-contract`**
>
> Source contracts are required inputs before any Bronze ingestion code is written (skill anti-pattern: "jumping straight into code without documenting the source contract").
> Each contract must cover: entity inventory, key and time semantics, extraction constraints, Bronze mapping expectations, Silver mapping expectations, and demo narrative value.
> Contracts feed directly into `data_contracts/source-inventory.yml` enrichment (entity-level key/time/constraint fields currently missing).

#### E-SC — Source Contracts

- [ ] **T-SC-1** Write MBTA source contract — `skill: public-api-source-contract` — **Batch + Transform**
  - Entities: routes, stops, trips, predictions, vehicles, alerts
  - Covers: MBTA V3 auth tier, paging, rate limits, source-local vs. UTC timestamps, GTFS-RT considerations for streaming path
  - Feeds: F2.1, F3.1
- [ ] **T-SC-2** Write WMATA source contract — `skill: public-api-source-contract` — **Batch + Transform**
  - Entities: train arrivals, bus predictions, schedules, routes, stops, vehicle positions, alerts
  - Covers: API key requirements, GTFS vs. REST paths, auth risk, schema differences vs. MBTA
  - Feeds: F2.2
- [ ] **T-SC-3** Write Open-Meteo source contract — `skill: public-api-source-contract` — **Batch**
  - Entities: hourly weather by city
  - Covers: unauthenticated access confirmation, rate limits, UTC output verification, city parameterization
  - Feeds: F2.3
- [ ] **T-SC-4** Write Ticketmaster (or fallback source) contract — `skill: public-api-source-contract` — **Lead + Batch**
  - Entities: events, venues
  - Covers: API key tier, rate limits, fallback source decision (depends on T1.4.4), demo narrative value for KPI enrichment
  - Feeds: F2.4

---

## Phase 2 — Bronze Ingestion (Batch)

> **Depends on:** Phase 0 complete, T-SC-1 through T-SC-4 complete.
>
> Skill governing all Bronze landing work: **`bronze-ingestion-pattern`**
>
> All Bronze tasks must meet the Bronze Acceptance Criteria from the skill before being marked complete:
> output is clearly raw · source system identified · ingestion metadata present · no business logic leaked · replay/fallback considerations documented.

### E2 — Bronze Ingestion (Batch)

#### F2.1 — MBTA Spark Notebook Ingestion

> Requires: T-SC-1 (MBTA source contract) · `skill: bronze-ingestion-pattern`

- [ ] **T2.1.1** Create `src/ingestion/notebooks/bronze_mbta_routes.ipynb` — pull `/routes`, write to `bronze_mbta_routes_raw` — `skill: bronze-ingestion-pattern` — **Batch**
- [ ] **T2.1.2** Create `src/ingestion/notebooks/bronze_mbta_stops.ipynb` — pull `/stops` — `skill: bronze-ingestion-pattern` — **Batch**
- [ ] **T2.1.3** Create `src/ingestion/notebooks/bronze_mbta_predictions.ipynb` — pull `/predictions` with route/stop filters — `skill: bronze-ingestion-pattern` — **Batch**
- [ ] **T2.1.4** Create `src/ingestion/notebooks/bronze_mbta_vehicles.ipynb` — pull `/vehicles` — `skill: bronze-ingestion-pattern` — **Batch**
- [ ] **T2.1.5** Add required technical metadata to all MBTA notebooks: `source_system`, `extraction_ts`, `source_endpoint`, `source_record_id`, optional record hash — `skill: bronze-ingestion-pattern` (Pattern 2) — **Batch**

#### F2.2 — WMATA Spark Notebook Ingestion

> Requires: T-SC-2 (WMATA source contract) · `skill: bronze-ingestion-pattern`

- [ ] **T2.2.1** Create `src/ingestion/notebooks/bronze_wmata_routes.ipynb` — `skill: bronze-ingestion-pattern` — **Batch**
- [ ] **T2.2.2** Create `src/ingestion/notebooks/bronze_wmata_stops.ipynb` — `skill: bronze-ingestion-pattern` — **Batch**
- [ ] **T2.2.3** Create `src/ingestion/notebooks/bronze_wmata_predictions.ipynb` — `skill: bronze-ingestion-pattern` — **Batch**
- [ ] **T2.2.4** Create `src/ingestion/notebooks/bronze_wmata_vehicle_positions.ipynb` — `skill: bronze-ingestion-pattern` — **Batch**

#### F2.3 — Weather via Data Factory Pipeline

> Requires: T-SC-3 (Open-Meteo source contract) · `skill: bronze-ingestion-pattern`
>
> Note: Pipeline path must land source-faithful output. Renaming or restructuring during landing is an anti-pattern per `bronze-ingestion-pattern` Pattern 5.

- [ ] **T2.3.1** Create `src/ingestion/pipelines/pl_ingest_weather.json` — Pipeline calling Open-Meteo hourly endpoint — `skill: bronze-ingestion-pattern` — **Batch**
- [ ] **T2.3.2** Pipeline writes raw JSON to `bronze_weather_hourly_raw`; no field renaming during landing — `skill: bronze-ingestion-pattern` (Pattern 1, anti-pattern review) — **Batch**
- [ ] **T2.3.3** Parameterize city list (Boston, Washington DC) via pipeline parameters — `skill: fabric-environment-setup` (Pattern 4) — **Batch**

#### F2.4 — Public Events via Pipeline

> Requires: T-SC-4 (Ticketmaster/fallback source contract) · `skill: bronze-ingestion-pattern`

- [ ] **T2.4.1** Create `src/ingestion/pipelines/pl_ingest_events.json` — Pipeline calling source decided in T-SC-4 — `skill: bronze-ingestion-pattern` — **Batch**
- [ ] **T2.4.2** Write raw events to `bronze_public_events_raw` with required technical metadata — `skill: bronze-ingestion-pattern` (Pattern 2) — **Batch**

#### F2.5 — Pipeline Orchestration

- [ ] **T2.5.1** Create `src/ingestion/pipelines/pl_orchestrate_bronze.json` — master pipeline triggering all batch ingestion in dependency order — **Batch**
- [ ] **T2.5.2** Add retry configuration and logging to all pipelines — **Batch**
- [ ] **T2.5.3** Explicitly document replay/fallback status for each pipeline — `skill: bronze-ingestion-pattern` (Pattern 6) — **Batch**
- [ ] **T2.5.4** Add daily schedule trigger to master pipeline — **DemoOps**

---

## Phase 2 (continued) — Bronze Ingestion (Streaming)

### E3 — Bronze Ingestion (Streaming)

> **Depends on:** T1.3.4, T1.3.5 (Eventhouse and Eventstream items created), T-SC-1 (MBTA source contract for streaming entity).
>
> Skill governing all streaming Bronze work: **`bronze-ingestion-pattern`** (Pattern 5 — streaming path must preserve raw event structure and source metadata).

#### F3.1 — Eventstream Configuration

- [ ] **T3.1.1** Configure `es_transit_realtime` source — MBTA GTFS-RT feed or custom endpoint — `skill: bronze-ingestion-pattern` (Pattern 5) — **Stream**
- [ ] **T3.1.2** Configure Eventstream destination to Lakehouse (`bronze_transit_stream_raw`) — `skill: bronze-ingestion-pattern` (Pattern 4, 5) — **Stream**
- [ ] **T3.1.3** Configure secondary destination to Eventhouse KQL Database for real-time query demo path — `skill: demo-readiness-and-fallback` (Pattern 2, streaming path is a required demo capability) — **Stream**

#### F3.2 — Stream Fallback Replay

> The skill directly mandates capturing whether replay/cached snapshots exist. This is not optional.

- [ ] **T3.2.1** Capture a representative MBTA GTFS-RT snapshot as a static JSON fixture in `src/ingestion/fixtures/mbta_gtfsrt_sample.json` — `skill: bronze-ingestion-pattern` (Pattern 6) — **Stream**
- [ ] **T3.2.2** Create `src/ingestion/fixtures/replay_stream.ipynb` — notebook that injects fixture data into the stream path — `skill: bronze-ingestion-pattern` (Pattern 6) — **Stream**

#### F3.3 — Source Inventory Update

- [ ] **T3.3.1** Add `bronze_transit_stream_raw` to `data_contracts/source-inventory.yml` under a new `streaming` source entry — `skill: public-api-source-contract` (entity inventory) — **Scribe**

---

## Phase 3 — Silver Transformation

> **Depends on:** E2 Bronze tables populated at MVP level.

### E4 — Silver Transformation

> Skill governing all E4 work: **`silver-normalization-pattern`**
>
> Required inputs before any Silver task begins: completed source contracts (T-SC-1 through T-SC-4), Bronze target names, and expected entity grain (per skill required inputs).
> Required output from this epic before E5 begins: conformed Silver entities with explicit grain, UTC-normalized timestamps, collision-safe identifiers, documented quality rules, and transformation method justification per artifact.
> All Silver tasks must meet the Silver Acceptance Criteria from the skill before being marked complete.
> Anti-pattern to prevent: do not allow E5 Gold tables to depend directly on raw Bronze because Silver was underspecified — this is explicitly called out in the `silver-normalization-pattern` anti-pattern list.

#### F4.0 — Silver Entity Design (new — required by skill)

- [ ] **T4.0.1** Produce Silver entity design document covering: output grain per entity, UTC normalization rules per source, key-mapping and collision-safety strategy, quality filtering rules, and justification for Notebook vs. Dataflow Gen2 vs. SQL per transform — `skill: silver-normalization-pattern` (required inputs + Pattern 7) — **Transform + Arch**

#### F4.1 — Transit Normalization (Notebooks)

> Requires: T4.0.1 (Silver entity design) · source contracts T-SC-1 and T-SC-2 · `skill: silver-normalization-pattern`

- [ ] **T4.1.1** Create `src/transform/notebooks/silver_dim_route.ipynb` — harmonize MBTA and WMATA routes into `dim_route` — `skill: silver-normalization-pattern` (Pattern 1, 3) + source contracts T-SC-1, T-SC-2 — **Transform**
- [ ] **T4.1.2** Create `src/transform/notebooks/silver_dim_stop.ipynb` — harmonize stops into `dim_stop` — `skill: silver-normalization-pattern` (Pattern 1, 3) — **Transform**
- [ ] **T4.1.3** Create `src/transform/notebooks/silver_dim_vehicle.ipynb` — `skill: silver-normalization-pattern` (Pattern 1, 3) — **Transform**
- [ ] **T4.1.4** Create `src/transform/notebooks/silver_fact_prediction_snapshot.ipynb` — parse predictions, compute `predicted_delay_seconds`, normalize timestamps to UTC — `skill: silver-normalization-pattern` (Pattern 2, UTC normalization) + source contracts T-SC-1, T-SC-2 — **Transform**
- [ ] **T4.1.5** Create `src/transform/notebooks/silver_fact_vehicle_position.ipynb` — `skill: silver-normalization-pattern` (Pattern 2, 6) — **Transform**
- [ ] **T4.1.6** All Silver notebooks: UTC normalization applied, surrogate key generation, corrupted record filter with documented rule per rejection type — `skill: silver-normalization-pattern` (Pattern 2, 5) — **Transform**

#### F4.2 — Weather Shaping (Dataflow Gen2)

> Requires: T4.0.1 (Silver entity design) · source contract T-SC-3 · `skill: silver-normalization-pattern`

- [ ] **T4.2.1** Create `src/transform/dataflows/df_silver_weather.json` — Dataflow Gen2 shaping `bronze_weather_hourly_raw` → `fact_hourly_weather` — `skill: silver-normalization-pattern` (Pattern 2, 7) + source contract T-SC-3 — **Transform**
- [ ] **T4.2.2** Rename/cast columns; derive weather condition label from code; UTC timestamp confirmed — `skill: silver-normalization-pattern` (Pattern 2) — **Transform**

#### F4.3 — Public Events Shaping (Dataflow Gen2)

> Requires: T4.0.1 (Silver entity design) · source contract T-SC-4 · `skill: silver-normalization-pattern`

- [ ] **T4.3.1** Create `src/transform/dataflows/df_silver_events.json` — shape `bronze_public_events_raw` → `dim_public_event` + `dim_event_venue` — `skill: silver-normalization-pattern` (Pattern 1, 6) + source contract T-SC-4 — **Transform**

#### F4.4 — Static Dimensions

- [ ] **T4.4.1** Create `src/transform/notebooks/silver_dim_city.ipynb` — seed `dim_city` for Boston and Washington DC — `skill: silver-normalization-pattern` (Pattern 1, 3) — **Transform**
- [ ] **T4.4.2** Create `src/transform/notebooks/silver_dim_date.ipynb` — populate `dim_date` for demo date range — `skill: silver-normalization-pattern` (Pattern 2) — **Transform**
- [ ] **T4.4.3** Create `src/transform/notebooks/silver_dim_agency.ipynb` — seed MBTA and WMATA agencies — `skill: silver-normalization-pattern` (Pattern 1) — **Transform**

#### F4.5 — Silver Orchestration Pipeline

- [ ] **T4.5.1** Create `src/transform/pipelines/pl_orchestrate_silver.json` — runs Silver transforms in dependency order after Bronze — `skill: silver-normalization-pattern` (Pattern 4, confirm no KPI logic in pipeline) — **Batch**

---

## Phase 4 — Gold Warehouse and KPIs

> **Depends on:** E4 Silver tables populated in `lh_transit_silver`.

### E5 — Gold Warehouse and KPIs

#### F5.1 — Materialized Lake Views

- [ ] **T5.1.1** Create `src/warehouse/mlv/mlv_route_hourly_agg.sql` — aggregate predictions and vehicles by route/hour — **SQL**
- [ ] **T5.1.2** Create `src/warehouse/mlv/mlv_stop_daily_agg.sql` — stop-level daily summary — **SQL**
- [ ] **T5.1.3** Create `src/warehouse/mlv/mlv_weather_city_hourly.sql` — join weather to city/hour grain — **SQL**

#### F5.2 — Warehouse DDL

- [ ] **T5.2.1** Create `src/warehouse/ddl/wh_dimensions.sql` — `CREATE TABLE` for all Gold dimensions in `wh_transit_gold` — **SQL**
- [ ] **T5.2.2** Create `src/warehouse/ddl/wh_facts.sql` — `CREATE TABLE` for `fact_prediction_snapshot`, `fact_vehicle_position`, `fact_hourly_weather` — **SQL**
- [ ] **T5.2.3** Create `src/warehouse/ddl/wh_kpi_views.sql` — `CREATE VIEW` for `vw_gold_route_hourly_performance`, `vw_gold_stop_daily_performance`, `vw_gold_city_weather_correlation`, `vw_gold_event_impact_summary` — **SQL**

#### F5.3 — Gold Load Pipeline

- [ ] **T5.3.1** Create `src/warehouse/pipelines/pl_load_gold.json` — copies conformed Silver tables into Warehouse Gold — **SQL**
- [ ] **T5.3.2** Add `is_event_window` and `is_adverse_weather` flag derivation in Gold load — **SQL**

#### F5.4 — KPI Validation Queries

- [ ] **T5.4.1** Create `src/warehouse/validation/kpi_smoke_queries.sql` — spot-check row counts, null rates, and on-time percentage by route — `skill: demo-readiness-and-fallback` (Pattern 2, at least one KPI must be explainable for gate T6.5.4) — **SQL + DemoOps**

---

## Phase 5 — Demo Readiness and Fallback Data

> **Depends on:** E2, E3, E4, E5 at MVP fidelity.

### E6 — Demo Readiness and Fallback Data

> Skill governing all E6 work: **`demo-readiness-and-fallback`**
>
> Required inputs before any E6 task begins: current implementation status across E2–E5, required Fabric capabilities list, current runbook state, known live dependencies, and target audience profile if known.
> Required output from this epic: demo readiness summary, MVD path defined, per-dependency fallback plan, operator checklist, and a passed demo readiness gate (T6.5.4).
> E6 is not optional. Fallback is part of the design — not a last-minute rescue.

#### F6.0 — Demo Scope and Narrative Definition (new — required by skill)

> This feature should be started as soon as Phase 4 (E5) is underway — not blocked until everything else is done.

- [ ] **T6.0.1** Define Minimum Viable Demo (MVD) path and full demo path separately; record which capabilities are required vs optional enrichments — `skill: demo-readiness-and-fallback` (Pattern 7) — **Lead + DemoOps**
- [ ] **T6.0.2** For each required Fabric capability, document: the story it tells, where it appears in the session flow, which artifact demonstrates it, and what value the audience should take away — `skill: demo-readiness-and-fallback` (Pattern 1) — **Lead + Scribe**

#### F6.1 — Fallback / Cached Data

> Fallback design was initiated in E1 (T1.6.1 per `fabric-environment-setup` Pattern 7). This feature executes it.

- [ ] **T6.1.1** Capture Bronze snapshot CSVs or Parquet for all four sources into `src/fixtures/bronze/` — `skill: demo-readiness-and-fallback` (Pattern 3) — **DemoOps**
- [ ] **T6.1.2** Create `src/fixtures/load_fixtures.ipynb` — populates Bronze tables from fixture files without live API calls — `skill: demo-readiness-and-fallback` (Pattern 3) — **DemoOps**
- [ ] **T6.1.3** Add fixture load step to `docs/runbook.md` — `skill: demo-readiness-and-fallback` (Pattern 5) — **Scribe**

#### F6.2 — Smoke Tests

> Bronze smoke test structure is derived from the `bronze-ingestion-pattern` Review Checklist.
> Silver smoke test structure is derived from the `silver-normalization-pattern` Review Checklist: grain explicit · UTC timestamps present · identifiers conformed and collision-safe · quality rules documented · no KPI logic in Silver.
> Gold and end-to-end readiness is governed by `demo-readiness-and-fallback` Demo Acceptance Criteria.

- [ ] **T6.2.1** Create `tests/smoke_bronze.py` — validates Bronze tables: non-empty, expected columns, `ingestion_ts` populated, source system field present — `skill: bronze-ingestion-pattern` (Review Checklist) — **DemoOps**
- [ ] **T6.2.2** Create `tests/smoke_silver.py` — validates Silver tables: UTC timestamps present, surrogate keys populated, no null conformed identifiers, row counts reasonable, no KPI aggregation columns — `skill: silver-normalization-pattern` (Review Checklist) — **DemoOps**
- [ ] **T6.2.3** Create `tests/smoke_gold.py` — validates Warehouse KPI views: row counts, no null on KPI columns, on-time percentage in plausible range — `skill: demo-readiness-and-fallback` (Pattern 2, end-to-end path validation) — **DemoOps**

#### F6.3 — Pre-Demo Reset Script

- [ ] **T6.3.1** Create `src/reset/reset_demo.ipynb` — truncates or reloads Bronze from fixtures, re-runs Silver and Gold — `skill: demo-readiness-and-fallback` (Pattern 3, fallback execution) — **DemoOps**
- [ ] **T6.3.2** Document reset procedure in `docs/runbook.md` — `skill: demo-readiness-and-fallback` (Pattern 5, operator readiness) — **Scribe**

#### F6.4 — Runbook Hardening

- [ ] **T6.4.1** Expand `docs/runbook.md` with executable pre-demo checklist (capacity, API keys, Bronze state, Silver deps, Gold load, fallback ready) and operator guidance (presentation order, skip paths, failure branches) — `skill: demo-readiness-and-fallback` (Pattern 5) + `skill: fabric-environment-setup` (Pattern 7) — **DemoOps + Scribe**
- [ ] **T6.4.2** Add post-demo cleanup steps to `docs/runbook.md` — `skill: demo-readiness-and-fallback` (Pattern 4, artifact freshness) — **DemoOps**

#### F6.5 — Demo Readiness Gate (new — required by skill)

> This feature is the formal customer-facing delivery gate. F6.0 defined the MVD and narrative; F6.5 confirms they still hold against the completed implementation and signs off before any rehearsal or customer session.
> Produces: demo readiness summary, critical path validation, must-show vs optional artifact list, confirmed fallback plan per dependency, operator checklist.

- [ ] **T6.5.1** Confirm MVD path and full demo path (defined in T6.0.1) are still accurate against the completed E2–E5 implementation; record any changes — `skill: demo-readiness-and-fallback` (Pattern 7) — **Lead + DemoOps**
- [ ] **T6.5.2** Validate per-artifact narrative alignment (documented in T6.0.2) against implemented artifacts; confirm each artifact demonstrates the intended story point — `skill: demo-readiness-and-fallback` (Pattern 1, 4) — **Lead + Scribe**
- [ ] **T6.5.3** For each live dependency, confirm the explicit fallback plan: whether it is required for the session, whether cached data exists and is loaded, what the operator does if it fails, and how to explain the fallback without undermining the story — `skill: demo-readiness-and-fallback` (Pattern 3) — **DemoOps**
- [ ] **T6.5.4** Conduct formal demo readiness gate check against Demo Acceptance Criteria: every required Fabric workload has a clear demonstration point, end-to-end Bronze → Silver → Gold story is valid, at least one KPI is explainable, live-source failures do not collapse the session, operator knows the failure branches — `skill: demo-readiness-and-fallback` (Demo Acceptance Criteria) — **Lead + DemoOps**

---

## Phase 5 (continued) — Documentation and Field Enablement

### E7 — Documentation and Field Enablement

#### F7.1 — Decision Log

- [ ] **T7.1.1** Record E1 infrastructure decisions in `decisions.md` — **Scribe**
- [ ] **T7.1.2** Record source selection decisions (Ticketmaster vs. alternative) in `decisions.md` — **Scribe**

#### F7.2 — Architecture Diagram

- [ ] **T7.2.1** Create a Mermaid architecture diagram in `docs/architecture.md` showing Bronze → Silver → Gold data flow and all Fabric items — **Arch**

#### F7.3 — Workload Talk Track

- [ ] **T7.3.1** Add a "When to use this pattern" reference table to `docs/product-spec.md`: one row per ingestion and transformation method, when to choose it, what it demonstrates — `skill: demo-readiness-and-fallback` (Pattern 1, narrative per workload) — **Scribe + Lead**

#### F7.4 — Field Reuse Guide

- [ ] **T7.4.1** Create `docs/field-reuse-guide.md` — how another field team forks this repo, adapts cities and sources, and connects to their workspace — `skill: fabric-environment-setup` (demo portability) — **Scribe**

---

## Skill Reference Summary

| Skill | Governs |
|---|---|
| `fabric-environment-setup` | CP-1, CP-2, CP-3, CP-5, all of E1 (F1.1–F1.6), T2.3.3, T1.5.x, T6.4.1, T7.4.1 |
| `public-api-source-contract` | CP-4, T1.4.1, T1.4.4, all of E-SC (T-SC-1–T-SC-4), T3.3.1, T4.1.1, T4.1.4, T4.2.1, T4.3.1 |
| `bronze-ingestion-pattern` | All of E2 (F2.1–F2.5), all of E3 (F3.1–F3.2), T6.2.1 |
| `silver-normalization-pattern` | T4.0.1, all of E4 (F4.1–F4.5), T6.2.2 |
| `demo-readiness-and-fallback` | All of E6 (F6.0–F6.5), T6.2.3 |

## Dependency Chain

```
Phase 0 (CP-1–CP-5)
  └─ Phase 1 E1 (F1.1–F1.6) + E-SC (T-SC-1–T-SC-4) [parallel]
       └─ Phase 2 E2 (F2.1–F2.5) + E3 (F3.1–F3.3) [parallel tracks]
            └─ Phase 3 E4 (F4.1–F4.5)
                 └─ Phase 4 E5 (F5.1–F5.4)
                      └─ Phase 5 E6 (F6.0–F6.5) + E7 (F7.1–F7.4) [parallel]
                         Note: E6/F6.0 (narrative + MVD definition) can start once E5 is underway
```

## Risks and Assumptions

| # | Item | Severity | Owner |
|---|---|---|---|
| R1 | WMATA API authentication is non-trivial; schema may diverge from MBTA | High | T-SC-2 resolves |
| R2 | Ticketmaster may throttle or require paid tier | Medium | T1.4.4 + T-SC-4 resolve |
| R3 | MBTA GTFS-RT streaming needs persistent connection; may need custom adapter | High | T3.2.1 fallback mitigates |
| R4 | Fabric Git integration branch state can diverge from workspace state | Medium | T1.2.1, T1.2.2 mitigate |
| R5 | Open-Meteo has hourly call limits | Low | Daily batch cadence mitigates |
| R6 | F-SKU capacity required for Warehouse and Eventstream | High | CP-1 resolves |
| R7 | Air-gapped or restricted demo environments have no live API access | High | E6 fallback fixtures are non-optional |
| A1 | Single workspace, single capacity, single Git branch per demo environment | — | — |
| A2 | Open-Meteo free tier is unauthenticated (verify in T-SC-3) | — | T-SC-3 confirms |
| A3 | MBTA V3 open data tier used; no key required for read-only static and predictions | — | T-SC-1 confirms |
