# Demo Runbook (Starter)

## Pre-demo checks

- Validate workspace and capacity availability
- Validate API keys for sources that require them
- Validate Bronze landing tables exist
- Validate Silver dependencies refresh successfully
- Validate Gold Warehouse objects load
- Validate fallback/cached demo data is present

## Suggested demo order

1. Introduce source systems
2. Show three ingestion methods
3. Show Bronze raw payloads
4. Show Silver normalization
5. Show three transformation methods
6. Show Gold KPIs and slicing dimensions
7. Close with workload selection guidance

## Fallback strategy

- If live APIs fail, switch to cached Bronze snapshots
- If streaming path is unstable, replay captured events into the stream demo path or show pre-populated Eventhouse results
- If events API is unavailable, keep weather-only enrichment path active

## Live Bronze validation evidence (2026-06-11)

- MBTA and WMATA live endpoint validation passed for all Bronze notebook sources using local `.env.local` keys.
- MBTA:
  - `/predictions?filter[route]=Red` returned HTTP 200 with live records.
  - `/routes`, `/stops`, and `/vehicles` returned HTTP 200 with live records.
- WMATA:
  - `/StationPrediction.svc/json/GetPrediction/All` returned HTTP 200 with live records.
  - `/Bus.svc/json/jRoutes`, `/Bus.svc/json/jStops`, and `/Bus.svc/json/jBusPositions` returned HTTP 200 with live records.

### Validation blocker

- Local terminal validation cannot execute final Delta writes because Bronze notebooks require an active Fabric Spark session (`SparkSession.getActiveSession()`).
- Full end-to-end acceptance must run from Fabric notebook jobs or a Fabric pipeline notebook activity.

## Key Vault runtime secret wiring

- Bronze notebooks now resolve secrets in this order:
  1. Direct environment variable (`MBTA_API_KEY`, `WMATA_API_KEY`)
  2. Azure Key Vault secret via `mssparkutils.credentials.getSecret(AZURE_KEY_VAULT_URI, <secret-name>)`
- Required runtime configuration:
  - `AZURE_KEY_VAULT_URI`
  - `MBTA_API_KEY_SECRET_NAME` (default: `mbta-api-key`)
  - `WMATA_API_KEY_SECRET_NAME` (default: `wmata-api-key`)
- Do not store API keys in repository files.

## Bronze orchestration skeleton

- Master pipeline scaffold: `src/ingestion/pipelines/pl_orchestrate_bronze.json`
- Current orchestration behavior:
  - Runs MBTA Bronze notebooks first, then WMATA notebooks.
  - Uses dependency-safe sequencing and retry policy (`retry: 2`, 30-second interval).
  - Captures basic run log entries via pipeline variables.
