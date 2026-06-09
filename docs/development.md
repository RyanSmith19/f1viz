# Development

Run commands from the project root:

```bash
cd /Users/ryansmith/dev/GitHub/f1viz
```

## Setup

```bash
make setup
```

This creates `.venv` and installs the project in editable mode with development dependencies.

## Test

```bash
make test
```

Default tests should not require network access. OpenF1 API behavior should be tested with recorded fixtures or mocked HTTP responses.

## Lint

```bash
make lint
```

## Demo Report

```bash
make demo
```

This writes scaffold reports under `reports/`.

## Record OpenF1 Fixtures

Fixture recording uses the network and is intentionally outside the default test path:

```bash
.venv/bin/f1viz fixtures endpoints
.venv/bin/f1viz fixtures record --year 2025 --gp monaco --session-name Race
.venv/bin/f1viz fixtures summary --name 2025-monaco-race
```

Recorded fixtures are written under `tests/fixtures/openf1/` by default.

## Direct Commands

The CLI can also be run directly from the root path:

```bash
.venv/bin/f1viz --help
.venv/bin/f1viz race analyze --year 2025 --gp monaco --output-dir reports
.venv/bin/f1viz race analyze --year 2025 --gp sample --fixture-name sample-race
.venv/bin/f1viz race compare --year 2025 --gp sample --fixture-name sample-race --first-driver NOR --second-driver PIA
.venv/bin/f1viz fixtures endpoints
```

## Development Principles

- Keep OpenF1 fetching separate from analysis.
- Keep repositories separate from explanations.
- Keep CLI commands thin.
- Add fixture-backed tests before adding analysis rules.
- Make Markdown and JSON outputs from the same structured report object.
