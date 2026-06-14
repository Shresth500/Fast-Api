from fastapi import APIRouter, Query
from services.chat_service import (
    enqueue_chat_job,
    get_job_result
)

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

@router.post("/")
def chat(
    query: str = Query(
        ...,
        description="The chat query of user"
    )
):
    return enqueue_chat_job(query)


@router.get("/status")
def job_status(
    job_id: str = Query(
        ...,
        description="Job Id"
    )
):
    return get_job_result(job_id)