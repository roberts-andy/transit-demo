# Shared Decision Log

- Decision records will be added here as the squad converges on architecture, source contracts, and demo flow.

---

## 2026-06-11: Execution kickoff decisions

### CP-1 through CP-4 — Human action required (BLOCKED)

The following critical path items require human action before any Fabric implementation can run:

- **CP-1** — Provision Fabric workspace and confirm F-SKU or Trial capacity
- **CP-2** — Create four Fabric items: `lh_transit_bronze`, `lh_transit_silver`, `eh_transit_realtime`, `wh_transit_gold`
- **CP-3** — Connect repo to Fabric via Git integration
- **CP-4** — Obtain and vault API keys: MBTA, WMATA, Open-Meteo

Until CP-1 through CP-4 are complete, all notebooks run in `api_mode = cached` against fixture files.

### MBTA V3 API auth approach confirmed

MBTA V3 open-data tier is unauthenticated for read-only access. An optional `MBTA_API_KEY` header can be added for higher rate limits. All MBTA Bronze notebooks accept the key via environment variable but do not require it.

**Source:** backlog assumption A3

### WMATA API key is required — no open-data tier

WMATA has no unauthenticated tier. All WMATA Bronze notebooks will raise an error if `WMATA_API_KEY` is not set in the environment and `api_mode = live`.

**Source:** backlog risk R1 — confirmed at implementation start

### Open-Meteo is unauthenticated — confirmed

Open-Meteo free tier requires no API key. Weather pipeline and notebooks do not include an auth header. Timestamps from Open-Meteo are UTC natively — no server-side conversion is needed in Bronze.

**Source:** backlog assumption A2

### Bronze notebook pattern locked

All Bronze notebooks (MBTA + WMATA, 8 total) follow the `bronze-ingestion-pattern` skill exactly:
- Technical metadata: `source_system`, `source_endpoint`, `source_record_id`, `source_record_hash`, `extraction_ts`, `ingestion_ts`
- `raw_payload` stored as JSON string
- No business logic in Bronze
- `api_mode` parameter controls live vs. cached execution

### Ticketmaster source contract deferred

T-SC-4 (Ticketmaster/fallback source contract) is deferred until T1.4.4 decision on fallback source is made. The public events ingestion path (F2.4) is blocked until T-SC-4 is resolved.

### Source contracts written for MBTA, WMATA, and Open-Meteo

T-SC-1, T-SC-2, and T-SC-3 are now complete. Files created:
- `data_contracts/sources/mbta-source-contract.yml`
- `data_contracts/sources/wmata-source-contract.yml`
- `data_contracts/sources/open-meteo-source-contract.yml`

These gate F2.1, F2.2, F2.3, and F3.1 Bronze ingestion work.

---

## 2026-06-11: User unblock inputs received

### Capacity and workspace confirmed

- Capacity: `andyfabcentral`
- Workspace requested name: `TransitDemo`
- Workspace discovered via Fabric API: `transit-demo` (`1771407e-fabc-4774-83fd-572e6347792c`)

CP-1 can proceed as complete from project-planning perspective.

### Git integration confirmed

User confirmed the Fabric workspace is connected to this repository.

CP-3 marked complete.

### Core Fabric items provisioned via API

- `lh_transit_bronze` (Lakehouse): `652074ad-c45e-4245-9eba-ae470adeb4cb`
- `lh_transit_silver` (Lakehouse): `bd6c7417-3f8f-4b49-b9eb-498cb09b46a9`
- `wh_transit_gold` (Warehouse): `26d157ff-e24c-4503-bced-76760f91090d`
- `eh_transit_realtime` (Eventhouse): `daf2482a-15f1-4c5b-b0e9-f3a59d219777`
- `es_transit_realtime` (Eventstream): `29e74f19-93d9-486b-9adc-b3ad9c752c5d`

Note: Fabric auto-created SQL Endpoints for each Lakehouse and a KQL Database within the Eventhouse.

### API keys received for live validation

User provided MBTA, WMATA, and Ticketmaster API keys in chat. Keys are being consumed via local-only environment configuration and must not be committed to git.

CP-4 is now in progress: key acquisition is complete, secure vault wiring in Fabric still pending.

### Demo fallback policy clarified

The previous question about fallback mode means: if live APIs fail during demo, should the demo auto-switch to cached fixtures so the narrative still works.

Default for execution is now: **fallback enabled**.

### Live API connectivity checks passed

Using local-only environment variables, live connectivity checks succeeded:

- MBTA `/routes`: successful response (178 route records)
- WMATA `/StationPrediction.svc/json/GetPrediction/All`: successful response (567 train records)
- Ticketmaster `/discovery/v2/events.json`: successful response (`size=1` smoke test)

This confirms Bronze live-source preconditions are met for external APIs.

---

## 2026-06-11: Bronze live validation + runtime wiring updates

### Bronze live source validation completed for MBTA and WMATA notebooks

Live checks were executed against all MBTA and WMATA Bronze notebook source endpoints with local-only keys from `.env.local`.

- MBTA endpoints validated: `/predictions?filter[route]=Red`, `/routes`, `/stops`, `/vehicles`
- WMATA endpoints validated: `/StationPrediction.svc/json/GetPrediction/All`, `/Bus.svc/json/jRoutes`, `/Bus.svc/json/jStops`, `/Bus.svc/json/jBusPositions`
- Result: all endpoints returned HTTP 200 with live payloads.

### Blocker: local environment cannot validate Delta writes

Notebook ingestion logic requires `SparkSession.getActiveSession()`. Full Bronze acceptance (`saveAsTable` + post-write row count) must run inside Fabric notebook runtime or pipeline notebook activities.

### Key Vault-first secret resolution adopted for Bronze notebooks

MBTA and WMATA Bronze notebooks now resolve secrets using this order:

1. Environment variable (`MBTA_API_KEY` / `WMATA_API_KEY`)
2. Key Vault lookup via `mssparkutils.credentials.getSecret(AZURE_KEY_VAULT_URI, secret_name)`

Secret names are runtime-configurable with defaults:

- `MBTA_API_KEY_SECRET_NAME=mbta-api-key`
- `WMATA_API_KEY_SECRET_NAME=wmata-api-key`

### Bronze orchestration sequencing decision

`pl_orchestrate_bronze` now exists as the master skeleton and sequences ingestion in a dependency-safe order:

- MBTA: routes -> stops -> predictions -> vehicles
- WMATA: routes -> stops -> predictions -> vehicle positions

The skeleton includes baseline retry and run-log variables for observability.

---

## 2026-06-11: Execution tracking mode activated

### Sprint activation

- Active work set: `Sprint-2026-06-11-Bronze-Stabilization`
- Sprint gate decision: Bronze Fabric runtime write validation is the first execution gate for sprint completion.

### Assumption recorded

- Assumption: Fabric workspace execution identity will be granted Key Vault secret-read permissions before final demo rehearsal.

## EX-1 Evidence Note - 2026-06-11 14:11:00
- **Preflight Result**: PASS.
- **Notebook Inventory**: 8 Bronze notebooks confirmed in src/ingestion/notebooks.
- **Live Endpoint Checks**:
	- MBTA /routes -> HTTP 200, records=178
	- WMATA TrainPositions -> HTTP 200, records=106
- **Remaining Gate**: Full EX-1 completion still requires Fabric runtime write evidence (saveAsTable + post-write row counts).

## EX-2 Kickoff/Progress Note - 2026-06-11 14:11:00
- **Readiness**: Notebooks integrated with resolve_secret and mssparkutils.credentials.getSecret. Secret names standardized.
- **Blockers**: AZURE_KEY_VAULT_URI is empty/placeholder in parameters.dev.yml and .env.template.

