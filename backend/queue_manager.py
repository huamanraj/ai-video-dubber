import asyncio
import logging

logger = logging.getLogger(__name__)

job_queue: asyncio.Queue[str] = asyncio.Queue()
gpu_lock = asyncio.Lock()

# Event that fires on every job state change so SSE can push updates
job_updated_event = asyncio.Event()


def notify_update():
    """Signal SSE listeners that job state has changed."""
    job_updated_event.set()


async def worker():
    """Background worker: pulls job_ids from queue, runs pipeline one at a time."""
    from pipeline.runner import run_pipeline  # deferred to avoid circular imports

    logger.info("Queue worker started")
    while True:
        job_id = await job_queue.get()
        try:
            async with gpu_lock:
                await run_pipeline(job_id)
        except Exception:
            logger.exception("Unhandled error in worker for job %s", job_id)
        finally:
            job_queue.task_done()
