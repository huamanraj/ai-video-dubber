import torch
from fastapi import APIRouter

from queue_manager import job_queue

router = APIRouter()


@router.get("/health")
async def health():
    vram_free = 0.0
    if torch.cuda.is_available():
        vram_free = torch.cuda.mem_get_info()[0] / 1024**2

    return {
        "status": "ok",
        "gpu_vram_free_mb": round(vram_free, 1),
        "jobs_in_queue": job_queue.qsize(),
    }
