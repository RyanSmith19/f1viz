from f1viz.models.openf1 import Meeting, Session
from f1viz.models.session_data import RawSessionData
from f1viz.openf1 import OpenF1Endpoint
from f1viz.repositories.fixture_repository import FixtureRepository
from f1viz.services.session_fixture_writer import SessionFixtureWriter


def test_session_fixture_writer_saves_meeting_session_and_endpoint_records(tmp_path) -> None:
    repository = FixtureRepository(tmp_path)
    writer = SessionFixtureWriter(repository)
    data = RawSessionData(
        meeting=Meeting(meeting_key=1254, year=2025, meeting_name="Monaco Grand Prix"),
        session=Session(session_key=9911, meeting_key=1254, session_name="Race", year=2025),
        records={
            OpenF1Endpoint.DRIVERS: [{"driver_number": 4, "name_acronym": "NOR"}],
            OpenF1Endpoint.LAPS: [{"driver_number": 4, "lap_number": 1}],
        },
    )

    paths = writer.save(data, name="2025-monaco-race")

    assert tmp_path / "meetings" / "2025-monaco-race.json" in paths
    assert tmp_path / "sessions" / "2025-monaco-race.json" in paths
    assert repository.load(OpenF1Endpoint.DRIVERS, "2025-monaco-race") == [
        {"driver_number": 4, "name_acronym": "NOR"}
    ]

