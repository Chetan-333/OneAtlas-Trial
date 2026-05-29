import uuid


JOB_STORE = {}


def create_job():
    job_id = str(uuid.uuid4())

    JOB_STORE[job_id] = {
        "status": "created",
        "events": [],
        "result": None,
        "errors": None
    }

    return job_id


def update_job(
    job_id,
    status=None,
    events=None,
    result=None,
    errors=None
):

    if job_id not in JOB_STORE:
        return

    if status:
        JOB_STORE[job_id]["status"] = status

    if events:
        JOB_STORE[job_id]["events"] = events

    if result:
        JOB_STORE[job_id]["result"] = result

    if errors:
        JOB_STORE[job_id]["errors"] = errors


def get_job(job_id):
    return JOB_STORE.get(job_id)