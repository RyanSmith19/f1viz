# F1Viz Next Steps

## Immediate Cleanup

Clean tracked generated files before committing.

Current issue:

- generated Python bytecode is tracked
- generated reports are tracked
- `.gitignore` now ignores them, but git still tracks existing entries

Recommended command:

```bash
git rm --cached -r src/f1viz/**/__pycache__ tests/__pycache__ reports
```

Then:

```bash
make test
make lint
git status --short
```

## Next Implementation Stage

Continue Stage 4: comparative metrics.

Current comparison:

- any two drivers
- lap count
- best lap
- average lap
- best-lap delta
- average-lap delta

Next comparison additions:

- teammate context
- field median baseline
- session leader baseline
- own-best lap or stint baseline
- clear evidence entries for every baseline

Recommended sequence:

1. Add a `LapBaselineFacts` model.
2. Add a `LapBaselineService`.
3. Keep baselines factual, not explanatory.
4. Extend `DriverComparisonFacts` with optional baseline fields.
5. Extend report output after tests pass.

## Then Stage 5

Stage 5 is conservative explanatory replay.

Do not jump to strategy scoring first. Start with safe explanations:

- "Driver A had the better best lap in this fixture."
- "Driver B's average lap was slower across included laps."
- "This comparison uses selected-driver baseline only."

Then add:

- confidence levels
- missing-data warnings
- plain-English caveats

## Real OpenF1 Fixture Decision

The project still needs one real race fixture set.

Before committing a full real fixture:

1. Run fixture record against a known race.
2. Check fixture size.
3. Decide whether fixtures should be:
   - full and committed
   - trimmed and committed
   - stored outside git

Recording command:

```bash
.venv/bin/f1viz fixtures record --year 2025 --gp monaco --session-name Race
```

## CLI Commands To Preserve

These should keep working:

```bash
make test
make lint
.venv/bin/f1viz fixtures endpoints
.venv/bin/f1viz fixtures summary --name sample-race
.venv/bin/f1viz race analyze --year 2025 --gp sample --fixture-name sample-race
.venv/bin/f1viz race compare --year 2025 --gp sample --fixture-name sample-race --first-driver NOR --second-driver PIA
```

## Caution

Avoid adding dashboard code yet. The data model and comparison services are still maturing. The dashboard should consume stable report JSON later, not force premature UI-specific structures into the core.

