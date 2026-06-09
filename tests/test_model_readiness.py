from datetime import UTC, datetime

from f1viz.models.model_stage import ModelStage
from f1viz.models.openf1 import Meeting, Session
from f1viz.models.race_session import DriverInfo, LapInfo, RaceSession, StintInfo, TimelineRecord
from f1viz.openf1 import OpenF1Endpoint
from f1viz.services.model_readiness import assess_race_session_readiness


def test_model_readiness_marks_next_stage_when_comparative_metrics_are_missing() -> None:
    session = RaceSession(
        meeting=Meeting(meeting_key=1, year=2025, meeting_name="Sample Grand Prix"),
        session=Session(session_key=10, meeting_key=1, session_name="Race"),
        started_at=datetime(2025, 1, 1, 14, tzinfo=UTC),
        drivers={4: DriverInfo(driver_number=4, acronym="NOR")},
        laps=[LapInfo(driver_number=4, lap_number=1, lap_duration=92.1, raw={})],
        stints=[StintInfo(driver_number=4, stint_number=1, compound="MEDIUM", raw={})],
        timeline=[
            TimelineRecord(
                elapsed_seconds=0,
                endpoint=OpenF1Endpoint.RACE_CONTROL,
                category="flag",
                summary="GREEN FLAG",
                source_time=datetime(2025, 1, 1, 14, tzinfo=UTC),
                raw={},
            )
        ],
    )

    readiness = assess_race_session_readiness(session)

    assert ModelStage.RACE_FACTS in readiness.completed
    assert ModelStage.EXPLANATORY_REPLAY in readiness.completed
    assert readiness.next_stage == ModelStage.COMPARATIVE_METRICS
    assert readiness.missing == []


def test_model_readiness_reports_missing_laps_stints_and_timeline() -> None:
    session = RaceSession(
        meeting=Meeting(meeting_key=1, year=2025, meeting_name="Sample Grand Prix"),
        session=Session(session_key=10, meeting_key=1, session_name="Race"),
        started_at=datetime(2025, 1, 1, 14, tzinfo=UTC),
        drivers={4: DriverInfo(driver_number=4, acronym="NOR")},
    )

    readiness = assess_race_session_readiness(session)

    assert readiness.next_stage == ModelStage.RACE_FACTS
    assert "lap records" in readiness.missing
    assert "stint records" in readiness.missing
    assert "timestamped replay timeline records" in readiness.missing
