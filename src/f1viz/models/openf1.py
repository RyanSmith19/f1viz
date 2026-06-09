from datetime import datetime

from pydantic import BaseModel, ConfigDict


class OpenF1Model(BaseModel):
    model_config = ConfigDict(extra="allow")


class Meeting(OpenF1Model):
    meeting_key: int
    year: int
    meeting_name: str
    country_name: str | None = None
    location: str | None = None


class Session(OpenF1Model):
    session_key: int
    meeting_key: int
    session_name: str
    session_type: str | None = None
    year: int | None = None
    date_start: datetime | None = None
    date_end: datetime | None = None
