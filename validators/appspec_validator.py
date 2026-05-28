from integrations.integration_registry import (
    is_valid_integration,
    is_valid_action
)


def validate_appspec(appspec):

    errors = []

    # pages validation
    if len(appspec.pages) == 0:
        errors.append({
            "stage": "appspec",
            "error_type": "missing_pages",
            "message": "No pages generated"
        })

    # api validation
    if len(appspec.apiEndpoints) == 0:
        errors.append({
            "stage": "appspec",
            "error_type": "missing_api",
            "message": "No API endpoints generated"
        })

    # workflow validation
    for workflow in appspec.workflowStubs:

        if not workflow.integration:
            errors.append({
                "stage": "appspec",
                "error_type": "missing_integration",
                "workflow": workflow.name,
                "message": "Workflow missing integration"
            })

    # integration hook validation
    for hook in appspec.integrationHooks:

        if not is_valid_integration(hook.integration):
            errors.append({
                "stage": "appspec",
                "error_type": "invalid_integration",
                "integration": hook.integration,
                "message": f"Invalid integration: {hook.integration}"
            })

        if not is_valid_action(hook.integration, hook.action):
            errors.append({
                "stage": "appspec",
                "error_type": "invalid_action",
                "integration": hook.integration,
                "action": hook.action,
                "message": f"Invalid action: {hook.action}"
            })

    # workflow action validation
    for workflow in appspec.workflowStubs:

        if not is_valid_integration(workflow.integration):
            errors.append({
                "stage": "appspec",
                "error_type": "invalid_workflow_integration",
                "integration": workflow.integration,
                "message": f"Invalid workflow integration: {workflow.integration}"
            })

        if not is_valid_action(workflow.integration, workflow.action):
            errors.append({
                "stage": "appspec",
                "error_type": "invalid_workflow_action",
                "action": workflow.action,
                "message": f"Invalid workflow action: {workflow.action}"
            })

    return {
        "valid": len(errors) == 0,
        "errors": errors
    }