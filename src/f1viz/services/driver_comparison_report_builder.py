from f1viz.models.comparison import DriverComparisonFacts
from f1viz.models.openf1 import Meeting, Session
from f1viz.models.reports import Confidence, Evidence, RaceReport, ReportSection


class DriverComparisonReportBuilder:
    """Render driver comparison facts as the shared Markdown/JSON report contract."""

    def build(
        self,
        *,
        meeting: Meeting,
        session: Session,
        comparison: DriverComparisonFacts,
    ) -> RaceReport:
        return RaceReport(
            report_type="driver_comparison",
            year=meeting.year,
            grand_prix=meeting.meeting_name,
            session_name=session.session_name,
            executive_summary=_summary(comparison),
            sections=[_lap_comparison_section(comparison)],
        )


def _summary(comparison: DriverComparisonFacts) -> str:
    return (
        f"Compared {comparison.first.acronym} and {comparison.second.acronym} using "
        "lap facts only. Positive deltas mean the second selected driver was slower "
        "than the first selected driver for that metric."
    )


def _lap_comparison_section(comparison: DriverComparisonFacts) -> ReportSection:
    first_best = _format_duration(comparison.first.best_lap_duration)
    first_average = _format_duration(comparison.first.average_lap_duration)
    second_best = _format_duration(comparison.second.best_lap_duration)
    second_average = _format_duration(comparison.second.average_lap_duration)

    return ReportSection(
        title="Lap Comparison Facts",
        summary=(
            f"{comparison.first.acronym}: best lap {first_best}, "
            f"average lap {first_average}. "
            f"{comparison.second.acronym}: best lap {second_best}, "
            f"average lap {second_average}. "
            f"Best-lap delta: {_format_delta(comparison.best_lap_delta_seconds)}. "
            f"Average-lap delta: {_format_delta(comparison.average_lap_delta_seconds)}."
        ),
        evidence=[
            Evidence(
                label="Comparison baseline",
                detail=comparison.baseline,
                source="DriverComparisonService",
            ),
            Evidence(
                label=comparison.first.acronym,
                detail=f"{comparison.first.lap_count} laps included.",
                source="RaceSession.laps",
            ),
            Evidence(
                label=comparison.second.acronym,
                detail=f"{comparison.second.lap_count} laps included.",
                source="RaceSession.laps",
            ),
        ],
        confidence=Confidence.HIGH,
    )


def _format_duration(value: float | None) -> str:
    if value is None:
        return "not available"
    return f"{value:.3f}s"


def _format_delta(value: float | None) -> str:
    if value is None:
        return "not available"
    return f"{value:+.3f}s"
