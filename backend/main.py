import asyncio
import os
import sys
from contextlib import asynccontextmanager

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables
load_dotenv()

from routers import upload, status, queue, download, stream
from queue_manager import worker, job_queue
from job_store import init_db, list_jobs
from model_loader import preload_models_async


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()

    # Re-enqueue any jobs that were "queued" when the server last shut down.
    # They are in the DB but not in the in-memory asyncio.Queue.
    for job in list_jobs():
        if job["status"] == "queued":
            await job_queue.put(job["job_id"])

    preload_task = asyncio.create_task(preload_models_async())
    worker_task = asyncio.create_task(worker())

    try:
        yield
    finally:
        for task in (preload_task, worker_task):
            task.cancel()
        for task in (preload_task, worker_task):
            try:
                await task
            except (asyncio.CancelledError, Exception):
                pass


app = FastAPI(title="Video Dubbing API", version="1.0.0", lifespan=lifespan)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload.router, prefix="/api", tags=["upload"])
app.include_router(status.router, prefix="/api", tags=["status"])
app.include_router(queue.router, prefix="/api", tags=["queue"])
app.include_router(download.router, prefix="/api", tags=["download"])
app.include_router(stream.router, prefix="/api", tags=["stream"])


@app.get("/")
async def root():
    return {"message": "Video Dubbing API", "version": "1.0.0"}


@app.get("/health")
async def health():
    from model_loader import models_ready
    return {"status": "healthy", "models_ready": models_ready.is_set()}


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")

    # On Windows, uvicorn's reload mode spawns a child process that re-imports
    # the app — which would re-trigger the multi-GB model preload on every save
    # and frequently crashes the reloader. Default to reload=off on Windows;
    # opt in with RELOAD=1 if you really want it.
    default_reload = sys.platform != "win32"
    reload = os.getenv("RELOAD", "1" if default_reload else "0") == "1"

    reload_kwargs = {}
    if reload:
        # Only watch our own source. Without this, watchfiles sees .venv
        # internals touched as modules get imported (pandas/whisperx/etc)
        # and reloads the server mid-startup, which kills model preload.
        here = os.path.dirname(os.path.abspath(__file__))
        reload_kwargs = {
            "reload_dirs": [here],
            "reload_excludes": [
                ".venv/*", "venv/*", "**/.venv/*", "**/site-packages/*",
                "uploads/*", "**/__pycache__/*", "*.pyc",
            ],
        }

    uvicorn.run("main:app", host=host, port=port, reload=reload, **reload_kwargs)
