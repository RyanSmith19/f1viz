from pathlib import Path

from f1viz.models.session_data import RawSessionData
from f1viz.openf1.endpoints import OpenF1Endpoint
from f1viz.repositories.fixture_repository import FixtureRepository


class SessionFixtureWriter:
    """Persist raw session data into endpoint fixtures."""

    def __init__(self, repository: FixtureRepository) -> None:
        self.repository = repository

    def save(self, data: RawSessionData, *, name: str) -> list[Path]:
        paths = [
            self.repository.save(OpenF1Endpoint.MEETINGS, name, [data.meeting.model_dump()]),
            self.repository.save(OpenF1Endpoint.SESSIONS, name, [data.session.model_dump()]),
        ]

        for endpoint, rows in data.records.items():
            paths.append(self.repository.save(endpoint, name, rows))

        return paths

