def validate_data_schema(data_schema):
    errors = []

    entity_names = []

    for entity in data_schema.entities:

        entity_names.append(entity.name)

        field_names = [field.name for field in entity.fields]

        # tenantId validation
        if "tenantId" not in field_names:
            errors.append({
                "stage": "data_schema",
                "error_type": "missing_tenant_id",
                "entity": entity.name,
                "message": f"{entity.name} missing tenantId field"
            })

        # empty fields
        if len(entity.fields) == 0:
            errors.append({
                "stage": "data_schema",
                "error_type": "empty_entity",
                "entity": entity.name,
                "message": f"{entity.name} has no fields"
            })

        # relation validation
        for relation in entity.relations:
            print(entity_names)
            print(relation.target)

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