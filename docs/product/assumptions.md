# F1Viz Product Assumptions

## User Intent

F1Viz is a personal Formula 1 learning and replay companion. The primary user is a casual F1 viewer who wants to understand race performance, strategy, and driver/team differences while watching or rewatching a Grand Prix.

The product should explain what happened and why the data supports that interpretation. It should avoid overclaiming when the data only supports a proxy or correlation.

## Primary Mode

The primary mode is a time-based race replay and visual storytelling experience.

The user starts from a race weekend, then reviews:

- qualifying context that may influence the race
- race event timeline
- driver and team performance changes over time
- major overtakes
- pit stops and strategy consequences
- pace shifts by stint, tire age, traffic, and race control events

The app should eventually support syncing the replay timeline with an external race video.

## Secondary Mode

The secondary mode is an analyst dashboard for deeper inspection.

Dashboard views should be reachable from replay events rather than existing only as disconnected charts. A replay moment should be able to lead to lap, stint, telemetry, strategy, or comparison views.

## First Build Surface

The first build surface is a CLI that produces:

- Markdown reports for human reading
- JSON reports for future dashboard/API consumption

The CLI is not a throwaway prototype. It is the first controller/view over reusable domain, repository, analysis, and explanation layers.

## Default Analysis

The default analysis should process a whole race weekend or whole race session.

The user can later narrow analysis by:

- driver
- team
- battle
- elapsed race time range
- lap range
- stint
- repeated corner/track segment attempts, when data quality allows

## Driver Comparison

The first comparison capability should support any two drivers.

Each comparison should include baseline context where available:

- teammate
- field median
- session leader
- driver's own best lap or best comparable stint

The tool should avoid comparing drivers in isolation because different traffic, tire, strategy, and car contexts can mislead.

## Explanation Style

Explanations should be conservative first, scored second.

The app should state evidence before interpretation. Strong labels such as "bad strategy" should only appear when supported by measurable losses versus relevant baselines.

Preferred language:

- "appears costly"
- "likely helped"
- "the data suggests"
- "relative to comparable cars"
- "estimated impact"

Avoid unsupported claims:

- "driver error" without race control, telemetry, or lap evidence
- "bad car" without teammate/team/session context
- "optimal racing line" when only proxy data is available

## Strategy Interpretation

Strategy analysis should compare pit timing, tire age, traffic, race control events, and pace deltas.

The first strategy score should be evidence-based and approximate:

- positive, neutral, or negative direction
- estimated time impact range where feasible
- confidence level based on available data

## Replay Timeline

The replay should support two levels of detail:

- major event flags: overtakes, pit stops, safety car/VSC/yellows, abnormal pace, large position swings, undercut/overcut moments
- continuous indicators: position, gap, tire age, stint, pace versus baselines, traffic pressure, pit window state

The timeline should be time-based, not only lap-based.

## Video Sync

The product should eventually support manual calibration against a race video.

Supported sync options should include:

- official session start
- lights out/race start
- manual offset

No single default is assumed yet. The first CLI can expose elapsed race time and leave video sync calibration for the dashboard.

## Optimal Path / Execution Efficiency

True optimal racing line analysis is out of scope for early versions.

OpenF1 exposes useful proxy data, including car telemetry and location data. However, the location data does not provide enough detail to claim a true optimal path or full racing line quality.

Later features should use conservative names:

- execution efficiency
- reference lap match
- speed trace efficiency
- best available lap delta
- ideal sector lap
- corner performance proxy

The UI should not imply that the app can compute the mathematically optimal racing line.

