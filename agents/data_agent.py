import json

from utils.llm import generate_response
from schemas.data_schema_v2 import DataSchema


def clean_json_response(response: str):
    return (
        response.strip()
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )


def generate_data_schema(app_intent) -> DataSchema:

    prompt = f"""
You are a Data Schema Generation Agent.

Convert this AppIntent into a structured DataSchema.

AppIntent:
{app_intent.model_dump()}

Return ONLY valid JSON in exactly this format:

{{
  "entities": [
    {{
      "name": "Lead",
      "tableName": "leads",
      "fields": [
        {{
          "name": "id",
          "type": "string",
          "nullable": false,
          "isRelation": false,
          "isPrimary": true,
          "isUnique": true
        }},
        {{
          "name": "tenantId",
          "type": "string",
          "nullable": false,
          "isRelation": false,
          "isPrimary": false,
          "isUnique": false
        }}
      ],
      "relations": [
  {{
    "type": "belongsTo",
    "target": "Lead",
    "foreignKey": "leadId",
    "onDelete": "cascade"
  }}
]
    }}
  ]
}}

Rules:
- Every entity MUST include tenantId.
- tableName must be snake_case plural.
- Include id as primary field.
- Use only these field types:
  string, number, boolean, date, datetime, text, enum, json
- relations must reference existing entities only.
- Do not include explanations.
- Do not include markdown.

Relations MUST follow exactly this format:
{{
  "type": "belongsTo | hasMany | hasOne",
  "target": "ExistingEntityName",
  "foreignKey": "fieldName",
  "onDelete": "cascade"
}}

Do NOT use "entity" or "field" keys inside relations.
"""

    response = generate_response(
        prompt,
        stage_name="schema_generation"
    )

    cleaned = clean_json_response(response)

    parsed = json.loads(cleaned)

    return DataSchema(**parsed)