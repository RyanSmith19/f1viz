from pathlib import Path

from f1viz.repositories.fixture_repository import FixtureRepository
from f1viz.services.race_report_builder import RaceReportBuilder
from f1viz.services.race_session_builder import RaceSessionBuilder
from f1viz.services.session_fixture_reader import SessionFixtureReader


def test_race_report_builder_creates_fixture_backed_report() -> None:
    data = SessionFixtureReader(
        FixtureRepository(Path("tests/fixtures/openf1"))
    ).load(name="sample-race")
    session = RaceSessionBuilder().build(data)

    report = RaceReportBuilder().build(session)

    assert report.grand_prix == "Sample Grand Prix"
    assert "2 drivers" in report.executive_summary
    assert report.sections[0].title == "Data Coverage"
    assert report.sections[1].title == "Model Readiness"
    assert report.timeline[0].elapsed_seconds == 0
    assert report.timeline[0].category == "position"
