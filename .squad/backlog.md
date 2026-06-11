# Squad Backlog

## Current Sprint / Active Work Set

- Sprint ID: Sprint-2026-06-11-Bronze-Stabilization
- Objective: complete live Bronze execution evidence, finish Key Vault runtime wiring, and harden Bronze orchestration for demo-safe runs.
- Owner: Lead

## Active Tasks Board

| Task ID | Task | Assigned Agent | Status | Notes |
|---|---|---|---|---|
| EX-1 | Run MBTA and WMATA Bronze notebooks in Fabric runtime and capture write-validation evidence (saveAsTable, row counts, metadata columns) | Batch Ingestion Engineer | In Progress | 2026-06-11 preflight PASS: MBTA /routes=200 (178), WMATA TrainPositions=200 (106); Fabric runtime write evidence still pending |
| EX-2 | Finalize Key Vault runtime wiring (key_vault_uri, secret-name mapping, access checklist) for Bronze notebooks | DemoOps / QA Engineer | In Progress | Runs in parallel with EX-1 |
| EX-3 | Harden pl_orchestrate_bronze.json with explicit failure branches and schedule trigger settings | Batch Ingestion Engineer | Not Started | Starts after EX-1 evidence checkpoint |
| EX-4 | Update runbook and execution evidence log for Sprint-2026-06-11-Bronze-Stabilization | Scribe | Not Started | Starts after EX-1 and EX-2 |

## Decisions and Assumptions

- Decision: EX-1 is the execution gate for this sprint. EX-3 and EX-4 cannot be marked complete until Fabric runtime evidence exists.
- Assumption: Fabric workspace execution identity can read Key Vault secrets after access policy or RBAC assignment.
