# OpenF1 Fixture Contract

Fixture sets live under `tests/fixtures/openf1/` and are grouped by endpoint.

Each complete race fixture set uses the same fixture name across endpoint folders:

```text
tests/fixtures/openf1/
  meetings/{fixture-name}.json
  sessions/{fixture-name}.json
  drivers/{fixture-name}.json
  laps/{fixture-name}.json
  position/{fixture-name}.json
  intervals/{fixture-name}.json
  pit/{fixture-name}.json
  stints/{fixture-name}.json
  race_control/{fixture-name}.json
  overtakes/{fixture-name}.json
```

For example:

```bash
.venv/bin/f1viz fixtures summary --name sample-race
```

## Required Shape

- `meetings/{name}.json` must contain exactly one meeting record.
- `sessions/{name}.json` must contain exactly one session record.
- Core race endpoint files must contain JSON lists, even when empty.

## Purpose

Fixtures support deterministic offline tests and development. They should preserve raw OpenF1-shaped records. Normalized race-session models are built from these raw records in later architecture layers.

## Real Fixture Policy

Small synthetic fixtures are useful for tests and CLI smoke checks.

Real race fixtures should be recorded intentionally with:

```bash
.venv/bin/f1viz fixtures record --year 2025 --gp monaco --session-name Race
```

Real fixtures may be large. Before committing them, verify size and decide whether the repo should keep full fixtures, trimmed fixtures, or external fixture artifacts.

