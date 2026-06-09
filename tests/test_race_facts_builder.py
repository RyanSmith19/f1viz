from pathlib import Path

from f1viz.repositories.fixture_repository import FixtureRepository
from f1viz.services.race_facts_builder import RaceFactsBuilder
from f1viz.services.race_session_builder import RaceSessionBuilder
from f1viz.services.session_fixture_reader import SessionFixtureReader


def test_race_facts_builder_summarizes_session_without_interpretation() -> None:
    data = SessionFixtureReader(
        FixtureRepository(Path("tests/fixtures/openf1"))
    ).load(name="sample-race")
    session = RaceSessionBuilder().build(data)

    facts = RaceFactsBuilder().build(session)

    assert facts.driver_count == 2
    assert facts.lap_count == 2
    assert facts.stint_count == 2
    assert facts.timeline_record_count == 4
    assert facts.timeline_category_counts == {
        "flag": 1,
        "intervals": 1,
        "position": 2,
    }
    assert facts.drivers[4].acronym == "NOR"
    assert facts.drivers[4].lap_count == 1
    assert facts.drivers[81].stint_count == 1

