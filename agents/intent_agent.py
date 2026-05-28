import json

from utils.llm import generate_response
from schemas.app_intent_schema import AppIntent


def clean_json_response(response: str):
    return (
        response.strip()
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )


def extract_intent(user_prompt: str) -> AppIntent:

    prompt = f"""
You are an Intent Extraction Agent.

Convert the user prompt into a structured AppIntent.

User Prompt:
{user_prompt}

Return ONLY valid JSON in exactly this format:

{{
  "appName": "string",
  "appType": "crm | project_management | ecommerce | hr_tool | inventory | content_platform | analytics | custom",
  "features": ["string"],
  "entities": ["string"],
  "integrations_requested": ["slack | gmail | stripe | whatsapp | webhook"],
  "assumptions": ["string"],
  "clarification_required": false,
  "clarification_question": null
}}

Rules:
- If prompt is vague, set clarification_required to true and ask one clear question.
- If proceeding with assumptions, document them in assumptions.
- Do not include explanations.
- Do not include markdown.
"""

    response = generate_response(
        prompt,
        stage_name="intent_extraction"
    )

    cleaned = clean_json_response(response)

    parsed = json.loads(cleaned)

    return AppIntent(**parsed)