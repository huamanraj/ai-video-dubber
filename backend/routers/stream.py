import asyncio
import json
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from job_store import get_job
from queue_manager import job_updated_event

router = APIRouter()


@router.get("/stream/{job_id}")
async def stream(job_id: str):
    job = get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    async def event_generator():
        last_sent = None
        while True:
            current = get_job(job_id)
            if current is None:
                break

            snapshot = json.dumps(current, default=str)
            if snapshot != last_sent:
                yield f"data: {snapshot}\n\n"
                last_sent = snapshot

            if current["status"] in ("done", "failed"):
                break

            # Wait for signal or timeout after 0.5s
            job_updated_event.clear()
            try:
                await asyncio.wait_for(job_updated_event.wait(), timeout=0.5)
            except asyncio.TimeoutError:
                pass

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )
