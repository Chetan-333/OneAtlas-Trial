from agents.intent_agent import extract_intent
from agents.data_agent import generate_data_schema
from agents.appspec_agent import generate_appspec

from validators.intent_validator import validate_intent
from validators.data_schema_validator import validate_data_schema
from validators.appspec_validator import validate_appspec

from runtime.evaluation_logger import (
    start_timer,
    end_timer,
    create_stage_log
)


class PipelineEngine:
    def __init__(self, event_callback=None):
        self.events = []
        self.repair_logs = []
        self.evaluation_logs = []
        self.event_callback = event_callback

    def log_event(self, stage, status, data=None):
        event = {
            "stage": stage,
            "status": status,
            "data": data
        }

        self.events.append(event)

        if self.event_callback:
            self.event_callback(self.events)

    def log_evaluation(self, stage, provider, success, latency_ms, error=None):
        self.evaluation_logs.append(
            create_stage_log(
                stage=stage,
                provider=provider,
                success=success,
                latency_ms=latency_ms,
                error=error
            )
        )

    def run(self, prompt: str):
        self.events = []
        self.repair_logs = []
        self.evaluation_logs = []

        # Stage 1: Intent Extraction
        self.log_event("intent_extraction", "running")
        intent_timer = start_timer()

        try:
            intent = extract_intent(prompt)
            intent_latency = end_timer(intent_timer)
            intent_validation = validate_intent(intent)

            if not intent_validation["valid"]:
                self.log_evaluation(
                    "intent_extraction",
                    "groq",
                    False,
                    intent_latency,
                    intent_validation["errors"]
                )

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
                    "repair_logs": self.repair_logs,
                    "evaluation_logs": self.evaluation_logs
                }

            self.log_evaluation(
                "intent_extraction",
                "groq",
                True,
                intent_latency
            )

            self.log_event(
                "intent_extraction",
                "complete",
                intent.model_dump()
            )

        except Exception as error:
            intent_latency = end_timer(intent_timer)

            self.log_evaluation(
                "intent_extraction",
                "groq",
                False,
                intent_latency,
                str(error)
            )

            self.log_event(
                "intent_extraction",
                "failed",
                str(error)
            )

            return {
                "success": False,
                "failed_stage": "intent_extraction",
                "errors": str(error),
                "events": self.events,
                "repair_logs": self.repair_logs,
                "evaluation_logs": self.evaluation_logs
            }

        # Stage 2: Data Schema Generation
        self.log_event("data_schema_generation", "running")
        schema_timer = start_timer()

        try:
            data_schema = generate_data_schema(intent)
            schema_latency = end_timer(schema_timer)
            schema_validation = validate_data_schema(data_schema)

            if not schema_validation["valid"]:
                self.log_evaluation(
                    "data_schema_generation",
                    "groq",
                    False,
                    schema_latency,
                    schema_validation["errors"]
                )

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
                    "repair_logs": self.repair_logs,
                    "evaluation_logs": self.evaluation_logs
                }

            self.log_evaluation(
                "data_schema_generation",
                "groq",
                True,
                schema_latency
            )

            self.log_event(
                "data_schema_generation",
                "complete",
                data_schema.model_dump()
            )

        except Exception as error:
            schema_latency = end_timer(schema_timer)

            self.log_evaluation(
                "data_schema_generation",
                "groq",
                False,
                schema_latency,
                str(error)
            )

            self.log_event(
                "data_schema_generation",
                "failed",
                str(error)
            )

            return {
                "success": False,
                "failed_stage": "data_schema_generation",
                "errors": str(error),
                "events": self.events,
                "repair_logs": self.repair_logs,
                "evaluation_logs": self.evaluation_logs
            }

        # Stage 3: AppSpec Generation
        self.log_event("appspec_generation", "running")
        appspec_timer = start_timer()

        try:
            appspec = generate_appspec(intent, data_schema)
            appspec_latency = end_timer(appspec_timer)
            appspec_validation = validate_appspec(appspec)

            if not appspec_validation["valid"]:
                self.log_evaluation(
                    "appspec_generation",
                    "groq",
                    False,
                    appspec_latency,
                    appspec_validation["errors"]
                )

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
                    "repair_logs": self.repair_logs,
                    "evaluation_logs": self.evaluation_logs
                }

            self.log_evaluation(
                "appspec_generation",
                "groq",
                True,
                appspec_latency
            )

            self.log_event(
                "appspec_generation",
                "complete",
                appspec.model_dump()
            )

        except Exception as error:
            appspec_latency = end_timer(appspec_timer)

            self.log_evaluation(
                "appspec_generation",
                "groq",
                False,
                appspec_latency,
                str(error)
            )

            self.log_event(
                "appspec_generation",
                "failed",
                str(error)
            )

            return {
                "success": False,
                "failed_stage": "appspec_generation",
                "errors": str(error),
                "events": self.events,
                "repair_logs": self.repair_logs,
                "evaluation_logs": self.evaluation_logs
            }

        self.log_event("generation_complete", "complete")

        return {
            "success": True,
            "intent": intent.model_dump(),
            "data_schema": data_schema.model_dump(),
            "appspec": appspec.model_dump(),
            "events": self.events,
            "repair_logs": self.repair_logs,
            "evaluation_logs": self.evaluation_logs
        }