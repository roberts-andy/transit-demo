# Product Specification — Fabric Transit Demo

## 1. Purpose
Build a Microsoft Fabric demo that shows **multiple valid ways to ingest and transform data** using the same business scenario: public transit operations for Boston and Washington, DC.

The demo should make it easy to explain:
1. Why Fabric supports both ETL and ELT patterns
2. When to use notebooks vs Data Factory vs Eventstreams vs Dataflow Gen2 vs Materialized Lake Views
3. How OneLake + medallion design + Warehouse serving work together

## 2. Audience
- Data platform architects
- Fabric engineers / data engineers
- Analytics leaders
- Customers comparing low-code and code-first integration patterns
- Customers evaluating batch + real-time patterns in one platform

## 3. Demo objective
Demonstrate a unified analytics platform that ingests transit, weather, and public event data into Fabric, transforms it into curated entities, and exposes gold KPIs for reporting and storytelling.

## 4. Business story
Transit operators, city analysts, and event planners need a unified view of:
- real-time vehicle movement
- predicted arrival performance
- route and stop metadata
- weather conditions that may affect service
- major public events that may create demand spikes or delays

The demo answers:
- Are vehicles arriving on time?
- Which routes or stops underperform?
- How do weather and public events correlate with delays or headway variability?
- How can the same platform support streaming, batch, low-code, and code-first transformation?

## 5. In-scope Fabric capabilities
### Ingestion patterns to show
- Spark Notebook ingestion
- Fabric Data Factory Pipeline ingestion
- Eventstream ingestion

### Transformation patterns to show
- Dataflow Gen2
- Spark Notebook transformations
- Materialized Lake Views

### Serving pattern to show
- Gold-model serving in Fabric Warehouse

## 6. Source systems
### 6.1 Transit APIs
#### MBTA (Boston)
Use MBTA V3 endpoints such as:
- `/routes`
- `/stops`
- `/trips`
- `/predictions`
- `/vehicles`
- `/shapes`
- `/alerts`

#### WMATA (Washington, DC)
Use WMATA APIs / GTFS / GTFS-RT for:
- train arrivals / bus predictions
- schedules
- static routes and stops
- vehicle positions
- alerts

### 6.2 Weather
Use Open-Meteo hourly weather forecast / recent history for:
- temperature
- precipitation
- precipitation probability
- wind speed / direction
- visibility
- weather code

### 6.3 Public events
Use Ticketmaster Discovery API (or another public events source if preferred) for:
- event title
- venue / location
- start date / time
- classification / genre
- city / metro area

## 7. Layered architecture
### Bronze layer
Purpose: preserve raw source fidelity.

Persist raw payloads from each source into a Lakehouse and/or Eventhouse:
- raw MBTA API responses
- raw WMATA API / GTFS-RT payloads
- raw weather API responses
- raw public events payloads
- eventstream landings for streaming entities

Bronze rules:
- retain source-native field names where practical
- keep ingestion timestamp
- keep source system name
- keep source record id / hash where available
- avoid business logic except minimal technical normalization required for parsing

### Silver layer
Purpose: normalize and model shared entities.

Silver outputs should:
- harmonize city-specific transit shapes into common entities
- standardize timestamps to UTC
- normalize route, stop, vehicle, trip, and prediction concepts into shared schemas
- derive conformed date/time attributes
- create surrogate / business keys where needed
- filter corrupted / unusable records
- support dimensional and fact-style analytical design

### Gold layer
Purpose: analytics-ready Warehouse model.

Gold should provide:
- facts for transit performance and demand context
- dimensions for city, route, stop, vehicle, event, weather period, and date/time
- KPI tables/views for reporting

## 8. Canonical entities
### Bronze entities
- bronze_mbta_routes_raw
- bronze_mbta_stops_raw
- bronze_mbta_predictions_raw
- bronze_mbta_vehicles_raw
- bronze_wmata_routes_raw
- bronze_wmata_stops_raw
- bronze_wmata_predictions_raw
- bronze_wmata_vehicle_positions_raw
- bronze_weather_hourly_raw
- bronze_public_events_raw
- bronze_transit_stream_raw

### Silver dimensions
- dim_city
- dim_agency
- dim_route
- dim_stop
- dim_vehicle
- dim_trip
- dim_date
- dim_time
- dim_weather_condition
- dim_event_venue
- dim_public_event

### Silver facts / normalized entities
- fact_vehicle_position
- fact_prediction_snapshot
- fact_service_alert
- fact_hourly_weather
- fact_event_calendar
- fact_transit_observation_window

### Gold facts / marts
- mart_on_time_performance
- mart_headway_reliability
- mart_stop_delay_summary
- mart_route_delay_summary
- mart_weather_delay_correlation
- mart_event_impact_summary

## 9. KPI candidates
- On-time performance % by city / route / stop / hour / day
- Average predicted lateness by city / route / stop
- Headway variance by route and time-of-day
- Vehicle utilization proxy (count of active vehicles by route / hour)
- Delay correlation versus precipitation / wind / visibility bands
- Delay correlation versus major public event windows
- Top problematic stops by lateness / bunching
- Daily service reliability trend

## 10. Fabric workload mapping
### 10.1 Notebook ingestion path
Use Spark notebooks for:
- API extraction patterns that need custom code
- pagination / retry logic
- JSON flattening
- GTFS / GTFS-RT parsing
- full control over bronze landing format

Suggested notebook examples:
- `nb_ingest_mbta_predictions`
- `nb_ingest_wmata_vehicle_positions`
- `nb_ingest_openmeteo_hourly`

### 10.2 Data Factory pipeline path
Use pipelines for:
- orchestrating notebook runs
- copy / HTTP-based ingestion patterns
- parameterized runs by city / source / environment
- scheduled refresh orchestration

Suggested pipeline examples:
- `pl_batch_transit_ingestion`
- `pl_weather_ingestion`
- `pl_gold_refresh`

### 10.3 Eventstream path
Use Eventstreams for:
- real-time ingestion demonstrations
- routing transit event feeds into Eventhouse and/or Lakehouse
- showing no-code or SQL operator transformations for stream processing

Suggested stream examples:
- `es_transit_positions`
- `es_transit_predictions`

### 10.4 Dataflow Gen2 path
Use Dataflow Gen2 for:
- low-code shaping of weather and event datasets
- join / cleanse / standardize exercises
- showing business-friendly transformation authoring

Suggested examples:
- standardize weather condition codes
- normalize event venue / city names
- apply conformed date/time columns

### 10.5 Materialized Lake Views path
Use Materialized Lake Views for:
- SQL-defined silver-to-gold transformations
- reusable query-ready aggregated assets
- automatic dependency-aware refresh

Suggested MLV examples:
- `mlv_silver_prediction_enriched`
- `mlv_gold_route_hourly_performance`
- `mlv_gold_stop_daily_performance`

## 11. Recommended implementation split by workload
### Ingestion showcase
- **Notebook**: MBTA + WMATA REST pull into Bronze Lakehouse
- **Pipeline**: Pipeline orchestrates weather + event ingestion and triggers notebook execution
- **Eventstream**: Streaming feed lands into Eventhouse/Lakehouse for real-time telemetry pattern

### Transformation showcase
- **Dataflow Gen2**: Weather + events cleanup and standardization
- **Notebook**: Raw transit JSON/GTFS normalization into conformed silver entities
- **Materialized Lake Views**: SQL-based silver-to-gold aggregations

## 12. Suggested demo flow
1. Show source systems and explain why transit is a strong scenario
2. Show raw Bronze landing in Lakehouse / Eventhouse
3. Show each ingestion method separately
4. Show Silver normalization and conformed model
5. Show multiple transformation methods on the same underlying data
6. Show Gold Warehouse KPI model
7. Show report slicing by city, route, stop, weather, and event context
8. Close with guidance: “when to use which Fabric workload”

## 13. Non-functional goals
- Repeatable demo refresh
- Clear environment parameterization
- No secrets committed to repo
- Demo-friendly dataset sizes and refresh windows
- Cost-aware execution
- Minimal setup friction for account teams or field reuse

## 14. Assumptions
- Public APIs remain available and suitable for demo use
- Fabric workspace has required capacity and permissions
- A Git-backed Fabric workspace is available for item lifecycle management
- Warehouse, Eventhouse, Lakehouse, Notebook, Dataflow Gen2, Data Pipeline, and Eventstream items are available in the chosen environment

## 15. Risks / watchouts
- Real-time public transit feeds can change unpredictably
- Public event APIs may require registration and quotas
- Cross-city schema differences require careful normalization
- Streaming demos need a fallback recording / cached data path
- Public API rate limits may affect live demo reliability

## 16. MVP scope
### Phase 1 (recommended MVP)
- MBTA + WMATA routes / stops / predictions / vehicles
- Open-Meteo hourly weather
- Notebook ingestion + Pipeline orchestration + Eventstream ingestion demo
- Notebook + Dataflow Gen2 + Materialized Lake Views transformation demo
- Gold Warehouse KPI model with on-time performance + route / stop summaries

### Phase 2 (optional)
- Ticketmaster or municipal event feeds
- alerting / Real-Time Dashboard / Activator extensions
- geospatial map visuals
- multi-environment CI/CD automation
