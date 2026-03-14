import os
from datetime import datetime, timezone

from config import UPLOAD_DIR
from job_store import update_job


def output_path_for(job_id: str):
    return UPLOAD_DIR / job_id / "output.mp4"


def _is_valid_output_file(job_id: str) -> bool:
    output_path = output_path_for(job_id)
    return output_path.exists() and output_path.stat().st_size > 0


def reconcile_output_state(job: dict) -> dict:
    """Downgrade stale done jobs when output file is missing/empty."""
    if job.get("status") != "done":
        return job

    job_id = job["job_id"]
    if _is_valid_output_file(job_id):
        return job

    message = "Processing error: final video output is missing or empty."
    updated = update_job(
        job_id,
        status="failed",
        stage_name="Output missing",
        error=message,
        finished_at=datetime.now(timezone.utc).isoformat(),
    )
    return updated or job


def serialize_job(job: dict) -> dict:
    reconciled = reconcile_output_state(job)
    job_id = reconciled["job_id"]
    can_download = reconciled.get("status") == "done" and _is_valid_output_file(job_id)

    payload = dict(reconciled)
    payload["can_download"] = can_download
    payload["download_url"] = f"/download/{job_id}" if can_download else None
    return payload