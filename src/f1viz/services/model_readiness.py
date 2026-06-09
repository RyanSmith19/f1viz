from f1viz.models.model_stage import ModelReadiness, ModelStage
from f1viz.models.race_session import RaceSession


def assess_race_session_readiness(session: RaceSession) -> ModelReadiness:
    """Assess how far a normalized race session has progressed toward replay completeness."""
    completed = [
        ModelStage.RAW_SOURCE,
        ModelStage.RESOLVED_SESSION,
        ModelStage.NORMALIZED_SESSION,
    ]
    missing: list[str] = []

    if not session.drivers:
        missing.append("driver identity map")
    if not session.started_at:
        missing.append("session start time")

    has_lap_stint_facts = bool(session.laps) and bool(session.stints)
    if has_lap_stint_facts:
        completed.append(ModelStage.RACE_FACTS)
    else:
        if not session.laps:
            missing.append("lap records")
        if not session.stints:
            missing.append("stint records")

    if session.timeline:
        completed.append(ModelStage.EXPLANATORY_REPLAY)
    else:
        missing.append("timestamped replay timeline records")

    next_stage = _next_stage(completed)
    return ModelReadiness(completed=completed, next_stage=next_stage, missing=missing)


def _next_stage(completed: list[ModelStage]) -> ModelStage | None:
    order = [
        ModelStage.RAW_SOURCE,
        ModelStage.RESOLVED_SESSION,
        ModelStage.NORMALIZED_SESSION,
        ModelStage.RACE_FACTS,
        ModelStage.COMPARATIVE_METRICS,
        ModelStage.EXPLANATORY_REPLAY,
        ModelStage.COMPLETE_REPLAY_MODEL,
    ]

    for stage in order:
        if stage not in completed:
            return stage
    return None
