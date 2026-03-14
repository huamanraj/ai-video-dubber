import os
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio

# Load environment variables
load_dotenv()

from routers import upload, status, queue, download, stream
from queue_manager import worker

app = FastAPI(title="Video Dubbing API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
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
    return {"status": "healthy"}


@app.on_event("startup")
async def startup_event():
    # Start the background worker
    asyncio.create_task(worker())


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    uvicorn.run("main:app", host=host, port=port, reload=True)