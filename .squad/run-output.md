# Run Output — {task title}

> Final assembled artifact from a multi-agent run.

## Termination Condition

**Reason:** {One of: User accepted | Reviewer approved | Constraint budget exhausted | Deadlock — escalated to user | User cancelled}

## Constraint Budgets

<!-- Track all active constraints inline. Remove this section if no constraints are active. -->

| Constraint | Used | Max | Status |
|------------|------|-----|--------|
| Clarifying questions | 📊 {n} | {max} | {Active / Exhausted} |
| Revision cycles | 📊 {n} | {max} | {Active / Exhausted} |

## Result

{Assembled final artifact goes here. This is the Coordinator's synthesis of agent outputs.}

---

## Reviewer Verdict

<!-- Include one block per review. Remove this section if no review occurred. -->

### Review by {Name} ({Role})

| Field | Value |
|-------|-------|
| **Verdict** | {Approved / Rejected} |
| **What's wrong** | {Specific issue — not vague} |
| **Why it matters** | {Impact if not fixed} |
| **Who fixes it** | {Name of agent assigned to revise — MUST NOT be the original author} |
| **Revision budget** | 📊 {used} / {max} revision cycles remaining |

---

## APPENDIX: RAW AGENT OUTPUTS

<!-- Paste each agent's verbatim response below. Do NOT edit, summarize, rewrite, or wrap in code fences. One section per agent. -->

### {Name} ({Role}) — Raw Output

{Paste agent's verbatim response here, unedited}

### {Name} ({Role}) — Raw Output

{Paste agent's verbatim response here, unedited}

### 2026-06-11 14:04:39 EX-1 Preflight Check
- Preflight started.
- Fabric items discoverable: Yes (8 items found).

### 2026-06-11 14:04:46 EX-1 Preflight Check
- Preflight started.
- Fabric items discoverable: Yes (8 items found).

## EX-2 Kickoff/Progress Note - 2026-06-11 14:05:21
- **Readiness**: Notebooks (ronze_mbta_*, ronze_wmata_*) integrated with 
esolve_secret and mssparkutils.credentials.getSecret. Secret names standardized in configs.
- **Blockers**: AZURE_KEY_VAULT_URI is empty in infra/parameters.dev.yml and .env.template. Requires URI for live integration validation.


## EX-2 Kickoff/Progress Note - 2026-06-11 14:05:33
- **Readiness**: Notebooks integrated with resolve_secret and mssparkutils. Secret names standardized.
- **Blockers**: AZURE_KEY_VAULT_URI is empty/placeholder in parameters.dev.yml and .env.template.

## EX-1 Live Preflight Evidence - 2026-06-11 14:11:00
- Notebook count: 8 Bronze notebooks found in src/ingestion/notebooks.
- MBTA /routes smoke check: HTTP 200, count=178.
- WMATA TrainPositions smoke check: HTTP 200, count=106.
- Status: PASS (connectivity and key load validated).
- Open gate: Fabric runtime write validation still required for EX-1 completion.

