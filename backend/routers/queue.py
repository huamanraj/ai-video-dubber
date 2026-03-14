from fastapi import APIRouter, HTTPException

from job_store import list_jobs, get_job, remove_job
from routers.job_view import serialize_job

router = APIRouter()


@router.get("/queue")
async def queue_list():
    return [serialize_job(job) for job in list_jobs()]


@router.delete("/queue/{job_id}")
async def cancel_job(job_id: str):
    job = get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    if job["status"] == "processing":
        raise HTTPException(status_code=400, detail="Cannot cancel a job in progress")
    if job["status"] in ("done", "failed"):
        remove_job(job_id)
        return {"detail": "Job removed"}
    # status == "queued"
    remove_job(job_id)
    return {"detail": "Job cancelled"}
