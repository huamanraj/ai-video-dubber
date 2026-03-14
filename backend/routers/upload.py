import uuid
from fastapi import APIRouter, UploadFile, File, Form, HTTPException

from config import UPLOAD_DIR, LANGUAGE_MAP, SARVAM_VOICES
from job_store import create_job, get_job
from queue_manager import job_queue, notify_update

router = APIRouter()


@router.post("/dub")
async def dub(
    video: UploadFile = File(...),
    target_language: str = Form(...),
    voice_id: str = Form(None),  # Optional voice selection
):
    if target_language not in LANGUAGE_MAP:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported language '{target_language}'. Supported: {list(LANGUAGE_MAP.keys())}",
        )

    # Validate voice_id if provided
    if voice_id and target_language in SARVAM_VOICES:
        if voice_id not in SARVAM_VOICES[target_language]:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid voice '{voice_id}' for language '{target_language}'. Available: {SARVAM_VOICES[target_language]}",
            )

    job_id = uuid.uuid4().hex
    job_dir = UPLOAD_DIR / job_id
    job_dir.mkdir(parents=True, exist_ok=True)

    video_path = job_dir / "input.mp4"
    with open(video_path, "wb") as f:
        f.write(await video.read())

    job = create_job(job_id, video.filename or "input.mp4", target_language, voice_id=voice_id)
    
    await job_queue.put(job_id)
    notify_update()

    return {"job_id": job_id, "queue_position": job["queue_position"]}
