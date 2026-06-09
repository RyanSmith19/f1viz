from typing import Any

from f1viz.openf1 import OpenF1Endpoint
from f1viz.services.session_data_loader import CORE_RACE_ENDPOINTS, SessionDataLoader


class FakeOpenF1Client:
    def __init__(self) -> None:
        self.calls: list[tuple[OpenF1Endpoint, dict[str, Any] | None]] = []

    def meetings(self, **params: Any) -> list[dict[str, Any]]:
        assert params == {"year": 2025}
        return [
            {
                "meeting_key": 1254,
                "year": 2025,
                "meeting_name": "Monaco Grand Prix",
            }
        ]

    def sessions(self, **params: Any) -> list[dict[str, Any]]:
        assert params == {"year": 2025}
        return [
            {
                "session_key": 9911,
                "meeting_key": 1254,
                "session_name": "Race",
                "session_type": "Race",
                "year": 2025,
            }
        ]

    def get(
        self,
        endpoint: OpenF1Endpoint,
        params: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        self.calls.append((endpoint, params))
        return [{"endpoint": endpoint.value, "session_key": params["session_key"]}]


def test_session_data_loader_resolves_session_and_fetches_core_endpoints() -> None:
    client = FakeOpenF1Client()
    loader = SessionDataLoader(client)

    data = loader.load(year=2025, grand_prix="monaco")

    assert data.meeting.meeting_key == 1254
    assert data.session.session_key == 9911
    assert set(data.records) == set(CORE_RACE_ENDPOINTS)
    assert data.counts_by_endpoint()["laps"] == 1
    assert all(params == {"session_key": 9911} for _endpoint, params in client.calls)


def test_session_data_loader_can_limit_endpoints() -> None:
    client = FakeOpenF1Client()
    loader = SessionDataLoader(client)

    data = loader.load(
        year=2025,
        grand_prix="monaco",
        endpoints=[OpenF1Endpoint.DRIVERS, OpenF1Endpoint.LAPS],
    )

    assert set(data.records) == {OpenF1Endpoint.DRIVERS, OpenF1Endpoint.LAPS}
    assert [endpoint for endpoint, _params in client.calls] == [
        OpenF1Endpoint.DRIVERS,
        OpenF1Endpoint.LAPS,
    ]

