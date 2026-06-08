# F1Viz

F1Viz is a personal Formula 1 race replay and storytelling analytics tool.

The first version is a CLI that produces Markdown and JSON reports. The CLI is the first view over reusable analysis services that will later power a local dashboard.

## Current Focus

- Load race-weekend data from OpenF1.
- Build time-based race replay reports.
- Compare any two drivers with teammate, field median, session leader, and own-best baselines.
- Keep explanations conservative and evidence-backed.

## Development

```bash
python -m pip install -e ".[dev]"
pytest
f1viz --help
```

