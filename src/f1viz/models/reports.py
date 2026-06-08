from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, Field


class Confidence(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Evidence(BaseModel):
    label: str
    detail: str
    source: str


class ReplayEvent(BaseModel):
    elapsed_seconds: float = Field(ge=0)
    title: str
    category: str
    summary: str
    evidence: list[Evidence] = Field(default_factory=list)
    confidence: Confidence = Confidence.MEDIUM


class ReportSection(BaseModel):
    title: str
    summary: str
    evidence: list[Evidence] = Field(default_factory=list)
    confidence: Confidence = Confidence.MEDIUM


class RaceReport(BaseModel):
    report_type: str = "race_analysis"
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    year: int
    grand_prix: str
    session_name: str = "Race"
    executive_summary: str
    sections: list[ReportSection] = Field(default_factory=list)
    timeline: list[ReplayEvent] = Field(default_factory=list)

