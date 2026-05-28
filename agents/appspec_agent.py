
import json

from utils.llm import generate_response
from schemas.appspec_schema import AppSpec


def clean_json_response(response: str):
    return (
        response.strip()
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )


def generate_appspec(app_intent, data_schema) -> AppSpec:

    prompt = f"""
You are an AppSpec Generation Agent.

Generate a structured AppSpec from this AppIntent and DataSchema.

AppIntent:
{app_intent.model_dump()}

DataSchema:
{data_schema.model_dump()}

Return ONLY valid JSON in EXACTLY this structure:

{{
  "pages": [
    {{
      "name": "Leads",
      "route": "/leads",
      "layout": "list",
      "boundEntity": "Lead",
      "components": ["table", "form"]
    }}
  ],
  "apiEndpoints": [
    {{
      "path": "/api/leads",
      "method": "GET",
      "handler": "List leads",
      "boundEntity": "Lead",
      "authRequired": true,
      "rateLimit": true
    }}
  ],
  "authRules": [
    {{
      "role": "admin",
      "permissions": [
        {{
          "entity": "Lead",
          "read": true,
          "write": true,
          "delete": true
        }}
      ]
    }}
  ],
  "integrationHooks": [
    {{
      "integration": "whatsapp",
      "trigger": "status_changed",
      "action": "send_template_message"
    }}
  ],
  "workflowStubs": [
    {{
      "name": "Send WhatsApp notification when deal closes",
      "trigger": {{
        "entity": "Deal",
        "event": "status_changed",
        "condition": "status == closed"
      }},
      "integration": "whatsapp",
      "action": "send_template_message",
      "payload": {{
        "phone": "Deal.contactPhone",
        "templateName": "deal_closed",
        "variables": {{
          "dealId": "Deal.id",
          "status": "Deal.status"
        }}
      }}
    }}
  ]
}}

STRICT RULES:
- pages MUST use keys: name, route, layout, boundEntity, components.
- apiEndpoints MUST use keys: path, method, handler, boundEntity, authRequired, rateLimit.
- rateLimit MUST be boolean true or false, NOT a number.
- authRules permissions MUST be objects, NOT strings.
- integrationHooks MUST use keys: integration, trigger, action.
- workflowStubs trigger MUST be an object with entity, event, condition.
- workflowStubs MUST include integration, action, payload.
- Valid integration IDs: slack, gmail, stripe, whatsapp, webhook.
- Valid actions:
  slack -> send_channel_message
  gmail -> send_email
  stripe -> create_customer
  whatsapp -> send_template_message
  webhook -> post_payload
- boundEntity values MUST match entity names from DataSchema exactly.
- workflow trigger entity MUST match entity names from DataSchema exactly.
- Do not use integrationId.
- Do not use callbackUrl.
- Do not use permissions as string arrays.
- Do not include explanations.
- Do not include markdown.
"""

    response = generate_response(
        prompt,
        stage_name="appspec_generation"
    )

    cleaned = clean_json_response(response)

    parsed = json.loads(cleaned)

    return AppSpec(**parsed)