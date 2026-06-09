# F1Viz Architecture Handoff

## Design Principle

Keep each layer small and specific. Do not put strategy judgement, explanatory prose, or chart concerns into data-loading or normalization code.

Current flow:

```text
OpenF1 API / fixtures
  -> RawSessionData
  -> RaceSession
  -> RaceFacts / DriverComparisonFacts
  -> RaceReport
  -> Markdown + JSON
```

## Model Stages

The model stage plan is documented in:

- `docs/architecture/model-stages.md`

Current implemented stages:

- Stage 0: raw source data
- Stage 1: resolved session
- Stage 2: normalized race session
- Stage 3: race facts
- Stage 4: initial comparative metrics

Later stages:

- richer comparative baselines
- conservative explanatory replay
- complete replay model

## Key Models

### RawSessionData

File:

- `src/f1viz/models/session_data.py`

Purpose:

- preserves OpenF1-shaped endpoint rows
- keeps fixture/cache data close to source shape
- should not contain interpretation

### RaceSession

File:

- `src/f1viz/models/race_session.py`

Purpose:

- normalized session aggregate
- driver identity map
- lap and stint collections
- timestamped replay timeline on common elapsed-time axis

Helpful methods:

- `driver_by_acronym`
- `laps_for_driver`
- `stints_for_driver`
- `timeline_for_driver`

### RaceFacts

File:

- `src/f1viz/models/race_facts.py`

Purpose:

- factual, non-interpretive summaries
- counts by driver and timeline category
- input to reports and later analysis

### DriverComparisonFacts

File:

- `src/f1viz/models/comparison.py`

Purpose:

- first comparison fact object
- currently best/average lap comparisons for any two drivers
- later should add teammate, field median, session leader, and own-best baselines

## Key Services

### OpenF1Client

File:

- `src/f1viz/openf1/client.py`

Purpose:

- endpoint URL construction
- HTTP request/response handling
- no analysis logic

### SessionDataLoader

File:

- `src/f1viz/services/session_data_loader.py`

Purpose:

- resolves race session from OpenF1 meetings/sessions
- loads core race endpoints
- produces `RawSessionData`

### Fixture Reader/Writer

Files:

- `src/f1viz/services/session_fixture_reader.py`
- `src/f1viz/services/session_fixture_writer.py`
- `src/f1viz/repositories/fixture_repository.py`

Purpose:

- deterministic offline data path
- default tests should use fixtures/mocks, not network

### RaceSessionBuilder

File:

- `src/f1viz/services/race_session_builder.py`

Purpose:

- converts `RawSessionData` into `RaceSession`
- parses timestamps
- builds driver/lap/stint/timeline structures

### RaceFactsBuilder

File:

- `src/f1viz/services/race_facts_builder.py`

Purpose:

- Stage 3 factual summaries
- should remain non-interpretive

### DriverComparisonService

File:

- `src/f1viz/services/driver_comparison.py`

Purpose:

- Stage 4 comparison facts
- currently compares selected drivers by lap facts only

### Report Builders

Files:

- `src/f1viz/services/race_report_builder.py`
- `src/f1viz/services/driver_comparison_report_builder.py`

Purpose:

- convert facts into shared `RaceReport` contract
- keep wording conservative and evidence-backed

## Test Strategy

Default tests must not require network.

Current test coverage includes:

- OpenF1 client URL/shape behavior
- fixture repository round trips
- session resolver
- fixture reader/writer
- race session builder
- model readiness
- race facts builder
- race report builder
- driver comparison service
- driver comparison report builder
- Markdown rendering

Run:

```bash
make test
make lint
```

