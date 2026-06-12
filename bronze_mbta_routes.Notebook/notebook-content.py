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

# # Bronze: MBTA Routes
# 
# **Bronze Layer Rules**
# 
# - **Source fidelity**: Raw JSON:API payloads are stored exactly as received from the MBTA V3 API. No business logic, field renaming, or aggregation.
# - **Technical metadata**: Every record carries `source_system`, `source_endpoint`, `source_record_id`, `source_record_hash`, `extraction_ts`, and `ingestion_ts`.
# - **No business logic**: JSON:API attribute unwrapping, timestamp normalization to UTC, conformed keys, and derived fields all belong in Silver — not here.
# - **Fallback**: Set `API_MODE = 'cached'` to load from a local fixture file instead of calling the live API. Required for offline or rehearsal demos.

# CELL ********************

# ── Parameters ──────────────────────────────────────────────────────────────
API_BASE_URL    = "https://api-v3.mbta.com"
SOURCE_ENDPOINT = "/routes"
SOURCE_SYSTEM   = "mbta"
BRONZE_TABLE    = "bronze_mbta_routes_raw"
API_MODE        = "live"  # "live" | "cached"
FIXTURE_PATH    = "../../fixtures/bronze/mbta_routes_sample.json"

# CELL ********************

# ── Imports ─────────────────────────────────────────────────────────────────
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

# ── Ingestion Logic ──────────────────────────────────────────────────────────
extraction_ts = datetime.now(timezone.utc).isoformat()

if API_MODE == "cached":
    with open(FIXTURE_PATH, "r") as f:
        payload = json.load(f)
    items = payload.get("data", payload) if isinstance(payload, dict) else payload
else:
    mbta_api_key = resolve_secret("MBTA_API_KEY", os.environ.get("MBTA_API_KEY_SECRET_NAME", "mbta-api-key"))
    headers = {"x-api-key": mbta_api_key} if mbta_api_key else {}
    url = f"{API_BASE_URL}{SOURCE_ENDPOINT}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    items = response.json().get("data", [])

ingestion_ts = datetime.now(timezone.utc).isoformat()

records = []
for item in items:
    records.append({
        "source_system":      SOURCE_SYSTEM,
        "source_endpoint":    SOURCE_ENDPOINT,
        "source_record_id":   item.get("id"),
        "source_record_hash": hashlib.md5(json.dumps(item, sort_keys=True).encode()).hexdigest(),
        "extraction_ts":      extraction_ts,
        "ingestion_ts":       ingestion_ts,
        "raw_payload":        json.dumps(item),
    })

print(f"Extracted {len(records)} records from {SOURCE_SYSTEM}{SOURCE_ENDPOINT}")

# CELL ********************

# ── Write to Bronze Delta Table ──────────────────────────────────────────────
df = spark.createDataFrame(records)
(
    df.write
    .format("delta")
    .mode("append")
    .option("mergeSchema", "true")
    .saveAsTable(BRONZE_TABLE)
)

# ── Bronze Acceptance Check ──────────────────────────────────────────────────
row_count = spark.table(BRONZE_TABLE).count()
print(f"[BRONZE ACCEPTED] Table: {BRONZE_TABLE} | Rows written this batch: {len(records)} | Total rows: {row_count}"
