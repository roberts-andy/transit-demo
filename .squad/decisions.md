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

## Governance

- All meaningful changes require team consensus
- Document architectural decisions here
- Keep history focused on work, decisions focused on direction
