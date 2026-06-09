from enum import StrEnum

from pydantic import BaseModel, Field


class ModelStage(StrEnum):
    RAW_SOURCE = "raw_source"
    RESOLVED_SESSION = "resolved_session"
    NORMALIZED_SESSION = "normalized_session"
    RACE_FACTS = "race_facts"
    COMPARATIVE_METRICS = "comparative_metrics"
    EXPLANATORY_REPLAY = "explanatory_replay"
    COMPLETE_REPLAY_MODEL = "complete_replay_model"


class ModelReadiness(BaseModel):
    completed: list[ModelStage] = Field(default_factory=list)
    next_stage: ModelStage | None = None
    missing: list[str] = Field(default_factory=list)

    @property
    def is_complete(self) -> bool:
        return self.next_stage is None

