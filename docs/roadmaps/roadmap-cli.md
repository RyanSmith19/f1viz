# CLI Roadmap

## Goal

Build a tested command-line analysis engine that can load an F1 race weekend, analyze a race, compare any two drivers, and produce Markdown plus JSON reports.

## Phase 0: Project Foundation

Deliverables:

- Python project scaffold
- package layout under `src/f1viz`
- pytest setup
- lint/type-check commands
- basic CLI entrypoint
- fixture directory
- report output directory

Acceptance criteria:

- `f1viz --help` works
- tests run locally
- project can be installed in editable mode

## Phase 1: OpenF1 Client and Fixtures

Deliverables:

- typed OpenF1 HTTP client
- endpoint wrappers for meetings, sessions, drivers, laps, position, intervals, pit, stints, race control, overtakes
- fixture recording/loading strategy
- no-network integration test mode

Acceptance criteria:

- can resolve a race weekend and race session
- can load fixture data for one known race
- default tests do not require network

## Phase 2: Race Session Model

Deliverables:

- normalized race session aggregate
- driver metadata mapping
- team mapping
- timestamp normalization
- lap and elapsed race time helpers

Acceptance criteria:

- all race events can be sorted on a common time axis
- reports can reference driver acronyms, full names, and teams consistently

## Phase 3: Whole Race Report

Command:

```bash
f1viz race analyze --year 2025 --gp monaco
```

Deliverables:

- major event timeline
- race control summary
- pit stop summary
- overtake summary
- position swing summary
- Markdown report
- JSON report

Acceptance criteria:

- report flags major race moments
- JSON report has a stable schema
- all generated claims trace back to evidence entries

## Phase 4: Driver Comparison

Command:

```bash
f1viz race compare --year 2025 --gp monaco --drivers NOR PIA
```

Deliverables:

- any two-driver comparison
- lap pace comparison
- stint comparison
- tire age context
- pit context
- overtakes and traffic context
- baselines for teammate, field median, session leader, own best comparable stint

Acceptance criteria:

- comparison explains where one driver gained or lost time
- report avoids unsupported conclusions
- report includes conservative confidence levels

## Phase 5: Strategy Analysis

Deliverables:

- pit timing evaluation
- undercut/overcut detection
- traffic rejoin detection
- tire degradation estimate
- strategy impact estimate

Acceptance criteria:

- strategy labels start conservative
- score or time impact appears only when baseline data supports it
- uncertainty is visible in the output

## Phase 6: Time-Based Replay CLI

Commands:

```bash
f1viz race replay --year 2025 --gp monaco
f1viz race replay --year 2025 --gp monaco --from 00:25:00 --to 00:40:00
f1viz race replay --year 2025 --gp monaco --focus NOR
```

Deliverables:

- elapsed-time timeline
- major event markers
- continuous state snapshots
- focus driver/team/battle filters

Acceptance criteria:

- useful as a race rewatch companion
- can show what to watch at a given elapsed time
- can produce Markdown and JSON excerpts

## Phase 7: Qualifying Context

Command:

```bash
f1viz quali summarize --year 2025 --gp monaco
```

Deliverables:

- qualifying order summary
- teammate gaps
- sector weaknesses
- abnormal events
- likely race implications

Acceptance criteria:

- qualifying report highlights race-relevant context
- explanations remain conservative

## Phase 8: Optional Execution Efficiency Proxies

Deliverables:

- ideal sector lap
- reference lap match
- speed trace efficiency
- corner performance proxy if location quality is sufficient

Acceptance criteria:

- metric names clearly indicate proxy status
- no UI/report claims true optimal path

