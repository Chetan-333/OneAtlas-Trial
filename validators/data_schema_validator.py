def validate_data_schema(data_schema):
    errors = []

    # collect all entity names first
    entity_names = [entity.name for entity in data_schema.entities]

    for entity in data_schema.entities:

        field_names = [field.name for field in entity.fields]

        if "tenantId" not in field_names:
            errors.append({
                "stage": "data_schema",
                "error_type": "missing_tenant_id",
                "entity": entity.name,
                "message": f"{entity.name} missing tenantId field"
            })

        if len(entity.fields) == 0:
            errors.append({
                "stage": "data_schema",
                "error_type": "empty_entity",
                "entity": entity.name,
                "message": f"{entity.name} has no fields"
            })

        for relation in entity.relations:
            if relation.target not in entity_names:
                errors.append({
                    "stage": "data_schema",
                    "error_type": "invalid_relation",
                    "entity": entity.name,
                    "message": f"Invalid relation target: {relation.target}"
                })

    return {
        "valid": len(errors) == 0,
        "errors": errors
    }