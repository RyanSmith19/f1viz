from typing import Any

from pydantic import BaseModel, Field

from f1viz.models.openf1 import Meeting, Session
from f1viz.openf1.endpoints import OpenF1Endpoint


class RawSessionData(BaseModel):
    """Raw OpenF1 data for a resolved session.

    This is intentionally close to the API shape. Normalized race models should be
    built from this object in the next roadmap phase.
    """

    meeting: Meeting
    session: Session
    records: dict[OpenF1Endpoint, list[dict[str, Any]]] = Field(default_factory=dict)

    def get(self, endpoint: OpenF1Endpoint) -> list[dict[str, Any]]:
        return self.records.get(endpoint, [])

    def counts_by_endpoint(self) -> dict[str, int]:
        return {endpoint.value: len(rows) for endpoint, rows in self.records.items()}

