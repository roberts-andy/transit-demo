# Fabric Transit Demo

A Microsoft Fabric demo that showcases **multiple ingestion and transformation patterns** using public transit, weather, and public event data.

## What this demo proves
- Batch ingestion with **Spark Notebooks**
- Batch ingestion/orchestration with **Fabric Data Factory Pipelines**
- Streaming ingestion with **Eventstreams**
- Low-code transformation with **Dataflow Gen2**
- Code-first transformation with **Notebooks**
- SQL/declarative transformation with **Materialized Lake Views**
- Medallion design across **Bronze / Silver / Gold**
- KPI serving from a **Fabric Warehouse**

## Source systems in scope
- MBTA API (Boston)
- WMATA API (Washington, DC)
- Open-Meteo hourly weather API
- Ticketmaster Discovery API (optional public events source)

## Repository structure
- `docs/` – product spec, architecture, and runbook guidance
- `.squad/` – team definition, routing, ceremonies, and agent charters
- `infra/` – parameter and environment examples
- `data_contracts/` – source and entity definitions
- `src/` – implementation placeholders by Fabric workload
- `tests/` – validation checklist placeholders

## Suggested Fabric layout
- `lh_transit_bronze`
- `lh_transit_silver`
- `eh_transit_realtime`
- `wh_transit_gold`

## Notes
This scaffold is designed to be committed into a Git-backed Fabric project and adapted to your target workspace / capacity / demo narrative.
