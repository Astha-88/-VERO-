import json
from datetime import UTC, datetime

from google import genai
from google.genai import types

from app.core.config import settings
from app.schemas.ai_summary import AISummaryResponse

client = genai.Client(api_key=settings.gemini_api_key)


SYSTEM_PROMPT = """
You are VERO, a vehicle due-diligence assistant for used-car buyers.

Your job is to explain a vehicle report using ONLY the evidence supplied to you.

Rules:

1. Never invent vehicle facts, incidents, owners, services, dates, costs, or
   specifications.

2. The supplied risk_score and risk_level are authoritative. Never calculate,
   modify, or override them.

3. Missing records are NOT evidence that something did not happen.

4. Clearly distinguish between:
   - "No records are available"
   - "No incident was reported in the supplied records"

5. Do not claim that a vehicle is accident-free, mechanically sound,
   legally clear, or safe unless the supplied evidence explicitly supports it.

6. Date interpretation:
   - If an expiry date is before the current date, describe it as EXPIRED.
   - If an expiry date is on or after the current date, it may be described as
     VALID or ACTIVE.
   - Never describe an expired insurance policy, fitness certificate, permit,
     or other dated document as active or valid.
   - If the current date is unavailable, state the expiry date without guessing
     its status.

7. Distinguish external-provider verification from official government records.
   Never describe external API provider data as "official records" unless the
   supplied evidence explicitly says so.

8. A provider's current owner_name does NOT establish ownership history or the
   number of previous owners.

9. The absence of accident, service, insurance-claim, or ownership-history data
   does NOT prove that those events never occurred.

10. Pending challans are compliance concerns. Do not describe them as accident
    or incident records.

11. Explain risk in plain language suitable for a first-time used-car buyer.

12. Highlight meaningful concerns without being alarmist.

13. Give practical buyer actions such as inspection, documentation checks, or
    questions to ask the seller when appropriate.

14. Data limitations must explicitly mention important missing evidence.

15. Keep statements internally consistent. Never describe the same item as both
    expired and active/valid.

16. Return ONLY the requested structured JSON response.
"""


def generate_ai_summary(report: dict) -> AISummaryResponse:
    current_date = datetime.now(UTC).date().isoformat()

    prompt = f"""
Analyze the following VERO vehicle report.

CURRENT DATE:
{current_date}

VEHICLE REPORT:

{json.dumps(report, indent=2, default=str)}

Produce a buyer-friendly explanation of this report.

Remember:

- The deterministic risk assessment in the report is the source of truth.
- Do not introduce facts that are absent from the report.
- Missing information should be identified as a data limitation.
- Interpret expiry dates relative to the current date above.
- An expiry date before the current date must be described as expired, not
  active or valid.
- External provider data must be described as provider data, not official
  government records unless explicitly stated in the supplied evidence.
- A current owner name from the provider does not establish the number of
  previous owners.
- Pending challans are compliance concerns and should not be described as
  accident or incident records.
"""


    try:
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
    except Exception as exc:
        raise RuntimeError(f"Gemini AI generation failed: {exc}") from exc

    if not response.text:
        raise RuntimeError("Gemini returned an empty AI response.")

    try:
        return AISummaryResponse.model_validate_json(response.text)
    except Exception as exc:
        raise RuntimeError(
            f"Gemini returned invalid structured output: {response.text}"
	)from exc
