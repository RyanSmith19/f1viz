from pydantic import BaseModel, Field


class DriverRaceFacts(BaseModel):
    driver_number: int
    acronym: str
    lap_count: int = 0
    stint_count: int = 0
    timeline_record_count: int = 0


class RaceFacts(BaseModel):
    driver_count: int
    lap_count: int
    stint_count: int
    timeline_record_count: int
    timeline_category_counts: dict[str, int] = Field(default_factory=dict)
    drivers: dict[int, DriverRaceFacts] = Field(default_factory=dict)

