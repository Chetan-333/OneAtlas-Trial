from repair.structural_repair import structural_repair
from repair.field_repair import field_repair
from repair.consistency_repair import consistency_repair


def repair_engine(
    error_type,
    data=None,
    missing_field=None,
    default_value=None,
    data_schema=None,
    appspec=None
):

    if error_type == "structural":
        return structural_repair(data)

    elif error_type == "field":
        return field_repair(
            data,
            missing_field,
            default_value
        )

    elif error_type == "consistency":
        return consistency_repair(
            data_schema,
            appspec
        )

    return {
        "status": "failed",
        "message": "Unknown repair strategy"
    }