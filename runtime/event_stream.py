import asyncio
from runtime.job_store import get_job


async def stream_job_events(job_id: str):

    while True:

        job = get_job(job_id)

        if not job:
            yield {
                "event": "error",
                "data": "Job not found"
            }
            break

        yield {
            "event": "progress",
            "data": str(job)
        }

        if job["status"] in ["completed", "failed"]:
            break

        await asyncio.sleep(1)