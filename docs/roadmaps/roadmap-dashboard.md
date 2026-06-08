# Dashboard Roadmap

## Goal

Build a local dashboard that consumes the same analysis outputs as the CLI and presents a time-based race replay experience with optional analyst views.

## Phase 0: API Contract

Deliverables:

- JSON schema or typed response contracts from CLI analysis services
- stable report IDs
- fixture-backed API examples

Acceptance criteria:

- dashboard can be developed without live OpenF1 calls
- CLI JSON output can drive the first UI prototype

## Phase 1: Backend API

Stack:

- FastAPI
- shared `f1viz` analysis package
- DuckDB/cache access

Deliverables:

- race weekend list endpoint
- session load endpoint
- whole race report endpoint
- driver comparison endpoint
- replay timeline endpoint

Acceptance criteria:

- API returns same analysis structures as CLI JSON
- route tests use fixtures

## Phase 2: Race Weekend Entry

Deliverables:

- race weekend selector
- session selector
- cached data status
- default "analyze race" path

Acceptance criteria:

- app opens into the actual tool, not a marketing page
- user can start from a race weekend

## Phase 3: Replay Timeline

Deliverables:

- time-based replay timeline
- major event markers
- continuous state panel
- filters for driver, team, and battle
- event detail drawer/panel

Acceptance criteria:

- replay view can be used while watching a race
- timeline supports jumping to important moments
- event details show evidence and related charts

## Phase 4: Video Sync Controls

Deliverables:

- manual race-video offset
- session start / lights out calibration options
- elapsed race time display
- bookmark export

Acceptance criteria:

- user can align the dashboard timeline to a replay video manually
- sync state persists locally

## Phase 5: Driver Comparison View

Deliverables:

- any two-driver comparison
- lap pace chart
- stint chart
- baseline selectors
- evidence-backed summary panel

Baselines:

- teammate
- field median
- session leader
- own best comparable stint

Acceptance criteria:

- chart and prose tell the same story
- unsupported explanations are not displayed

## Phase 6: Strategy View

Deliverables:

- pit stop timeline
- tire age visualization
- undercut/overcut markers
- traffic rejoin context
- strategy impact estimate

Acceptance criteria:

- strategy scoring is secondary to evidence
- confidence and uncertainty are visible

## Phase 7: Qualifying Context View

Deliverables:

- qualifying story summary
- teammate gaps
- sector ranking
- abnormal event flags
- race implication notes

Acceptance criteria:

- race replay can link back to qualifying context

## Phase 8: Analyst Dashboard

Deliverables:

- team performance summary
- pace distribution
- sector/team strengths
- speed trap comparison
- tire degradation comparison
- telemetry overlays where data supports them

Acceptance criteria:

- analyst mode is optional and reachable from replay stories
- charts avoid overwhelming the primary storytelling flow

## Phase 9: Execution Efficiency Proxies

Deliverables:

- ideal sector lap view
- reference lap match chart
- speed trace comparison
- optional corner cluster view

Acceptance criteria:

- all proxy metrics are labeled clearly
- no claim of true optimal racing line

