from pathlib import Path
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from job_store import get_job
from routers.job_view import output_path_for, reconcile_output_state

router = APIRouter()


@router.get("/download/{job_id}")
async def download(job_id: str):
    job = get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    job = reconcile_output_state(job)

    if job["status"] == "queued" or job["status"] == "processing":
        raise HTTPException(status_code=409, detail="Job still processing")

    if job["status"] == "failed":
        detail = job.get("error") or "Processing error"
        raise HTTPException(status_code=400, detail=detail)

    output_path = output_path_for(job_id)
    if not output_path.exists() or output_path.stat().st_size == 0:
        raise HTTPException(
            status_code=409,
            detail="Processing error: output file is not available",
        )

    original = Path(job.get("filename", "video.mp4"))
    dubbed_name = f"{original.stem}_dubbed{original.suffix}"

    return FileResponse(
        str(output_path),
        media_type="video/mp4",
        filename=dubbed_name,
    )


@router.get("/original/{job_id}")
async def original(job_id: str):
    job = get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    from config import UPLOAD_DIR
    input_path = UPLOAD_DIR / job_id / "input.mp4"
    if not input_path.exists():
        raise HTTPException(status_code=404, detail="Original file not found")

    original_name = Path(job.get("filename", "input.mp4"))
    return FileResponse(str(input_path), media_type="video/mp4", filename=original_name.name)
