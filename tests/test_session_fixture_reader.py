from pathlib import Path

from f1viz.models.openf1 import Meeting, Session
from f1viz.models.session_data import RawSessionData
from f1viz.openf1 import OpenF1Endpoint
from f1viz.repositories.fixture_repository import FixtureRepository
from f1viz.services.session_fixture_reader import SessionFixtureReader
from f1viz.services.session_fixture_writer import SessionFixtureWriter


def test_session_fixture_reader_reconstructs_raw_session_data(tmp_path) -> None:
    repository = FixtureRepository(tmp_path)
    writer = SessionFixtureWriter(repository)
    reader = SessionFixtureReader(repository)
    original = RawSessionData(
        meeting=Meeting(meeting_key=1254, year=2025, meeting_name="Monaco Grand Prix"),
        session=Session(session_key=9911, meeting_key=1254, session_name="Race", year=2025),
        records={
            OpenF1Endpoint.DRIVERS: [{"driver_number": 4, "name_acronym": "NOR"}],
            OpenF1Endpoint.LAPS: [{"driver_number": 4, "lap_number": 1}],
        },
    )
    writer.save(original, name="2025-monaco-race")

    loaded = reader.load(
        name="2025-monaco-race",
        endpoints=[OpenF1Endpoint.DRIVERS, OpenF1Endpoint.LAPS],
    )

    assert loaded.meeting == original.meeting
    assert loaded.session == original.session
    assert loaded.records == original.records


def test_session_fixture_reader_requires_single_meeting_record(tmp_path) -> None:
    repository = FixtureRepository(tmp_path)
    repository.save(OpenF1Endpoint.MEETINGS, "bad", [])
    repository.save(
        OpenF1Endpoint.SESSIONS,
        "bad",
        [{"session_key": 9911, "meeting_key": 1254, "session_name": "Race"}],
    )
    reader = SessionFixtureReader(repository)

    try:
        reader.load(name="bad", endpoints=[])
    except ValueError as exc:
        assert "exactly one meeting" in str(exc)
    else:
        raise AssertionError("Expected ValueError for invalid meeting fixture")


def test_session_fixture_reader_loads_checked_in_sample_fixture() -> None:
    repository = FixtureRepository(Path("tests/fixtures/openf1"))
    reader = SessionFixtureReader(repository)

    data = reader.load(name="sample-race")

    assert data.meeting.meeting_name == "Sample Grand Prix"
    assert data.session.session_name == "Race"
    assert data.counts_by_endpoint()["drivers"] == 2
