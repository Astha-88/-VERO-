from pydantic import BaseModel


class RiskAssessmentResponse(BaseModel):
    risk_score: int
    risk_level: str
    red_flags: list[str]
    positive_signals: list[str]
