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
