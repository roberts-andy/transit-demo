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

# # Bronze: WMATA Predictions
# 
# **Bronze Layer Rules**
# 
# - **Source fidelity**: Raw API payloads are stored exactly as received from the WMATA API. No business logic, field renaming, or aggregation.
# - **Technical metadata**: Every record carries `source_system`, `source_endpoint`, `source_record_id`, `source_record_hash`, `extraction_ts`, and `ingestion_ts`.
# - **No business logic**: `predicted_arrival_utc` derivation from relative `Min` field, StationCode normalization, and Silver conformed alignment with MBTA predictions all belong in Silver â€” not here.
# - **Fallback**: Set `API_MODE = 'cached'` to load from a local fixture file instead of calling the live API. Required for offline or rehearsal demos.
# 
# > **Auth Risk (R1)**: WMATA requires an API key. Without `WMATA_API_KEY` set in the environment, live mode will raise an error.
# >
# > **Schema difference vs. MBTA**: WMATA predictions use a relative `Min` field (integer minutes until arrival) rather than an absolute ISO 8601 timestamp. Silver computes `predicted_arrival_utc = extraction_ts + timedelta(minutes=Min)`. This difference is intentionally preserved raw in Bronze.
# >
# > **Endpoint note**: `/StationPrediction.svc/json/GetPrediction/All` returns all stations in one call as `{"Trains": [...]}`. Bus predictions use a separate endpoint and are not covered here.

# CELL ********************

# â”€â”€ Parameters â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
API_BASE_URL    = "https://api.wmata.com"
SOURCE_ENDPOINT = "/StationPrediction.svc/json/GetPrediction/All"
SOURCE_SYSTEM   = "wmata"
BRONZE_TABLE    = "bronze_wmata_predictions_raw"
API_MODE        = "live"  # "live" | "cached"
FIXTURE_PATH    = "../../fixtures/bronze/wmata_predictions_sample.json"

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
    # WMATA GetPrediction returns {"Trains": [...]} â€” handle both raw and pre-extracted
    items = payload.get("Trains", payload) if isinstance(payload, dict) else payload
else:
    wmata_api_key = resolve_secret("WMATA_API_KEY", os.environ.get("WMATA_API_KEY_SECRET_NAME", "wmata-api-key"))
    if not wmata_api_key:
        raise ValueError(
            "WMATA_API_KEY is required in live mode. "
            "Set environment variable or Key Vault wiring, or switch to API_MODE='cached'."
        )
    # WMATA uses 'api_key' header (not Authorization or x-api-key)
    headers = {"api_key": wmata_api_key}
    url = f"{API_BASE_URL}{SOURCE_ENDPOINT}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    # Response structure: {"Trains": [{"Car": "6", "Line": "RD", "LocationCode": "A01", "Min": "3", ...}]}
    items = response.json().get("Trains", [])

ingestion_ts = datetime.now(timezone.utc).isoformat()

records = []
for item in items:
    # WMATA predictions have no single stable ID field â€” use composite of Line + LocationCode + Car
    source_record_id = f"{item.get('Line', '')}-{item.get('LocationCode', '')}-{item.get('Car', '')}"
    records.append({
        "source_system":      SOURCE_SYSTEM,
        "source_endpoint":    SOURCE_ENDPOINT,
        "source_record_id":   source_record_id,
        "source_record_hash": hashlib.md5(json.dumps(item, sort_keys=True).encode()).hexdigest(),
        "extraction_ts":      extraction_ts,
        "ingestion_ts":       ingestion_ts,
        "raw_payload":        json.dumps(item),
    })

print(f"Extracted {len(records)} records from {SOURCE_SYSTEM}{SOURCE_ENDPOINT}")

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
print(f"[BRONZE ACCEPTED] Table: {BRONZE_TABLE} | Rows written this batch: {len(records)} | Total rows: {row_count}")