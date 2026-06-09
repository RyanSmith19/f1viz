from f1viz.models.openf1 import Meeting, Session
from f1viz.models.session_data import RawSessionData
from f1viz.openf1 import OpenF1Endpoint
from f1viz.services.race_session_builder import RaceSessionBuilder


def test_race_session_builder_maps_drivers_and_sorts_timeline() -> None:
    data = RawSessionData(
        meeting=Meeting(meeting_key=1, year=2025, meeting_name="Sample Grand Prix"),
        session=Session(
            session_key=10,
            meeting_key=1,
            session_name="Race",
            date_start="2025-01-01T14:00:00+00:00",
        ),
        records={
            OpenF1Endpoint.DRIVERS: [
                {
                    "driver_number": 4,
                    "name_acronym": "NOR",
                    "full_name": "Lando Norris",
                    "team_name": "McLaren",
                }
            ],
            OpenF1Endpoint.LAPS: [
                {"driver_number": 4, "lap_number": 2, "lap_duration": 91.2},
                {"driver_number": 4, "lap_number": 1, "lap_duration": 92.1},
            ],
            OpenF1Endpoint.STINTS: [
                {
                    "driver_number": 4,
                    "stint_number": 1,
                    "compound": "MEDIUM",
                    "lap_start": 1,
                    "lap_end": 10,
                }
            ],
            OpenF1Endpoint.POSITION: [
                {
                    "date": "2025-01-01T14:00:12+00:00",
                    "driver_number": 4,
                    "position": 1,
                }
            ],
            OpenF1Endpoint.RACE_CONTROL: [
                {
                    "date": "2025-01-01T14:00:05+00:00",
                    "category": "Flag",
                    "message": "GREEN FLAG",
                }
            ],
        },
    )

    race_session = RaceSessionBuilder().build(data)

    assert race_session.drivers[4].acronym == "NOR"
    assert [lap.lap_number for lap in race_session.laps_for_driver(4)] == [1, 2]
    assert race_session.stints_for_driver(4)[0].compound == "MEDIUM"
    assert race_session.driver_by_acronym("nor").driver_number == 4
    assert [record.elapsed_seconds for record in race_session.timeline] == [5, 12]
    assert race_session.timeline[0].summary == "GREEN FLAG"


def test_race_session_builder_infers_start_from_earliest_dated_record() -> None:
    data = RawSessionData(
        meeting=Meeting(meeting_key=1, year=2025, meeting_name="Sample Grand Prix"),
        session=Session(session_key=10, meeting_key=1, session_name="Race"),
        records={
            OpenF1Endpoint.POSITION: [
                {
                    "date": "2025-01-01T14:00:12Z",
                    "driver_number": 4,
                    "position": 1,
                }
            ],
            OpenF1Endpoint.RACE_CONTROL: [
                {
                    "date": "2025-01-01T14:00:05Z",
                    "category": "Flag",
                    "message": "GREEN FLAG",
                }
            ],
        },
    )

    race_session = RaceSessionBuilder().build(data)

    assert race_session.started_at.isoformat() == "2025-01-01T14:00:05+00:00"
    assert [record.elapsed_seconds for record in race_session.timeline] == [0, 7]
