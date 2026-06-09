from pydantic import BaseModel


class DriverLapSummary(BaseModel):
    driver_number: int
    acronym: str
    lap_count: int
    best_lap_duration: float | None = None
    average_lap_duration: float | None = None


class DriverComparisonFacts(BaseModel):
    first: DriverLapSummary
    second: DriverLapSummary
    best_lap_delta_seconds: float | None = None
    average_lap_delta_seconds: float | None = None
    baseline: str = "selected drivers"

