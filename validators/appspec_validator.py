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

    return {
        "valid": len(errors) == 0,
        "errors": errors
    }