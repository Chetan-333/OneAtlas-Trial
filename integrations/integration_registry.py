INTEGRATION_REGISTRY = [
    {
        "id": "slack",
        "displayName": "Slack",
        "authType": "oauth2",
        "triggers": ["record_created", "record_updated", "status_changed"],
        "actions": [
            {
                "id": "send_channel_message",
                "description": "Send message to Slack channel",
                "inputSchema": {
                    "channel": "string",
                    "message": "string"
                },
                "outputSchema": {
                    "messageId": "string"
                }
            }
        ]
    },
    {
        "id": "gmail",
        "displayName": "Gmail",
        "authType": "oauth2",
        "triggers": ["record_created", "status_changed"],
        "actions": [
            {
                "id": "send_email",
                "description": "Send email notification",
                "inputSchema": {
                    "to": "string",
                    "subject": "string",
                    "body": "string"
                },
                "outputSchema": {
                    "emailId": "string"
                }
            }
        ]
    },
    {
        "id": "stripe",
        "displayName": "Stripe",
        "authType": "api_key",
        "triggers": ["payment_created", "subscription_updated"],
        "actions": [
            {
                "id": "create_customer",
                "description": "Create Stripe customer",
                "inputSchema": {
                    "email": "string",
                    "name": "string"
                },
                "outputSchema": {
                    "customerId": "string"
                }
            }
        ]
    },
    {
        "id": "whatsapp",
        "displayName": "WhatsApp",
        "authType": "api_key",
        "triggers": ["record_created", "status_changed"],
        "actions": [
            {
                "id": "send_template_message",
                "description": "Send WhatsApp template message",
                "inputSchema": {
                    "phone": "string",
                    "templateName": "string",
                    "variables": "object"
                },
                "outputSchema": {
                    "messageId": "string"
                }
            }
        ]
    },
    {
        "id": "webhook",
        "displayName": "Generic Webhook",
        "authType": "webhook_secret",
        "triggers": ["record_created", "record_updated", "status_changed"],
        "actions": [
            {
                "id": "post_payload",
                "description": "Send structured payload to webhook URL",
                "inputSchema": {
                    "url": "string",
                    "payload": "object",
                    "signature": "string"
                },
                "outputSchema": {
                    "status": "string"
                }
            }
        ]
    }
]


def get_integration_registry():
    return INTEGRATION_REGISTRY


def get_integration_ids():
    return [integration["id"] for integration in INTEGRATION_REGISTRY]


def is_valid_integration(integration_id: str):
    return integration_id in get_integration_ids()


def is_valid_action(integration_id: str, action_id: str):
    for integration in INTEGRATION_REGISTRY:
        if integration["id"] == integration_id:
            return any(action["id"] == action_id for action in integration["actions"])

    return False