# F1Viz Handoff Overview

## Repository

Current working path:

```bash
/Users/ryansmith/dev/GitHub/f1viz
```

Run all project commands from that root.

Note: the Codex sandbox for the current thread may still have older workspace roots configured. If write commands ask for approval, the durable fix is to open/add `/Users/ryansmith/dev/GitHub/f1viz` as the workspace root.

## Product Direction

F1Viz is a personal Formula 1 race replay and visual storytelling tool.

Primary mode:

- time-based race replay companion
- useful while watching or rewatching a Grand Prix
- explains race events conservatively from data

Secondary mode:

- analyst dashboard later
- charts and deeper inspection built on the same analysis services

The first build surface is a CLI. The CLI should produce Markdown and JSON from shared report models so the future dashboard can reuse the same analysis outputs.

## Current Capabilities

The app can:

- list OpenF1 fixture endpoints
- record OpenF1 fixture sets from the network
- load saved fixture sets offline
- resolve meeting/session data
- normalize raw OpenF1-shaped records into a `RaceSession`
- build simple race facts
- build fixture-backed race reports
- compare any two drivers using lap facts
- render Markdown and JSON reports

Fixture-backed commands:

```bash
.venv/bin/f1viz fixtures endpoints
.venv/bin/f1viz fixtures summary --name sample-race
.venv/bin/f1viz race analyze --year 2025 --gp sample --fixture-name sample-race
.venv/bin/f1viz race compare --year 2025 --gp sample --fixture-name sample-race --first-driver NOR --second-driver PIA
```

## Verification

Last verified:

```bash
make test
# 22 passed

make lint
# All checks passed
```

## Important Repo Hygiene

Generated artifacts are currently tracked in git:

- `__pycache__/`
- `reports/2025-monaco-race-analysis.*`

`.gitignore` has been added, but already-tracked generated files still show as modified after tests/demo commands. Clean this up before committing the feature work.

Recommended cleanup:

```bash
git rm --cached -r src/f1viz/**/__pycache__ tests/__pycache__ reports
```

Then verify:

```bash
make test
make lint
```

