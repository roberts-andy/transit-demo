# Azure Infra Lead History

## Project Context
- Project: transit-demo
- Owner: roberts-andy
- Focus: Azure infrastructure for Key Vault-backed Fabric secret resolution

## Learnings
- 2026-06-11: Added to squad with EX-5 ownership.
- 2026-06-11: Azure CLI context confirmed on subscription f70cfb6a-3eda-4cd9-856c-eaf4f040a66e and tenant da78621e-f352-46cd-b186-fad7b71bb6cf.
- 2026-06-11: **Charter hardened:** Operational context now locked to specific subscription/resource group. All resource operations MUST include verification step. Script output success ≠ resource creation—verified with `az group exists` and `az keyvault show`. Verification protocol mandatory for all future tasks.
- 2026-06-11: **Key lesson:** First provisioning run appeared successful in output but resources were not actually created. Root cause was likely permission/context issue. Verification CLI queries catch this; Portal visibility is unreliable for immediate confirmation.
