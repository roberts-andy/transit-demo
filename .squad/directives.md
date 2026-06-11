# Persistent Team Directives

Always keep Bronze data as close to source fidelity as practical.
Always normalize Silver timestamps to UTC and retain source-local time when useful for analysis.
Always separate concerns: ingestion, normalization, and KPI serving must be independently explainable.
Always prefer reusable parameterization over hardcoded workspace, lakehouse, warehouse, or environment identifiers.
Always annotate every dataset with source system, extraction time, and grain.
Always design demo outputs to be scannable and executive-friendly as well as technically credible.
Never commit secrets, API keys, tokens, or connection strings to the repository.
Never couple the demo to only one city-specific schema if a conformed model is possible.
Never make Gold depend directly on raw Bronze payloads.
Never accept a live-demo-only dependency without a cached/fallback path.
When choosing between low-code and code-first, optimize first for clarity of the story and second for engineering elegance.
When a transformation can be expressed cleanly in SQL and benefits from automatic refresh/dependency handling, prefer a Materialized Lake View.
When a transformation requires custom parsing, procedural logic, or domain-heavy shaping, prefer a Notebook.
When the goal is to show approachable business-user-friendly shaping, prefer Dataflow Gen2.
When environment-specific settings are needed, use parameters / variable substitution patterns rather than per-environment copy-paste.
