from pathlib import Path

from f1viz.repositories.fixture_repository import FixtureRepository
from f1viz.services.driver_comparison import DriverComparisonService
from f1viz.services.race_session_builder import RaceSessionBuilder
from f1viz.services.session_fixture_reader import SessionFixtureReader


def test_driver_comparison_compares_any_two_drivers_by_acronym() -> None:
    data = SessionFixtureReader(
        FixtureRepository(Path("tests/fixtures/openf1"))
    ).load(name="sample-race")
    session = RaceSessionBuilder().build(data)

    comparison = DriverComparisonService().compare(session, "NOR", "PIA")

    assert comparison.first.acronym == "NOR"
    assert comparison.second.acronym == "PIA"
    assert comparison.first.best_lap_duration == 92.1
    assert comparison.second.best_lap_duration == 92.4
    assert comparison.best_lap_delta_seconds == 0.3


def test_driver_comparison_can_find_driver_by_number() -> None:
    data = SessionFixtureReader(
        FixtureRepository(Path("tests/fixtures/openf1"))
    ).load(name="sample-race")
    session = RaceSessionBuilder().build(data)

    comparison = DriverComparisonService().compare(session, "4", "81")

    assert comparison.first.acronym == "NOR"
    assert comparison.second.acronym == "PIA"

