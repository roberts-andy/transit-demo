---
title: "Bronze Fixture Snapshots"
description: "Cached Bronze-layer snapshots for demo fallback. Used when live APIs are unavailable."
---

## Purpose

This directory holds pre-captured snapshot files from each source system. These are loaded by `src/fixtures/load_fixtures.ipynb` when `api_mode = 'cached'`.

## Files (populate after CP-4 live API keys are available)

- `mbta_routes_sample.json` — MBTA /routes response
- `mbta_stops_sample.json` — MBTA /stops response
- `mbta_predictions_sample.json` — MBTA /predictions response (filtered by route)
- `mbta_vehicles_sample.json` — MBTA /vehicles response
- `wmata_routes_sample.json` — WMATA routes
- `wmata_stops_sample.json` — WMATA stops
- `wmata_predictions_sample.json` — WMATA predictions
- `wmata_vehicle_positions_sample.json` — WMATA vehicle positions
- `open_meteo_sample.json` — Open-Meteo hourly weather (both cities)

## Skill reference

`demo-readiness-and-fallback` Pattern 3: fallback is part of the design, not an afterthought.
