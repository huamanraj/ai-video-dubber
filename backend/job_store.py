from datetime import datetime, timezone

jobs: dict[str, dict] = {}


def create_job(job_id: str, filename: str, target_lang: str, voice_id: str = None, **extra) -> dict:
    job = {
        "job_id": job_id,
        "filename": filename,
        "target_lang": target_lang,
        "voice_id": voice_id,
        "status": "queued",
        "stage": 0,
        "stage_name": "Waiting in queue",
        "progress": 0,
        "error": None,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "started_at": None,
        "finished_at": None,
        "queue_position": 0,
        **extra,
    }
    jobs[job_id] = job
    _recalc_positions()
    return job


def update_job(job_id: str, **kwargs) -> dict | None:
    if job_id not in jobs:
        return None
    jobs[job_id].update(kwargs)
    _recalc_positions()
    return jobs[job_id]


def get_job(job_id: str) -> dict | None:
    return jobs.get(job_id)


def list_jobs() -> list[dict]:
    return sorted(jobs.values(), key=lambda j: j["created_at"])


def remove_job(job_id: str) -> bool:
    if job_id in jobs:
        del jobs[job_id]
        _recalc_positions()
        return True
    return False


def _recalc_positions():
    queued = [
        j for j in jobs.values() if j["status"] == "queued"
    ]
    queued.sort(key=lambda j: j["created_at"])

    processing = [j for j in jobs.values() if j["status"] == "processing"]
    for j in processing:
        j["queue_position"] = 0

    for i, j in enumerate(queued):
        j["queue_position"] = i + 1 + len(processing)

    for j in jobs.values():
        if j["status"] in ("completed", "failed"):
            j["queue_position"] = 0
