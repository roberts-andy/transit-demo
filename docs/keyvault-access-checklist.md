# Key Vault Access Checklist

**Version:** 2026-06-12  
**Status:** ✅ All steps verified and complete

This document provides a complete runbook for setting up and verifying Key Vault access for the transit-demo Bronze notebooks.

## Prerequisites

Before Key Vault wiring can be tested, the following must exist:

1. **Azure Resource Group** — `rg-transit-demo-kv` in subscription `f70cfb6a-3eda-4cd9-856c-eaf4f040a66e` (tenant `da78621e-f352-46cd-b186-fad7b71bb6cf`)
2. **Azure Key Vault** — `kvtransitdemo-f70cfb6a` in the resource group above
3. **Stored API Secrets** — The following secrets must exist in Key Vault:
   - `mbta-api-key` — MBTA API token
   - `wmata-api-key` — WMATA API token
   - `ticketmaster-api-key` — Ticketmaster API token
4. **Fabric Workspace Identity** — The workspace `1771407e-fabc-4774-83fd-572e6347792c` must have an active managed identity enabled
5. **RBAC Assignment** — The workspace identity must have the `Key Vault Secrets User` role on the Key Vault
6. **Fabric Connection** — A Fabric connection named `transit-vault` must be configured to point to the Key Vault
7. **Notebook Configuration** — All Bronze notebooks must be configured with:
   - `API_MODE = "live"`
   - Connection name: `transit-vault`
   - Secret resolution via `resolve_secret()` helper

## Verification Checklist

### 1. Resource Group ✅

Verify the resource group exists and contains the Key Vault:

```bash
az group show --name rg-transit-demo-kv --subscription f70cfb6a-3eda-4cd9-856c-eaf4f040a66e
```

**Expected:** Status is `Succeeded`, location is `eastus` or configured region.

### 2. Key Vault Instance ✅

Verify the Key Vault exists and is accessible:

```bash
az keyvault show --name kvtransitdemo-f70cfb6a --resource-group rg-transit-demo-kv
```

**Expected:** `provisioningState` is `Succeeded`, `enablePurgeProtection` is `true` (recommended).

### 3. Stored Secrets ✅

Verify all three required secrets exist in the Key Vault:

```bash
az keyvault secret list --vault-name kvtransitdemo-f70cfb6a --query "[?attributes.enabled].name" -o tsv
```

**Expected output:**
```
mbta-api-key
ticketmaster-api-key
wmata-api-key
```

### 4. Workspace Identity ✅

Verify the Fabric workspace has an active managed identity:

```bash
az rest --method get \
  --url "https://api.fabric.microsoft.com/v1/workspaces/1771407e-fabc-4774-83fd-572e6347792c/identity" \
  --subscription f70cfb6a-3eda-4cd9-856c-eaf4f040a66e
```

**Expected:** Response includes `principalId` (not null) and `state` is `Active`.

**Current state:**
- Principal ID: `a2e1a377-67a2-46e9-a0e4-20c69ea65bc4`
- State: `Active`

### 5. RBAC Assignment ✅

Verify the workspace identity has the `Key Vault Secrets User` role:

```bash
az role assignment list --assignee a2e1a377-67a2-46e9-a0e4-20c69ea65bc4 \
  --scope /subscriptions/f70cfb6a-3eda-4cd9-856c-eaf4f040a66e/resourceGroups/rg-transit-demo-kv/providers/Microsoft.KeyVault/vaults/kvtransitdemo-f70cfb6a
```

**Expected:** At least one role assignment with `roleDefinitionName` = `Key Vault Secrets User`.

### 6. Fabric Connection ✅

Verify the connection is configured in the Fabric workspace:

- Navigate to **Settings** > **Connections**
- Connection name: `transit-vault`
- Type: `Azure Key Vault`
- Key Vault URI: `https://kvtransitdemo-f70cfb6a.vault.azure.net/`

**Expected:** Connection is marked as `Connected` (green status).

### 7. Notebook Configuration ✅

Verify all Bronze notebooks are configured correctly. Check each notebook for:

**1. `API_MODE` parameter:**
```python
API_MODE = "live"
```

**2. `resolve_secret()` calls:**
```python
from notebookutils.mssparkutils import KeyVault

kv_connection = "transit-vault"
mbta_api_key = mssparkutils.credentials.getSecret(kv_connection, "mbta-api-key")
wmata_api_key = mssparkutils.credentials.getSecret(kv_connection, "wmata-api-key")
ticketmaster_api_key = mssparkutils.credentials.getSecret(kv_connection, "ticketmaster-api-key")
```

**Expected:** All 8 Bronze notebooks contain the above pattern and no hardcoded secrets.

## Troubleshooting

### ❌ "Invalid authentication token" or "403 Forbidden"

**Cause:** RBAC assignment is not yet active or is propagating.  
**Resolution:**
1. Verify the role assignment exists (see step 5 above)
2. Wait 1–2 minutes for Azure RBAC propagation
3. Restart the notebook session
4. Retry the secret retrieval

### ❌ "Connection 'transit-vault' not found"

**Cause:** The Fabric connection is not configured or has the wrong name.  
**Resolution:**
1. Verify the connection name is exactly `transit-vault` (case-sensitive)
2. Verify the Key Vault URI is correct: `https://kvtransitdemo-f70cfb6a.vault.azure.net/`
3. Recreate the connection and test the connection status

### ❌ "Secret not found" or "404 Not Found"

**Cause:** The secret name is misspelled or does not exist in the Key Vault.  
**Resolution:**
1. List all secrets in the Key Vault (see step 3 above)
2. Verify the secret name matches exactly (e.g., `mbta-api-key`, not `mbta_api_key`)
3. If the secret is missing, add it with the correct name:
   ```bash
   az keyvault secret set --vault-name kvtransitdemo-f70cfb6a \
     --name mbta-api-key --value "<api-key-value>"
   ```

### ❌ "Workspace identity not enabled"

**Cause:** The Fabric workspace identity has not been activated.  
**Resolution:**
1. Verify the workspace identity is active (see step 4 above)
2. If the identity state is `Disabled`, enable it:
   ```bash
   az rest --method post \
     --url "https://api.fabric.microsoft.com/v1/workspaces/1771407e-fabc-4774-83fd-572e6347792c/identity" \
     --subscription f70cfb6a-3eda-4cd9-856c-eaf4f040a66e \
     --body '{"state": "Active"}'
   ```
3. Wait a few seconds for the state change to propagate, then retry step 4

### ❌ Notebook hangs when calling `getSecret()`

**Cause:** The Fabric session is not running in the correct workspace or the connection timeout is too short.  
**Resolution:**
1. Verify the notebook is running in the `1771407e-fabc-4774-83fd-572e6347792c` workspace
2. Check network connectivity to Key Vault (no firewall/NSG blocks)
3. Increase the notebook timeout in `parameters.dev.yml` if running a large batch of notebooks

## Current State: 2026-06-12

| Component | Status | Evidence |
|-----------|--------|----------|
| Resource Group `rg-transit-demo-kv` | ✅ Created | Verified via `az group show` |
| Key Vault `kvtransitdemo-f70cfb6a` | ✅ Created | URI: `https://kvtransitdemo-f70cfb6a.vault.azure.net/` |
| Secrets (`mbta-api-key`, `wmata-api-key`, `ticketmaster-api-key`) | ✅ Loaded | All three present in Key Vault |
| Workspace Identity | ✅ Active | Principal ID: `a2e1a377-67a2-46e9-a0e4-20c69ea65bc4`, State: `Active` |
| RBAC Assignment (`Key Vault Secrets User`) | ✅ Granted | Identity has reader access to all secrets |
| Fabric Connection `transit-vault` | ✅ Configured | Connected and pointing to correct KV URI |
| All Bronze Notebooks (8 total) | ✅ Updated | `API_MODE = "live"`, using `resolve_secret()` pattern |

## Demo Setup Quick Reference

To set up a new demo environment or refresh the current one:

1. **Verify prerequisites** — Run all checks in the Verification Checklist above
2. **Start the Fabric workspace** — Open the transit-demo workspace in Fabric
3. **Run Bronze notebooks** — Run the entire `pl_orchestrate_bronze.json` pipeline or individual notebooks
4. **Verify live API calls** — Check notebook logs for successful API calls (HTTP 200) to MBTA, WMATA, Ticketmaster
5. **Confirm data in Silver layer** — Query Silver tables to verify transformed data from Bronze ingestion

For detailed pipeline and notebook documentation, see [`runbook.md`](./runbook.md).
