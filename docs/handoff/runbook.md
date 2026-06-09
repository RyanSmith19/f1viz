# F1Viz Runbook

## Root Path

```bash
cd /Users/ryansmith/dev/GitHub/f1viz
```

## Environment Setup

```bash
make setup
```

This creates `.venv` and installs the package in editable mode with development dependencies.

## Test And Lint

```bash
make test
make lint
```

## Generate Demo Report

```bash
make demo
```

This writes scaffold reports under `reports/`.

## Fixture Commands

List expected OpenF1 endpoints:

```bash
.venv/bin/f1viz fixtures endpoints
```

Summarize checked-in sample fixture:

```bash
.venv/bin/f1viz fixtures summary --name sample-race
```

Record a real fixture set:

```bash
.venv/bin/f1viz fixtures record --year 2025 --gp monaco --session-name Race
```

Recording uses the network.

## Race Reports

Fixture-backed race report:

```bash
.venv/bin/f1viz race analyze --year 2025 --gp sample --fixture-name sample-race
```

Driver comparison report:

```bash
.venv/bin/f1viz race compare --year 2025 --gp sample --fixture-name sample-race --first-driver NOR --second-driver PIA
```

Reports write Markdown and JSON under `reports/` unless `--output-dir` is passed.

## Known Environment Issue

If Codex asks for write approval under this path, it is because the active thread sandbox still lists older workspace roots. The repo path itself is correct. The durable fix is to open/add `/Users/ryansmith/dev/GitHub/f1viz` as the workspace root for future work.

