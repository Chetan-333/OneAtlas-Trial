from agents.intent_agent import extract_intent
from agents.data_agent import generate_data_schema
from agents.appspec_agent import generate_appspec

from validators.intent_validator import validate_intent
from validators.data_schema_validator import validate_data_schema
from validators.appspec_validator import validate_appspec


class PipelineEngine:
    def __init__(self):
        self.events = []
        self.repair_logs = []

    def log_event(self, stage, status, data=None):
        event = {
            "stage": stage,
            "status": status,
            "data": data
        }

        self.events.append(event)

    def run(self, prompt: str):

        # Stage 1: Intent Extraction
        self.log_event("intent_extraction", "running")

        intent = extract_intent(prompt)
        intent_validation = validate_intent(intent)

        if not intent_validation["valid"]:
            self.log_event(
                "intent_extraction",
                "failed",
                intent_validation["errors"]
            )

            return {
                "success": False,
                "failed_stage": "intent_extraction",
                "errors": intent_validation["errors"],
                "events": self.events,
                "repair_logs": self.repair_logs
            }

        self.log_event(
            "intent_extraction",
            "complete",
            intent.model_dump()
        )

        # Stage 2: Data Schema Generation
        self.log_event("data_schema_generation", "running")

        data_schema = generate_data_schema(intent)
        schema_validation = validate_data_schema(data_schema)

        if not schema_validation["valid"]:
            self.log_event(
                "data_schema_generation",
                "failed",
                schema_validation["errors"]
            )

            return {
                "success": False,
                "failed_stage": "data_schema_generation",
                "errors": schema_validation["errors"],
                "events": self.events,
                "repair_logs": self.repair_logs
            }

        self.log_event(
            "data_schema_generation",
            "complete",
            data_schema.model_dump()
        )

        # Stage 3: AppSpec Generation
        self.log_event("appspec_generation", "running")

        appspec = generate_appspec(intent, data_schema)
        appspec_validation = validate_appspec(appspec)

        if not appspec_validation["valid"]:
            self.log_event(
                "appspec_generation",
                "failed",
                appspec_validation["errors"]
            )

            return {
                "success": False,
                "failed_stage": "appspec_generation",
                "errors": appspec_validation["errors"],
                "events": self.events,
                "repair_logs": self.repair_logs
            }

        self.log_event(
            "appspec_generation",
            "complete",
            appspec.model_dump()
        )

        self.log_event("generation_complete", "complete")

        return {
            "success": True,
            "intent": intent,
            "data_schema": data_schema,
            "appspec": appspec,
            "events": self.events,
            "repair_logs": self.repair_logs
        }