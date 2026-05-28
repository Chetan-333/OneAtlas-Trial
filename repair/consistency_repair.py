def consistency_repair(data_schema, appspec):
    repair_log = []

    entity_names = [entity.name for entity in data_schema.entities]

    # Repair pages with invalid boundEntity
    for page in appspec.pages:
        if page.boundEntity not in entity_names:
            old_entity = page.boundEntity
            page.boundEntity = entity_names[0] if entity_names else "Unknown"

            repair_log.append({
                "strategy": "consistency_repair",
                "type": "invalid_page_entity",
                "old": old_entity,
                "new": page.boundEntity,
                "status": "repaired"
            })

    # Repair API endpoints with invalid boundEntity
    for endpoint in appspec.apiEndpoints:
        if endpoint.boundEntity not in entity_names:
            old_entity = endpoint.boundEntity
            endpoint.boundEntity = entity_names[0] if entity_names else "Unknown"

            repair_log.append({
                "strategy": "consistency_repair",
                "type": "invalid_api_entity",
                "old": old_entity,
                "new": endpoint.boundEntity,
                "status": "repaired"
            })

    # Repair workflow stubs with invalid trigger entity
    for workflow in appspec.workflowStubs:
        if workflow.trigger.entity not in entity_names:
            old_entity = workflow.trigger.entity
            workflow.trigger.entity = entity_names[0] if entity_names else "Unknown"

            repair_log.append({
                "strategy": "consistency_repair",
                "type": "invalid_workflow_entity",
                "old": old_entity,
                "new": workflow.trigger.entity,
                "status": "repaired"
            })

    return {
        "status": "repaired" if repair_log else "no_repair_needed",
        "appspec": appspec,
        "repair_log": repair_log
    }