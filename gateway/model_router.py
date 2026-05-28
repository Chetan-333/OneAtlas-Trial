import json
import os


def load_routing_config():
    config_path = os.path.join("config", "routing.json")

    with open(config_path, "r", encoding="utf-8") as file:
        return json.load(file)


def get_model_for_stage(stage_name: str):
    config = load_routing_config()

    if stage_name not in config:
        raise ValueError(f"No routing config found for stage: {stage_name}")

    return config[stage_name]


def log_model_selection(stage_name: str):
    model_config = get_model_for_stage(stage_name)

    return {
        "stage": stage_name,
        "primary_provider": model_config["primary"],
        "fallback_provider": model_config["fallback"],
        "model": model_config["model"]
    }