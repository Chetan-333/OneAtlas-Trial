from fastapi import FastAPI
from pipeline.pipeline_engine import PipelineEngine
from sse_starlette.sse import EventSourceResponse
from runtime.event_stream import stream_job_events

from runtime.job_store import (
    create_job,
    update_job,
    get_job
)

app = FastAPI()


def create_event_callback(job_id):

    def callback(events):

        job = get_job(job_id)

        if not job:
            return

        update_job(
            job_id,
            events=events
        )

    return callback





@app.get("/")
def home():
    return {
        "message": "OneAtlas AI Pipeline Running"
    }


@app.post("/api/generate")
def generate_app(payload: dict):

    prompt = payload.get("prompt")

    job_id = create_job()
    pipeline_engine = PipelineEngine(
    event_callback=create_event_callback(job_id)
)

    update_job(
        job_id,
        status="running"
    )

    try:
        result = pipeline_engine.run(prompt)

        update_job(
            job_id,
            status="completed",
            events=result.get("events"),
            result=result
        )

    except Exception as error:

        update_job(
            job_id,
            status="failed",
            errors=str(error)
        )

    return {
        "jobId": job_id,
        "status": get_job(job_id)["status"]
    }


@app.get("/api/generate/{job_id}")
def get_generation_job(job_id: str):

    job = get_job(job_id)

    if not job:
        return {
            "error": "Job not found"
        }

    return job


@app.get("/api/generate/{job_id}/stream")
async def stream_generation(job_id: str):

    return EventSourceResponse(
        stream_job_events(job_id)
    )

