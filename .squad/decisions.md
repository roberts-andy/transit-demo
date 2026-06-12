# Squad Decisions

## Active Decisions

### 2026-06-11: Dashboard Canonical Source Sync
- Decision: root Squad dashboard files are now synchronized from transit squad runtime state so dashboard views can render roster, sprint, and tasks from canonical root paths.
- Reason: execution tracking existed under .squad/squads/transitdemo but root files were template/empty.

### 2026-06-11: Sprint Gate Assumption
- Assumption: Fabric workspace execution identity will have secret-read access before final sprint sign-off.

### 2026-06-11: EX-1 Preflight Evidence Logged
- Decision: keep EX-1 as In Progress after live preflight until Fabric runtime write evidence is captured.
- Evidence: MBTA /routes HTTP 200 (178), WMATA TrainPositions HTTP 200 (106), 8 Bronze notebooks detected.

### 2026-06-11: Azure Infra Lead Added and Assigned
- Decision: add Azure Infra Lead as an active squad member responsible for Azure resource provisioning and shared configuration handoff.
- Assignment: EX-5 created to provision resource group + Key Vault, grant Fabric workspace identity secret-reader access, and load required secrets.
- Azure Context: Azure CLI pinned to subscription f70cfb6a-3eda-4cd9-856c-eaf4f040a66e in tenant da78621e-f352-46cd-b186-fad7b71bb6cf.

### 2026-06-11: EX-3 hardening and EX-2 close-prep update
- Decision: set EX-3 to In Progress with explicit failure handling in `pl_orchestrate_bronze.json` while preserving MBTA then WMATA dependency order.
- Evidence: each notebook activity now has an OnFailure path that records failed activity context into `run_log` through `last_failed_activity`.
- Evidence: notebook retries/timeouts confirmed; pipeline logging/failure activities also include retry/timeout policy values.

### 2026-06-11: EX-5 Azure provisioning executed
- Decision: execute EX-5 immediately under subscription `f70cfb6a-3eda-4cd9-856c-eaf4f040a66e` and tenant `da78621e-f352-46cd-b186-fad7b71bb6cf`.
- Evidence: created resource group `rg-transit-demo-kv` and Key Vault `kvtransitdemo-f70cfb6a`.
- Evidence: loaded secrets `mbta-api-key`, `wmata-api-key`, `ticketmaster-api-key` into Key Vault.
- Evidence: updated `infra/parameters.dev.yml` with `key_vault_uri=https://kvtransitdemo-f70cfb6a.vault.azure.net/`.
- Blocker: Fabric workspace identity principal is not enabled/resolvable yet; Key Vault reader assignment is pending identity enablement.
- Required next command: `az rest --method post --url "https://api.fabric.microsoft.com/v1/workspaces/1771407e-fabc-4774-83fd-572e6347792c/identity"`

## Governance

- All meaningful changes require team consensus
- Document architectural decisions here
- Keep history focused on work, decisions focused on direction
