from collections.abc import Iterable

from f1viz.models.openf1 import Meeting, Session
from f1viz.models.session_data import RawSessionData
from f1viz.openf1.endpoints import OpenF1Endpoint
from f1viz.repositories.fixture_repository import FixtureRepository
from f1viz.services.session_data_loader import CORE_RACE_ENDPOINTS


class SessionFixtureReader:
    """Reconstruct raw session data from saved endpoint fixtures."""

    def __init__(self, repository: FixtureRepository) -> None:
        self.repository = repository

    def load(
        self,
        *,
        name: str,
        endpoints: Iterable[OpenF1Endpoint] = CORE_RACE_ENDPOINTS,
    ) -> RawSessionData:
        meetings = self.repository.load(OpenF1Endpoint.MEETINGS, name)
        sessions = self.repository.load(OpenF1Endpoint.SESSIONS, name)

        if len(meetings) != 1:
            raise ValueError(f"Fixture {name} must contain exactly one meeting record")
        if len(sessions) != 1:
            raise ValueError(f"Fixture {name} must contain exactly one session record")

        records = {
            endpoint: self.repository.load(endpoint, name)
            for endpoint in endpoints
        }

        return RawSessionData(
            meeting=Meeting.model_validate(meetings[0]),
            session=Session.model_validate(sessions[0]),
            records=records,
        )

