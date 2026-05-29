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

    parsed = normalize_intent(parsed)
    return AppIntent(**parsed)


def normalize_intent(parsed):
    if not parsed.get("appName"):
        parsed["appName"] = "Untitled App"

    if not parsed.get("appType"):
        parsed["appType"] = "custom"

    if not parsed.get("features"):
        parsed["features"] = ["basic dashboard"]

    if not parsed.get("entities"):
        parsed["entities"] = ["User"]

    if not parsed.get("integrations_requested"):
        parsed["integrations_requested"] = []

    if not parsed.get("assumptions"):
        parsed["assumptions"] = [
            "Prompt was vague, so a basic application structure was assumed."
        ]

    parsed.setdefault("clarification_required", True)
    parsed.setdefault(
        "clarification_question",
        "What type of application do you want to build?"
    )

    return parsed