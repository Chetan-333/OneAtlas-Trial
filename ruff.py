from agents.intent_agent import extract_intent
from agents.design_agent import generate_design

from agents.schema_agent import (
    generate_database_schema,
    generate_api_schema,
    generate_ui_schema,
    generate_auth_schema
)

user_input = """
Build a CRM with login, contacts, dashboard,
role-based access, and premium plan with payments.
Admins can see analytics.
"""

# Stage 1
intent = extract_intent(user_input)

print("\n===== INTENT =====")
print(intent)

# Stage 2
design = generate_design(intent)

print("\n===== DESIGN =====")
print(design)

# Stage 3
db_schema = generate_database_schema(intent, design)

print("\n===== DATABASE SCHEMA =====")
print(db_schema)

# Stage 4
api_schema = generate_api_schema(intent, design)

print("\n===== API SCHEMA =====")
print(api_schema)

# Stage 5
ui_schema = generate_ui_schema(intent, design)

print("\n===== UI SCHEMA =====")
print(ui_schema)

# Stage 6
auth_schema = generate_auth_schema(intent, design)

print("\n===== AUTH SCHEMA =====")
print(auth_schema)

from agents.validator_agent import validate_system

validation_result = validate_system(
    db_schema,
    api_schema,
    ui_schema,
    auth_schema
)

print("\n===== VALIDATION =====")
print(validation_result)


from agents.runtime_agent import generate_application


generated_app = generate_application(
    app_name=intent.app_name.replace(" ", "_"),
    db_schema=db_schema,
    api_schema=api_schema,
    ui_schema=ui_schema,
    auth_schema=auth_schema
)

print("\n===== GENERATED APP =====")
print(generated_app)

validation = validate_system(db_schema, api_schema, ui_schema, auth_schema)

if validation["status"] == "failed":

    print("Repairing API schema...")

    from agents.repair_agent import repair_api_schema

    api_schema = repair_api_schema(
        validation["issues"],
        intent,
        design,
        api_schema
    )