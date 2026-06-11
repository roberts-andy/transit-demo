---
name: "demo-readiness-and-fallback"
description: "Prepare the Fabric transit demo for reliable customer-facing delivery by validating the end-to-end flow, confirming fallback paths, checking artifact readiness, and aligning the implementation to a clear demo narrative. Use before dry runs, rehearsals, or live customer sessions."
domain: "demo-operations"
confidence: "high"
source: "manual"
tools:
  - name: "Fabric"
    description: "Validate demo artifacts and data flow readiness"
    when: "When checking Lakehouse, Warehouse, Eventstream, Pipeline, Notebook, Dataflow Gen2, and Eventhouse assets"
  - name: "Git"
    description: "Verify repo state and reproducibility"
    when: "When ensuring the repo reflects the current demo implementation and fallback assets"
  - name: "Runbook"
    description: "Operational execution guidance"
    when: "When confirming step-by-step demo flow, recovery options, and operator responsibilities"
---

## Context

This skill applies whenever the transit demo is approaching customer-facing use, including:
- internal dry runs
- facilitator rehearsals
- executive previews
- customer briefings
- event-based showcases

This demo depends on public data sources and multiple Fabric workloads, so readiness is not only about whether the implementation exists. It is also about whether the implementation is:
- understandable
- repeatable
- resilient during live delivery
- aligned to the intended customer story

This skill should be used before any formal demo delivery and again when significant implementation changes occur.

## Patterns

### 1. Validate the narrative, not just the artifacts
A technically complete repo is not automatically demo-ready.

For each required demo capability, confirm:
- what story it tells
- where it appears in the flow
- which artifact demonstrates it
- what value the audience should take away

The demo should make it obvious why each Fabric workload exists.

### 2. Confirm the required end-to-end path
At minimum, validate that the demo can show:
- one or more ingestion paths
- Bronze raw landing
- Silver normalization
- Gold KPI serving
- at least one reportable or explainable KPI outcome

If one of the optional enrichments is unavailable, the core path should still work.

### 3. Always define fallback for live dependencies
This demo uses public APIs and potentially real-time feeds.

For every live dependency, define:
- whether it is required for the session
- whether cached or replayable data exists
- what the operator should do if the live dependency fails
- how to explain the fallback without undermining the story

Fallback should be treated as part of the design, not a last-minute rescue.

### 4. Validate artifact freshness and consistency
Before demo delivery, confirm:
- artifact names still match the intended story
- Warehouse outputs still align to the expected KPIs
- sample data reflects the current schema assumptions
- the repo and the workspace are not materially out of sync

### 5. Check operator readiness
A demo is only as strong as its execution.

The runbook should make clear:
- the recommended order of presentation
- what to show first
- what can be skipped if time is short
- what to do if a component fails
- which outputs are screenshots, cached data, or live data

### 6. Prefer clear, inspectable outputs
When under time pressure, default to showing outputs that are:
- stable
- visually interpretable
- directly tied to the architecture story
- easy to explain in one or two sentences

### 7. Capture “minimum viable demo” and “full demo” separately
Define:
- the minimum viable demo path required to prove the concept
- the expanded path that adds more sophistication or enrichments

This prevents the team from failing the entire demo when only an optional feature breaks.

## Required Inputs

Before applying this skill, gather:
- the current backlog and implementation status
- the required Fabric capabilities to demonstrate
- the current runbook or intended talk track
- known live dependencies
- available fallback datasets or replay assets
- target audience and session length if known

## Expected Outputs

A good run of this skill produces:
- demo readiness summary
- critical path validation
- list of must-show vs optional artifacts
- fallback plan per live dependency
- operator checklist
- updated runbook notes or rehearsal guidance
- visible risks and open issues

## Demo Acceptance Criteria

A demo is ready if:
- every required Fabric workload has a clear demonstration point
- there is a valid end-to-end Bronze → Silver → Gold story
- at least one KPI can be explained credibly
- live-source failures do not collapse the entire session
- the operator knows what to do if data, orchestration, or streaming is unavailable
- the narrative remains understandable to a customer audience

## Examples

### Example prompt
"DemoOps, validate whether the current implementation is ready for a 30-minute customer-facing Fabric demo."

### Example expected result
- MVP demo path identified
- optional enrichments marked as optional
- Eventstream fallback documented
- cached Bronze data confirmed
- Gold KPI path validated
- runbook updated with failure branches

## Anti-Patterns

- Assuming live APIs will work during a customer demo without a fallback
- Treating optional enrichments as critical-path dependencies
- Letting the architecture become too complex to explain clearly
- Showing half-working artifacts because they exist in the repo
- Leaving the operator to decide the story live with no runbook or recovery plan
- Confusing “workspace has assets” with “demo is reliable”

## Review Checklist

Before declaring demo readiness, confirm:
- the core narrative is clear
- all required demo workloads map to concrete artifacts
- fallback data or replay options exist where needed
- the minimum viable demo path is documented
- the runbook includes operator decision points
- current implementation status matches what the presenter intends to say