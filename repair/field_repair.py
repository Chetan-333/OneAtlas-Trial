def field_repair(data, missing_field, default_value=None):

    repaired_data = data.copy()

    repaired_data[missing_field] = default_value

    return {
        "strategy": "field_repair",
        "status": "repaired",
        "field": missing_field,
        "output": repaired_data
    }
