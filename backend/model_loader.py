import asyncio

# Stage 2 now uses Sarvam cloud STT — no local GPU models to preload.
# The event is set immediately so the pipeline never waits.
models_ready: asyncio.Event = asyncio.Event()


async def preload_models_async() -> None:
    models_ready.set()
