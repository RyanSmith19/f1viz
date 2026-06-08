# F1Viz Project Skill

Use this guidance when developing F1Viz features.

## Product North Star

F1Viz is a race replay and storytelling tool that teaches Formula 1 through data.

The user should come away understanding:

- why a driver or team performed well or poorly
- whether strategy helped or hurt
- where pace changed during the race
- which race moments mattered
- how qualifying context affected the Grand Prix

## Development Rules

Prefer reusable analysis code over one-off UI logic.

Keep these layers separate:

- data fetching
- local cache/repositories
- domain models
- analysis services
- explanation services
- CLI/API controllers
- views/report rendering

Do not put race interpretation logic directly in CLI commands or dashboard components.

## Explanation Rules

Explanations must be conservative and evidence-backed.

Use language such as:

- "the data suggests"
- "appears"
- "relative to field median"
- "compared with teammate"
- "estimated impact"

Avoid language such as:

- "definitely"
- "driver mistake"
- "bad strategy"
- "optimal path"

unless the report includes clear evidence and confidence.

## Testing Rules

Write tests before or alongside analysis functions.

At minimum, add tests for:

- every calculation that affects a score
- every event-detection rule
- every explanation branch
- every CLI report contract

Prefer fixtures for OpenF1 data. Network-dependent tests should be opt-in and not part of the default test suite.

## Output Contracts

Every major CLI command should eventually support:

- human-readable Markdown
- machine-readable JSON

The JSON shape is the future dashboard contract.

## Naming Rules

Use conservative metric names.

Preferred:

- `strategy_impact_estimate`
- `pace_delta_to_field_median`
- `pace_delta_to_teammate`
- `execution_efficiency_proxy`
- `reference_lap_match`

Avoid:

- `driver_error`
- `bad_strategy`
- `optimal_line`
- `perfect_lap`

## First Feature Bias

When choosing between broad coverage and trustworthy analysis, choose trustworthy analysis.

The first useful product is not a giant dashboard. It is a reliable report that explains a race or driver comparison clearly enough to help while rewatching a Grand Prix.

