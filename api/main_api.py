from fastapi import FastAPI
from pipeline.pipeline_engine import PipelineEngine

app = FastAPI()

pipeline_engine = PipelineEngine()


@app.get("/")
def home():
    return {
        "message": "OneAtlas AI Pipeline Running"
    }


@app.post("/api/generate")
def generate_app(payload: dict):

    prompt = payload.get("prompt")

    result = pipeline_engine.run(prompt)

    return result