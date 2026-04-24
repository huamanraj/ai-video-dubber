import sqlite3
import json
import threading
from datetime import datetime, timezone
from pathlib import Path
from contextlib import contextmanager
from typing import Optional

from config import UPLOAD_DIR

DB_PATH = UPLOAD_DIR / "jobs.db"

_local = threading.local()


def _get_db():
    if not hasattr(_local, "conn"):
        _local.conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
        _local.conn.row_factory = sqlite3.Row
    return _local.conn


@contextmanager
def get_cursor():
    conn = _get_db()
    cursor = conn.cursor()
    try:
        yield cursor
        conn.commit()
    except Exception:
        conn.rollback()
        raise


def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with get_cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                job_id TEXT PRIMARY KEY,
                filename TEXT NOT NULL,
                target_lang TEXT NOT NULL,
                voice_id TEXT,
                status TEXT NOT NULL DEFAULT 'queued',
                stage INTEGER DEFAULT 0,
                stage_name TEXT DEFAULT 'Waiting in queue',
                progress INTEGER DEFAULT 0,
                error TEXT,
                created_at TEXT NOT NULL,
                started_at TEXT,
                finished_at TEXT,
                queue_position INTEGER DEFAULT 0,
                extra_data TEXT DEFAULT '{}'
            )
        """)


def create_job(job_id: str, filename: str, target_lang: str, voice_id: str = None, **extra) -> dict:
    created_at = datetime.now(timezone.utc).isoformat()
    extra_json = json.dumps(extra)
    
    with get_cursor() as cursor:
        cursor.execute("""
            INSERT INTO jobs (job_id, filename, target_lang, voice_id, status, stage, 
                            stage_name, progress, created_at, extra_data)
            VALUES (?, ?, ?, ?, 'queued', 0, 'Waiting in queue', 0, ?, ?)
        """, (job_id, filename, target_lang, voice_id, created_at, extra_json))
    
    _recalc_positions()
    return get_job(job_id)


def update_job(job_id: str, **kwargs) -> Optional[dict]:
    if get_job(job_id) is None:
        return None
    
    set_clauses = []
    values = []
    
    for key, value in kwargs.items():
        if key == "extra_data":
            continue
        set_clauses.append(f"{key} = ?")
        values.append(value)
    
    if not set_clauses:
        return get_job(job_id)
    
    values.append(job_id)
    
    with get_cursor() as cursor:
        cursor.execute(f"""
            UPDATE jobs SET {', '.join(set_clauses)} WHERE job_id = ?
        """, values)
    
    _recalc_positions()
    return get_job(job_id)


def get_job(job_id: str) -> Optional[dict]:
    with get_cursor() as cursor:
        cursor.execute("SELECT * FROM jobs WHERE job_id = ?", (job_id,))
        row = cursor.fetchone()
    
    if row is None:
        return None
    
    return _row_to_job(row)


def list_jobs() -> list[dict]:
    with get_cursor() as cursor:
        cursor.execute("SELECT * FROM jobs ORDER BY created_at ASC")
        rows = cursor.fetchall()
    
    return [_row_to_job(row) for row in rows]


def clear_all_jobs() -> int:
    with get_cursor() as cursor:
        cursor.execute("DELETE FROM jobs")
        return cursor.rowcount


def remove_job(job_id: str) -> bool:
    with get_cursor() as cursor:
        cursor.execute("DELETE FROM jobs WHERE job_id = ?", (job_id,))
        affected = cursor.rowcount
    
    if affected > 0:
        _recalc_positions()
        return True
    return False


def _recalc_positions():
    with get_cursor() as cursor:
        cursor.execute("""
            SELECT job_id FROM jobs 
            WHERE status = 'queued' 
            ORDER BY created_at ASC
        """)
        queued_ids = [row[0] for row in cursor.fetchall()]
        
        cursor.execute("""
            SELECT job_id FROM jobs 
            WHERE status = 'processing' 
            ORDER BY created_at ASC
        """)
        processing_ids = [row[0] for row in cursor.fetchall()]
        
        for i, job_id in enumerate(processing_ids):
            cursor.execute("UPDATE jobs SET queue_position = 0 WHERE job_id = ?", (job_id,))
        
        for i, job_id in enumerate(queued_ids):
            position = i + 1 + len(processing_ids)
            cursor.execute("UPDATE jobs SET queue_position = ? WHERE job_id = ?", (position, job_id))
        
        cursor.execute("""
            UPDATE jobs SET queue_position = 0 
            WHERE status IN ('completed', 'failed')
        """)


def _row_to_job(row: sqlite3.Row) -> dict:
    job = dict(row)
    
    if job.get("extra_data"):
        try:
            extra = json.loads(job["extra_data"])
            job.update(extra)
        except (json.JSONDecodeError, TypeError):
            pass
    
    del job["extra_data"]
    return job
