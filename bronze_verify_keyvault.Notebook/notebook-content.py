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

# # Bronze Key Vault Verification
# 
# **Purpose**: Validate end-to-end Fabric runtime capabilities for EX-1 sprint gate.
# 
# This notebook confirms:
# 1. Secrets can be resolved from Key Vault via the `transit-vault` connection
# 2. MBTA and WMATA APIs are reachable with resolved credentials
# 3. Delta table writes succeed in the default lakehouse
# 
# **Prerequisites**:
# - Workspace identity enabled and granted Key Vault Secrets User role
# - Key Vault connection `transit-vault` configured in workspace
# - Secrets `mbta-api-key` and `wmata-api-key` loaded in Key Vault
# - Default lakehouse attached to this notebook

# CELL ********************

# ── Step 1: Resolve Secrets from Key Vault ──────────────────────────────────
from notebookutils import mssparkutils

KEY_VAULT_CONNECTION = "transit-vault"
results = {}
errors = []

# Resolve MBTA secret
try:
    mbta_key = mssparkutils.credentials.getSecret(KEY_VAULT_CONNECTION, "mbta-api-key")
    if mbta_key:
        results["mbta_secret"] = "✅ PASS"
        print(f"mbta-api-key: ****{mbta_key[-4:] if len(mbta_key) >= 4 else '****'}")
    else:
        results["mbta_secret"] = "❌ FAIL: Empty secret"
        errors.append("MBTA secret resolved but empty")
except Exception as e:
    results["mbta_secret"] = f"❌ FAIL: {str(e)}"
    errors.append(f"MBTA secret resolution failed: {str(e)}")
    mbta_key = None

# Resolve WMATA secret
try:
    wmata_key = mssparkutils.credentials.getSecret(KEY_VAULT_CONNECTION, "wmata-api-key")
    if wmata_key:
        results["wmata_secret"] = "✅ PASS"
        print(f"wmata-api-key: ****{wmata_key[-4:] if len(wmata_key) >= 4 else '****'}")
    else:
        results["wmata_secret"] = "❌ FAIL: Empty secret"
        errors.append("WMATA secret resolved but empty")
except Exception as e:
    results["wmata_secret"] = f"❌ FAIL: {str(e)}"
    errors.append(f"WMATA secret resolution failed: {str(e)}")
    wmata_key = None

print("\n[Secret Resolution Complete]")

# CELL ********************

# ── Step 2: Test API Connectivity ────────────────────────────────────────────
import requests

# Test MBTA API
if mbta_key:
    try:
        mbta_url = "https://api-v3.mbta.com/routes"
        headers = {"x-api-key": mbta_key}
        response = requests.get(mbta_url, headers=headers, timeout=10)
        response.raise_for_status()
        mbta_data = response.json().get("data", [])
        results["mbta_api"] = "✅ PASS"
        print(f"MBTA /routes: HTTP {response.status_code} | {len(mbta_data)} records")
    except Exception as e:
        results["mbta_api"] = f"❌ FAIL: {str(e)}"
        errors.append(f"MBTA API call failed: {str(e)}")
else:
    results["mbta_api"] = "⏭️ SKIPPED: No secret"
    print("MBTA API test skipped (no secret)")

# Test WMATA API
if wmata_key:
    try:
        wmata_url = "https://api.wmata.com/Rail.svc/json/jStations"
        headers = {"api_key": wmata_key}
        response = requests.get(wmata_url, headers=headers, timeout=10)
        response.raise_for_status()
        wmata_data = response.json().get("Stations", [])
        results["wmata_api"] = "✅ PASS"
        print(f"WMATA /jStations: HTTP {response.status_code} | {len(wmata_data)} records")
    except Exception as e:
        results["wmata_api"] = f"❌ FAIL: {str(e)}"
        errors.append(f"WMATA API call failed: {str(e)}")
else:
    results["wmata_api"] = "⏭️ SKIPPED: No secret"
    print("WMATA API test skipped (no secret)")

print("\n[API Connectivity Tests Complete]")

# CELL ********************

# ── Step 3: Test Delta Table Write ───────────────────────────────────────────
from pyspark.sql import SparkSession
from datetime import datetime, timezone

spark = SparkSession.getActiveSession()
TEST_TABLE = "bronze_verify_test"

try:
    # Create test data
    test_data = [
        {"id": 1, "name": "test_record_1", "ts": datetime.now(timezone.utc).isoformat()},
        {"id": 2, "name": "test_record_2", "ts": datetime.now(timezone.utc).isoformat()},
        {"id": 3, "name": "test_record_3", "ts": datetime.now(timezone.utc).isoformat()},
    ]
    
    # Write to Delta
    df = spark.createDataFrame(test_data)
    df.write.format("delta").mode("overwrite").saveAsTable(TEST_TABLE)
    print(f"Wrote {len(test_data)} rows to {TEST_TABLE}")
    
    # Read back and verify
    df_read = spark.table(TEST_TABLE)
    row_count = df_read.count()
    
    if row_count == len(test_data):
        results["delta_write"] = "✅ PASS"
        print(f"Read back {row_count} rows from {TEST_TABLE} (verified)")
    else:
        results["delta_write"] = f"❌ FAIL: Expected {len(test_data)} rows, got {row_count}"
        errors.append(f"Delta read verification failed: row count mismatch")
        
except Exception as e:
    results["delta_write"] = f"❌ FAIL: {str(e)}"
    errors.append(f"Delta table write failed: {str(e)}")

print("\n[Delta Table Write Test Complete]")

# CELL ********************

# ── Step 4: Verification Summary ─────────────────────────────────────────────
print("="*70)
print("BRONZE KEY VAULT VERIFICATION SUMMARY")
print("="*70)

for step, status in results.items():
    print(f"{step.upper()}: {status}")

print("="*70)

if not errors:
    print("\n✅ PASS: Secrets resolved, APIs reachable, Delta write confirmed")
    print("\nEX-1 Sprint Gate: READY FOR SIGN-OFF")
else:
    print("\n❌ FAIL: One or more verification steps failed")
    print("\nFailure Details:")
    for error in errors:
        print(f"  - {error}")
    print("\nEX-1 Sprint Gate: NOT READY (resolve failures above)")

# CELL ********************

# ── Step 5: Cleanup ──────────────────────────────────────────────────────────
try:
    spark.sql(f"DROP TABLE IF EXISTS {TEST_TABLE}")
    print(f"Cleaned up test table: {TEST_TABLE}")
except Exception as e:
    print(f"Warning: Could not drop test table {TEST_TABLE}: {str(e)}")