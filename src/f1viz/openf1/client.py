from collections.abc import Mapping
from typing import Any

import httpx

from f1viz.openf1.endpoints import OpenF1Endpoint


class OpenF1Client:
    """Small typed wrapper around the OpenF1 REST API."""

    def __init__(
        self,
        *,
        base_url: str = "https://api.openf1.org/v1",
        timeout: float = 20.0,
        http_client: httpx.Client | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._client = http_client

    def get(
        self,
        endpoint: OpenF1Endpoint,
        params: Mapping[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        client = self._client or httpx.Client(timeout=self.timeout)
        close_client = self._client is None
        try:
            response = client.get(f"{self.base_url}/{endpoint.value}", params=params)
            response.raise_for_status()
            payload = response.json()
        finally:
            if close_client:
                client.close()

        if not isinstance(payload, list):
            raise TypeError(f"OpenF1 endpoint {endpoint.value} returned {type(payload).__name__}")

        return payload

    def meetings(self, **params: Any) -> list[dict[str, Any]]:
        return self.get(OpenF1Endpoint.MEETINGS, params)

    def sessions(self, **params: Any) -> list[dict[str, Any]]:
        return self.get(OpenF1Endpoint.SESSIONS, params)

    def drivers(self, **params: Any) -> list[dict[str, Any]]:
        return self.get(OpenF1Endpoint.DRIVERS, params)

    def laps(self, **params: Any) -> list[dict[str, Any]]:
        return self.get(OpenF1Endpoint.LAPS, params)

    def positions(self, **params: Any) -> list[dict[str, Any]]:
        return self.get(OpenF1Endpoint.POSITION, params)

    def intervals(self, **params: Any) -> list[dict[str, Any]]:
        return self.get(OpenF1Endpoint.INTERVALS, params)

    def pit_stops(self, **params: Any) -> list[dict[str, Any]]:
        return self.get(OpenF1Endpoint.PIT, params)

    def stints(self, **params: Any) -> list[dict[str, Any]]:
        return self.get(OpenF1Endpoint.STINTS, params)

    def race_control(self, **params: Any) -> list[dict[str, Any]]:
        return self.get(OpenF1Endpoint.RACE_CONTROL, params)

    def overtakes(self, **params: Any) -> list[dict[str, Any]]:
        return self.get(OpenF1Endpoint.OVERTAKES, params)

    def car_data(self, **params: Any) -> list[dict[str, Any]]:
        return self.get(OpenF1Endpoint.CAR_DATA, params)

    def location(self, **params: Any) -> list[dict[str, Any]]:
        return self.get(OpenF1Endpoint.LOCATION, params)

