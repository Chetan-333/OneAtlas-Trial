def structural_repair(error_data):

    repaired_output = error_data.copy()

    # fill missing keys
    defaults = {
        "pages": [],
        "apiEndpoints": [],
        "workflowStubs": [],
        "integrationHooks": [],
        "authRules": []
    }

    for key, value in defaults.items():

        if key not in repaired_output:
            repaired_output[key] = value

    return {
        "strategy": "structural_repair",
        "status": "repaired",
        "output": repaired_output
    }