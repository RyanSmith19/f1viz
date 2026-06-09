from pathlib import Path

from f1viz.repositories.fixture_repository import FixtureRepository
from f1viz.services.driver_comparison import DriverComparisonService
from f1viz.services.driver_comparison_report_builder import DriverComparisonReportBuilder
from f1viz.services.race_session_builder import RaceSessionBuilder
from f1viz.services.session_fixture_reader import SessionFixtureReader


def test_driver_comparison_report_builder_uses_shared_report_contract() -> None:
    data = SessionFixtureReader(
        FixtureRepository(Path("tests/fixtures/openf1"))
    ).load(name="sample-race")
    session = RaceSessionBuilder().build(data)
    comparison = DriverComparisonService().compare(session, "NOR", "PIA")

    report = DriverComparisonReportBuilder().build(
        meeting=session.meeting,
        session=session.session,
        comparison=comparison,
    )

    assert report.report_type == "driver_comparison"
    assert "Compared NOR and PIA" in report.executive_summary
    assert report.sections[0].title == "Lap Comparison Facts"
    assert "+0.300s" in report.sections[0].summary
