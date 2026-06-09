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
cd /Users/ryansmith/dev/GitHub/f1viz
make setup
make test
.venv/bin/f1viz --help
```

See [docs/development.md](docs/development.md) for root-path commands.
