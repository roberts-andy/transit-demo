# Architecture Notes

## Reference decisions
- Favor a **medallion pattern** because the demo explicitly needs Bronze / Silver / Gold and SQL-defined step-ups.
- Use **UTC** as the canonical event timestamp standard in Silver and Gold.
- Keep **Bronze immutable** except for technical ingestion metadata.
- Prefer **Warehouse** for curated KPI serving and demonstration queries.

## Component mapping
### Bronze
- Lakehouse tables for batch raw payloads
- Eventhouse / KQL DB for streaming telemetry if needed
- Eventstream destinations feeding Lakehouse or Eventhouse

### Silver
- Notebook transformations for transit-domain normalization
- Dataflow Gen2 for low-code cleanup / shaping
- Lakehouse curated delta tables

### Gold
- Materialized Lake Views for SQL-defined reusable aggregations
- Fabric Warehouse for presentation mart / semantic-ready SQL model

## Example table pattern
### dim_city
- city_key
- city_name
- metro_area
- state_or_region
- transit_agency_code

### dim_route
- route_key
- agency_code
- city_key
- source_route_id
- route_short_name
- route_long_name
- route_type

### dim_stop
- stop_key
- agency_code
- city_key
- source_stop_id
- stop_name
- latitude
- longitude
- parent_station_id

### fact_prediction_snapshot
- prediction_snapshot_key
- agency_code
- city_key
- route_key
- stop_key
- trip_key
- vehicle_key
- event_timestamp_utc
- predicted_arrival_utc
- predicted_departure_utc
- predicted_delay_seconds
- source_record_ts_utc

### fact_vehicle_position
- vehicle_position_key
- agency_code
- city_key
- route_key
- vehicle_key
- trip_key
- event_timestamp_utc
- latitude
- longitude
- bearing
- current_status

### fact_hourly_weather
- weather_hour_key
- city_key
- weather_timestamp_utc
- temperature_c
- precipitation_mm
- precipitation_probability_pct
- wind_speed_kmh
- visibility_m
- weather_code

## Correlation logic ideas
- Join route / stop delay windows with same-hour weather by city
- Join event windows to nearby stop / route hours using city + local day + hour buckets
- Derive `is_event_window` and `is_adverse_weather` flags for sliceable KPI analysis

## Semantic model starter views
- vw_gold_route_hourly_performance
- vw_gold_stop_daily_performance
- vw_gold_city_weather_correlation
- vw_gold_event_impact_summary
