from collections.abc import Iterable
from typing import Any, Protocol

from f1viz.models.session_data import RawSessionData
from f1viz.openf1.endpoints import OpenF1Endpoint
from f1viz.services.session_resolver import SessionResolver

CORE_RACE_ENDPOINTS: tuple[OpenF1Endpoint, ...] = (
    OpenF1Endpoint.DRIVERS,
    OpenF1Endpoint.LAPS,
    OpenF1Endpoint.POSITION,
    OpenF1Endpoint.INTERVALS,
    OpenF1Endpoint.PIT,
    OpenF1Endpoint.STINTS,
    OpenF1Endpoint.RACE_CONTROL,
    OpenF1Endpoint.OVERTAKES,
)


class OpenF1Readable(Protocol):
    def meetings(self, **params: Any) -> list[dict[str, Any]]: ...

    def sessions(self, **params: Any) -> list[dict[str, Any]]: ...

    def get(
        self,
        endpoint: OpenF1Endpoint,
        params: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]: ...


class SessionDataLoader:
    """Load raw OpenF1 data for a resolved race weekend/session."""

    def __init__(
        self,
        client: OpenF1Readable,
        *,
        resolver: SessionResolver | None = None,
    ) -> None:
        self.client = client
        self.resolver = resolver or SessionResolver()

    def load(
        self,
        *,
        year: int,
        grand_prix: str,
        session_name: str = "Race",
        endpoints: Iterable[OpenF1Endpoint] = CORE_RACE_ENDPOINTS,
    ) -> RawSessionData:
        meetings = self.client.meetings(year=year)
        sessions = self.client.sessions(year=year)
        resolved = self.resolver.resolve(
            meetings=meetings,
            sessions=sessions,
            year=year,
            grand_prix=grand_prix,
            session_name=session_name,
        )

        records = {
            endpoint: self.client.get(endpoint, {"session_key": resolved.session.session_key})
            for endpoint in endpoints
        }

        return RawSessionData(
            meeting=resolved.meeting,
            session=resolved.session,
            records=records,
        )
