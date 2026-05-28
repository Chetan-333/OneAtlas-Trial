def validate_intent(intent):
    errors = []

    if not intent.appName:
        errors.append({
            "stage": "intent_extraction",
            "error_type": "missing_field",
            "field": "appName",
            "message": "appName is required"
        })

    if not intent.features:
        errors.append({
            "stage": "intent_extraction",
            "error_type": "missing_field",
            "field": "features",
            "message": "At least one feature is required"
        })

    if not intent.entities:
        errors.append({
            "stage": "intent_extraction",
            "error_type": "missing_field",
            "field": "entities",
            "message": "At least one entity is required"
        })

    return {
        "valid": len(errors) == 0,
        "errors": errors
    }