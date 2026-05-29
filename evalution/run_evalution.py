import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

from pipeline.pipeline_engine import PipelineEngine
import json

engine = PipelineEngine()

with open("evalution/prompts.json", "r") as f:
    prompts = json.load(f)

results = []

for idx, prompt in enumerate(prompts):

    result = engine.run(prompt)

    results.append({
    "prompt_id": idx + 1,
    "prompt": prompt,
    "success": result["success"],
    "failed_stage": result.get("failed_stage"),
    "errors": result.get("errors", [])
})

with open("evalution/results.json", "w") as f:
    json.dump(results, f, indent=2)