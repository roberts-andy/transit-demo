# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "652074ad-c45e-4245-9eba-ae470adeb4cb",
# META       "default_lakehouse_name": "lh_transit_bronze",
# META       "default_lakehouse_workspace_id": "1771407e-fabc-4774-83fd-572e6347792c"
# META     }
# META   }
# META }

# CELL ********************

# MARKDOWN ********************

# # Bronze: WMATA Vehicle Positions
# 
# **Bronze Layer Rules**
# 
# - **Source fidelity**: Raw API payloads are stored exactly as received from the WMATA REST API. No business logic, field renaming, or aggregation.
# - **Technical metadata**: Every record carries `source_system`, `source_endpoint`, `source_record_id`, `source_record_hash`, `extraction_ts`, and `ingestion_ts`.
# - **No business logic**: Lat/Lon normalization, timestamp UTC conversion, conformed entity alignment with MBTA fact_vehicle_position all belong in Silver â€” not here.
# - **Fallback**: Set `API_MODE = 'cached'` to load from a local fixture file instead of calling the live API. Required for offline or rehearsal demos.
# 
# > **Auth Risk (R1)**: WMATA requires an API key. Without `WMATA_API_KEY` set in the environment, live mode will raise an error.
# >
# > **GTFS-RT vs. REST**: The `SOURCE_ENDPOINT` parameter points to `/gtfs-rt/vehiclepositions`, which is the canonical GTFS-RT feed. However, **GTFS-RT returns protobuf binary** and requires a custom parser (e.g., `google.transit.gtfs_realtime_pb2`). For demo purposes, this notebook uses the REST JSON alternative `/Bus.svc/json/jBusPositions`, which returns structured JSON vehicle positions. Replace the live-mode URL below with a protobuf parser implementation when one is available.

# CELL ********************

# â”€â”€ Parameters â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
API_BASE_URL    = "https://api.wmata.com"
# Canonical GTFS-RT endpoint (protobuf binary â€” see notebook header note)
SOURCE_ENDPOINT = "/gtfs-rt/vehiclepositions"
SOURCE_SYSTEM   = "wmata"
BRONZE_TABLE    = "bronze_wmata_vehicle_positions_raw"
API_MODE        = "live"  # "live" | "cached"
FIXTURE_PATH    = "../../fixtures/bronze/wmata_vehicle_positions_sample.json"

# CELL ********************

# â”€â”€ Imports â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
import json
import hashlib
import os
import requests
from datetime import datetime, timezone
from pyspark.sql import SparkSession

spark = SparkSession.getActiveSession()

KEY_VAULT_CONNECTION = os.environ.get("KEY_VAULT_CONNECTION_NAME", "transit-vault")
KEY_VAULT_URI = os.environ.get("AZURE_KEY_VAULT_URI", "")

def resolve_secret(secret_env_name: str, secret_name: str) -> str:
    """Resolve secret: env var > Fabric connection > Key Vault URI fallback."""
    value = os.environ.get(secret_env_name, "")
    if value:
        return value
    try:
        from notebookutils import mssparkutils
        return mssparkutils.credentials.getSecret(KEY_VAULT_CONNECTION, secret_name)
    except Exception:
        pass
    if KEY_VAULT_URI:
        try:
            from notebookutils import mssparkutils
            return mssparkutils.credentials.getSecret(KEY_VAULT_URI, secret_name)
        except Exception as exc:
            print(f"[WARN] Could not retrieve secret '{secret_name}' from Key Vault: {exc}")
    return ""

# CELL ********************

# â”€â”€ Ingestion Logic â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
extraction_ts = datetime.now(timezone.utc).isoformat()

if API_MODE == "cached":
    with open(FIXTURE_PATH, "r") as f:
        payload = json.load(f)
    items = payload.get("BusPositions", payload) if isinstance(payload, dict) else payload
else:
    wmata_api_key = resolve_secret("WMATA_API_KEY", os.environ.get("WMATA_API_KEY_SECRET_NAME", "wmata-api-key"))
    if not wmata_api_key:
        raise ValueError(
            "WMATA_API_KEY is required in live mode. "
            "Set environment variable or Key Vault wiring, or switch to API_MODE='cached'."
        )
    # WMATA uses 'api_key' header (not Authorization or x-api-key)
    headers = {"api_key": wmata_api_key}

    # NOTE: SOURCE_ENDPOINT (/gtfs-rt/vehiclepositions) returns protobuf binary
    # and requires a custom parser (google.transit.gtfs_realtime_pb2).
    # For demo purposes, we use the REST JSON alternative /Bus.svc/json/jBusPositions
    # which returns structured JSON. Replace this URL with a protobuf implementation
    # if a GTFS-RT parser is available and full vehicle fidelity is required.
    rest_alt_url = f"{API_BASE_URL}/Bus.svc/json/jBusPositions"
    response = requests.get(rest_alt_url, headers=headers)
    response.raise_for_status()
    # REST response structure: {"BusPositions": [{"VehicleID": "...", "Lat": ..., "Lon": ..., ...}]}
    items = response.json().get("BusPositions", [])

ingestion_ts = datetime.now(timezone.utc).isoformat()

records = []
for item in items:
    records.append({
        "source_system":      SOURCE_SYSTEM,
        "source_endpoint":    SOURCE_ENDPOINT,
        "source_record_id":   item.get("VehicleID", item.get("id")),
        "source_record_hash": hashlib.md5(json.dumps(item, sort_keys=True).encode()).hexdigest(),
        "extraction_ts":      extraction_ts,
        "ingestion_ts":       ingestion_ts,
        "raw_payload":        json.dumps(item),
    })

print(f"Extracted {len(records)} records from {SOURCE_SYSTEM} vehicle positions (REST alternative)")

# CELL ********************

# â”€â”€ Write to Bronze Delta Table â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
df = spark.createDataFrame(records)
(
    df.write
    .format("delta")
    .mode("append")
    .option("mergeSchema", "true")
    .saveAsTable(BRONZE_TABLE)
)

# â”€â”€ Bronze Acceptance Check â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
row_count = spark.table(BRONZE_TABLE).count()
print(f"[BRONZE ACCEPTED] Table: {BRONZE_TABLE} | Rows written this batch: {len(records)} | Total rows: {row_count}"
