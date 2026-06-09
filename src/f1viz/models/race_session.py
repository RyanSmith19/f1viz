from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from f1viz.models.openf1 import Meeting, Session
from f1viz.openf1.endpoints import OpenF1Endpoint


class DriverInfo(BaseModel):
    driver_number: int
    acronym: str
    full_name: str | None = None
    team_name: str | None = None


class TimelineRecord(BaseModel):
    elapsed_seconds: float = Field(ge=0)
    endpoint: OpenF1Endpoint
    driver_number: int | None = None
    category: str
    summary: str
    source_time: datetime
    raw: dict[str, Any]


class LapInfo(BaseModel):
    driver_number: int
    lap_number: int
    lap_duration: float | None = None
    raw: dict[str, Any]


class StintInfo(BaseModel):
    driver_number: int
    stint_number: int
    compound: str | None = None
    lap_start: int | None = None
    lap_end: int | None = None
    raw: dict[str, Any]


class RaceSession(BaseModel):
    meeting: Meeting
    session: Session
    started_at: datetime
    drivers: dict[int, DriverInfo]
    laps: list[LapInfo] = Field(default_factory=list)
    stints: list[StintInfo] = Field(default_factory=list)
    timeline: list[TimelineRecord] = Field(default_factory=list)

    def driver_by_acronym(self, acronym: str) -> DriverInfo | None:
        normalized = acronym.upper()
        return next(
            (driver for driver in self.drivers.values() if driver.acronym.upper() == normalized),
            None,
        )

    def laps_for_driver(self, driver_number: int) -> list[LapInfo]:
        return [lap for lap in self.laps if lap.driver_number == driver_number]

    def stints_for_driver(self, driver_number: int) -> list[StintInfo]:
        return [stint for stint in self.stints if stint.driver_number == driver_number]

    def timeline_for_driver(self, driver_number: int) -> list[TimelineRecord]:
        return [record for record in self.timeline if record.driver_number == driver_number]
