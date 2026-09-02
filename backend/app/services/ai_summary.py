import json

from google import genai
from google.genai import types

from app.core.config import settings
from app.schemas.ai_summary import AISummaryResponse


client = genai.Client(api_key=settings.gemini_api_key)


SYSTEM_PROMPT = """
You are VERO, a vehicle due-diligence assistant for used-car buyers.

Your job is to explain a vehicle report using ONLY the evidence supplied to you.

Rules:
1. Never invent vehicle facts, incidents, owners, services, dates, costs, or specifications.
2. The supplied risk_score and risk_level are authoritative. Never calculate,
   modify, or override them.
3. Missing records are NOT evidence that something did not happen.
4. Clearly distinguish between:
   - "No records are available"
   - "No incident was reported in the supplied records"
5. Do not claim that a vehicle is accident-free, mechanically sound,
   legally clear, or safe unless the supplied evidence explicitly supports it.
6. Explain risk in plain language suitable for a first-time used-car buyer.
7. Highlight meaningful concerns without being alarmist.
8. Give practical buyer actions such as inspection, documentation checks,
   or questions to ask the seller when appropriate.
9. Data limitations must explicitly mention important missing evidence.
10. Return only the requested structured JSON response.
"""


def generate_ai_summary(report: dict) -> AISummaryResponse:
    prompt = f"""
Analyze the following VERO vehicle report.

VEHICLE REPORT:
{json.dumps(report, indent=2, default=str)}

Produce a buyer-friendly explanation of this report.

Remember:
- The deterministic risk assessment in the report is the source of truth.
- Do not introduce facts that are absent from the report.
- Missing information should be identified as a data limitation.
"""

    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=[
            SYSTEM_PROMPT,
            prompt,
        ],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=AISummaryResponse,
        ),
    )

    if not response.text:
        raise ValueError("AI did not return a structured vehicle summary.")

    return AISummaryResponse.model_validate_json(response.text)
