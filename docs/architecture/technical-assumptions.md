# Technical Assumptions

## Data Source

F1Viz uses OpenF1 as the primary data source.

Relevant OpenF1 endpoints include:

- meetings
- sessions
- drivers
- laps
- car data
- location
- intervals
- overtakes
- pit
- position
- race control
- session result
- starting grid
- stints
- team radio
- weather
- championship drivers
- championship teams

Historical data from 2023 onward is expected to be available without authentication. Live data may require a paid plan and is not a first-version requirement.

## Stack

The core stack should be Python-first:

- Python 3.12+
- Typer for CLI commands
- Pydantic for typed data models
- Polars for tabular/time-series transformations
- DuckDB for local analytical storage
- pytest for tests
- httpx for HTTP client behavior
- respx or recorded fixtures for API-facing tests

Later dashboard stack:

- FastAPI backend
- React + Vite + TypeScript frontend
- ECharts or Plotly for charts
- Playwright for browser tests

## Architecture

Use a layered MVC-inspired architecture:

```text
OpenF1 API
  -> Data Client
  -> Repository / Cache
  -> Domain Models
  -> Analysis Services
  -> Explanation Services
  -> Controllers
  -> Views
```

The CLI and future dashboard should call the same analysis services. UI code should not duplicate analytics logic.

## Layer Responsibilities

### OpenF1 Client

Responsible for:

- endpoint requests
- query parameter handling
- retry/timeouts
- response decoding
- basic API errors

Not responsible for:

- strategy analysis
- lap filtering rules
- race interpretation

### Repository / Cache

Responsible for:

- storing fetched OpenF1 data locally
- loading cached session data
- exposing stable typed collections or frames
- separating raw source data from derived reports

Early implementation can use filesystem JSON fixtures plus DuckDB. The cache should be replaceable without touching analysis services.

### Domain Models

Responsible for:

- typed representation of F1 concepts
- validation of required fields
- consistent naming and time handling

The models should preserve source timestamps because replay mode is time-based.

### Analysis Services

Responsible for:

- driver comparison
- team performance summaries
- qualifying context summaries
- stint and tire degradation analysis
- strategy impact estimates
- race replay timeline construction
- event detection

Services should return structured data that can be serialized to JSON.

### Explanation Services

Responsible for:

- conservative plain-English summaries
- evidence lists
- confidence labels
- score labels where supported

Explanations should be generated from structured analysis outputs, not directly from raw source rows.

### Controllers

Initial controllers are Typer CLI commands.

Later controllers are FastAPI routes.

### Views

Initial views are Markdown and terminal summaries.

Later views are dashboard pages and chart components.

## Test Strategy

Use TDD where calculations and interpretation rules matter.

Unit tests should cover:

- lap filtering
- pit lap exclusion
- teammate baselines
- field median baselines
- session leader baselines
- stint grouping
- degradation slope
- undercut/overcut detection
- overtaking classification
- qualifying anomaly detection
- replay timeline ordering
- conservative explanation wording

Integration tests should cover:

- loading recorded OpenF1 fixtures
- running CLI commands against fixtures
- writing Markdown and JSON reports
- cache read/write behavior

Dashboard tests later should cover:

- API route responses
- race weekend selection
- replay timeline rendering
- chart smoke tests
- video sync offset behavior

## Data Quality Principles

Every derived metric should include:

- source inputs used
- filtering rules
- comparison baseline
- confidence level when relevant

If a metric is a proxy, the name and explanation should make that clear.

