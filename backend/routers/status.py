from fastapi import APIRouter, HTTPException
from job_store import get_job
from routers.job_view import serialize_job

router = APIRouter()


@router.get("/status/{job_id}")
async def status(job_id: str):
    job = get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return serialize_job(job)
