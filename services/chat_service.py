from rq.decorators import job

from client.rq_client import queue
from queues.worker import process_query
def enqueue_chat_job(query: str):

    job = queue.enqueue(
        process_query,
        query
    )

    return {
        "status": "queued",
        "job_id": job.id
    }


def get_job_result(job_id: str):

    job = queue.fetch_job(job_id)

    if job is None:
        return {"status": "not_found", "result": None}

    status = job.get_status()
    return {
        "status": str(status),
        "result": job.return_value() if status == "finished" else None
    }