# Roadmap Status

## Completed

### Foundation

- Python package scaffold
- Typer CLI entrypoint
- Markdown and JSON report contract
- Project-local virtual environment setup through `make setup`
- Root-path commands documented in `docs/development.md`
- Unit tests for report serialization and rendering

### CLI Phase 1 Start

- OpenF1 endpoint enum
- OpenF1 HTTP client wrapper
- Endpoint methods for core race-analysis data sources
- Fixture repository for deterministic tests and demos
- Session resolver for matching a race weekend and session from OpenF1-shaped records
- No-network tests for client URL behavior, fixture persistence, and session resolution
- Raw session data container for OpenF1-shaped endpoint records
- Session data loader for meetings, sessions, and core race endpoints
- Session fixture writer for saving resolved session fixtures
- Session fixture reader for reconstructing raw session data offline
- CLI fixture endpoint listing and recording commands
- CLI fixture summary command
- Fixture contract document
- Small checked-in synthetic `sample-race` fixture set

### CLI Phase 2 Start

- Normalized race session aggregate model
- Driver metadata mapping
- Lap and stint normalized collections with driver helper methods
- Timestamped replay timeline records
- Common elapsed-time axis derived from session start or earliest dated record
- Model stage definitions from raw source data to complete replay model
- Race session readiness assessment
- Fixture-backed race report builder
- `race analyze` can produce a report from saved fixture data
- First driver comparison fact service for any two drivers
- Stage 3 race facts abstraction for factual non-interpretive summaries
- Stage 4 driver comparison report builder
- `race compare` CLI command for fixture-backed driver lap comparisons

## Next

### CLI Phase 1 Completion

- Add one real race fixture set.
- Decide whether real race fixtures should be full, trimmed, or stored outside git.

### CLI Phase 2

- Add race fact report sections for per-driver lap/stint coverage.
- Add teammate, field median, session leader, and own-best baselines to driver comparisons.
