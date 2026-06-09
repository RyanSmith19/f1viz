# Race Model Stages

The race model should mature in clear stages. Each stage unlocks a specific type of analysis without forcing later complexity into early layers.

## Stage 0: Raw Source Data

Goal: preserve OpenF1-shaped endpoint records.

Inputs:

- meetings
- sessions
- drivers
- laps
- position
- intervals
- pit
- stints
- race_control
- overtakes

Output:

- `RawSessionData`

Rules:

- Do not interpret race meaning here.
- Keep raw endpoint records close to OpenF1 shape.
- Fixtures and cache entries should live at this stage.

## Stage 1: Resolved Session

Goal: map a user request such as `2025 Monaco Race` to one OpenF1 meeting and one OpenF1 session.

Output:

- `ResolvedSession`

Rules:

- This stage answers "which race are we talking about?"
- It should not calculate pace, strategy, or replay events.

## Stage 2: Normalized Race Session

Goal: convert raw records into stable app concepts.

Output:

- `RaceSession`
- driver map
- lap list
- stint list
- replay timeline records on a common elapsed-time axis

Rules:

- Normalize identities, timestamps, and simple domain objects.
- Preserve the raw source row on normalized records where useful.
- Avoid conclusions.

## Stage 3: Race Facts

Goal: derive factual race events and summaries.

Examples:

- pit stop list
- race control timeline
- position changes
- overtake markers
- stint summaries
- lap pace summaries

Rules:

- Facts may transform data, but should not judge performance yet.
- Every fact should point back to source records.

## Stage 4: Comparative Metrics

Goal: compare drivers, teams, and baselines.

Baselines:

- teammate
- field median
- session leader
- own best comparable lap or stint

Examples:

- lap pace delta
- stint pace delta
- tire-age context
- degradation estimate
- traffic context

Rules:

- Metrics must state their baseline.
- Proxy metrics must be named as proxies.

## Stage 5: Explanatory Replay

Goal: produce conservative, evidence-backed explanations for race replay.

Examples:

- "The stop appears costly relative to nearby cars."
- "The driver lost pace versus field median during this stint."
- "This overtake changed the battle state."

Rules:

- Evidence first, interpretation second.
- Conservative language by default.
- Scores are allowed only when enough baseline data exists.

## Stage 6: Complete Replay Model

Goal: a race can support the planned replay and dashboard experience end to end.

Completeness means the app can provide:

- resolved meeting/session
- driver and team identity
- lap and stint context
- timestamped replay timeline
- race facts
- comparative metrics
- conservative explanations
- Markdown and JSON output

Completeness does not mean every possible OpenF1 endpoint is loaded. It means the model has enough verified structure to support the user-facing race replay workflow honestly.

