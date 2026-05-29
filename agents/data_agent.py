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
Every relation target MUST also exist as an entity in the entities list.

Before generating relations, ensure the target entity is created.
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

    # normalize invalid relation types
    allowed_relation_types = ["hasMany", "belongsTo", "hasOne"]

    for entity in parsed.get("entities", []):
        for relation in entity.get("relations", []):
            if relation.get("type") not in allowed_relation_types:
                relation["type"] = "hasMany"

    parsed = normalize_data_schema(parsed)
    return DataSchema(**parsed)




def normalize_data_schema(parsed):
    allowed_relation_types = ["hasMany", "belongsTo", "hasOne"]
    allowed_field_types = ["string", "number", "boolean", "date", "datetime", "text", "enum", "json"]

    for entity in parsed.get("entities", []):
        if "fields" not in entity:
            entity["fields"] = []

        field_names = [field.get("name") for field in entity["fields"]]

        if "id" not in field_names:
            entity["fields"].insert(0, {
                "name": "id",
                "type": "string",
                "nullable": False,
                "isRelation": False,
                "isPrimary": True,
                "isUnique": True
            })

        if "tenantId" not in field_names:
            entity["fields"].append({
                "name": "tenantId",
                "type": "string",
                "nullable": False,
                "isRelation": False,
                "isPrimary": False,
                "isUnique": False
            })

        for field in entity["fields"]:
            if field.get("type") not in allowed_field_types:
                field["type"] = "string"

            field.setdefault("nullable", False)
            field.setdefault("isRelation", False)
            field.setdefault("isPrimary", False)
            field.setdefault("isUnique", False)

        for relation in entity.get("relations", []):
            if relation.get("type") not in allowed_relation_types:
                relation["type"] = "hasMany"

            if "target" not in relation and "entity" in relation:
                relation["target"] = relation["entity"]

            if "foreignKey" not in relation and "field" in relation:
                relation["foreignKey"] = relation["field"]

            relation.setdefault("foreignKey", "id")
            relation.setdefault("onDelete", "cascade")

    return parsed