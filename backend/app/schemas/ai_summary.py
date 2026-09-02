from pydantic import BaseModel, Field


class AISummaryResponse(BaseModel):
    summary: str = Field(
        description="A concise buyer-friendly summary of the vehicle's condition and risk."
    )
    risk_explanation: str = Field(
        description="Explanation of the deterministic risk assessment using only supplied evidence."
    )
    key_concerns: list[str] = Field(
        default_factory=list,
        description="Important concerns a buyer should investigate."
    )
    positive_signals: list[str] = Field(
        default_factory=list,
        description="Evidence-supported positive signals about the vehicle."
    )
    buyer_advice: list[str] = Field(
        default_factory=list,
        description="Practical actions the buyer should take before purchasing."
    )
    data_limitations: list[str] = Field(
        default_factory=list,
        description="Important limitations caused by missing or unavailable vehicle data."
    )
