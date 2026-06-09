from f1viz.models.model_stage import ModelStage
from f1viz.models.race_facts import RaceFacts
from f1viz.models.race_session import RaceSession, TimelineRecord
from f1viz.models.reports import Confidence, Evidence, RaceReport, ReplayEvent, ReportSection
from f1viz.services.model_readiness import assess_race_session_readiness
from f1viz.services.race_facts_builder import RaceFactsBuilder


class RaceReportBuilder:
    """Create conservative report output from normalized race-session facts."""

    def build(self, session: RaceSession) -> RaceReport:
        readiness = assess_race_session_readiness(session)
        facts = RaceFactsBuilder().build(session)

        return RaceReport(
            year=session.meeting.year,
            grand_prix=session.meeting.meeting_name,
            session_name=session.session.session_name,
            executive_summary=(
                f"Loaded {facts.driver_count} drivers, {facts.lap_count} laps, "
                f"{facts.stint_count} stints, and {facts.timeline_record_count} "
                "replay timeline records. "
                "This report states model facts only; performance interpretation comes in "
                "later stages."
            ),
            sections=[
                _data_coverage_section(facts),
                _readiness_section(readiness.completed, readiness.next_stage, readiness.missing),
            ],
            timeline=[_to_replay_event(record) for record in session.timeline],
        )


def _data_coverage_section(facts: RaceFacts) -> ReportSection:
    return ReportSection(
        title="Data Coverage",
        summary=(
            f"The normalized race model contains {facts.driver_count} drivers, "
            f"{facts.lap_count} laps, {facts.stint_count} stints, and "
            f"{facts.timeline_record_count} timestamped timeline records."
        ),
        evidence=[
            Evidence(
                label="Normalized model",
                detail="Counts are derived from RaceFacts.",
                source="RaceFactsBuilder",
            )
        ],
        confidence=Confidence.HIGH,
    )


def _readiness_section(
    completed: list[ModelStage],
    next_stage: ModelStage | None,
    missing: list[str],
) -> ReportSection:
    completed_text = ", ".join(stage.value for stage in completed)
    if next_stage is None:
        summary = f"Completed model stages: {completed_text}. The replay model is complete."
    else:
        summary = f"Completed model stages: {completed_text}. Next stage: {next_stage.value}."

    evidence = [
        Evidence(
            label="Model stage guide",
            detail="Stage definitions are documented in docs/architecture/model-stages.md.",
            source="docs/architecture/model-stages.md",
        )
    ]
    for item in missing:
        evidence.append(
            Evidence(
                label="Missing input",
                detail=item,
                source="RaceSession readiness assessment",
            )
        )

    return ReportSection(
        title="Model Readiness",
        summary=summary,
        evidence=evidence,
        confidence=Confidence.HIGH,
    )


def _to_replay_event(record: TimelineRecord) -> ReplayEvent:
    return ReplayEvent(
        elapsed_seconds=record.elapsed_seconds,
        title=record.summary,
        category=record.category,
        summary=(
            f"Observed {record.endpoint.value} record at "
            f"{record.source_time.isoformat()}."
        ),
        evidence=[
            Evidence(
                label="Source endpoint",
                detail=record.endpoint.value,
                source="OpenF1 fixture",
            )
        ],
        confidence=Confidence.HIGH,
    )
