import asyncio
import os
import subprocess
import traceback
from datetime import datetime, timezone

from config import UPLOAD_DIR, LANGUAGE_MAP, STAGE_NAMES, INDIAN_LANGUAGES
from job_store import update_job, get_job
from queue_manager import notify_update
from model_loader import models_ready

from pipeline.stage1_extract import extract_audio
from pipeline.stage2_transcribe import transcribe
from pipeline.stage3_translate import translate_segments
from pipeline.stage4_tts import generate_tts_clips
from pipeline.stage4_tts_indic import generate_tts_clips_indic
from pipeline.stage5_stretch import time_stretch_clips
from pipeline.stage6_timeline import build_audio_timeline
from pipeline.stage7_mux import mux_video


def _run_in_thread(func, *args):
    return asyncio.to_thread(func, *args)


def _get_duration_ms(file_path: str) -> int:
    result = subprocess.run(
        [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            file_path,
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return int(float(result.stdout.strip()) * 1000)


def _begin_stage(job_id: str, stage: int):
    progress = int((stage - 1) * 100 / 7)
    update_job(job_id, stage=stage, stage_name=STAGE_NAMES[stage], progress=progress)
    notify_update()


def _end_stage(job_id: str, stage: int):
    progress = int(stage * 100 / 7)
    update_job(job_id, progress=progress)
    notify_update()


async def run_pipeline(job_id: str):
    job = get_job(job_id)
    if job is None:
        return

    # Wait for background model preload to finish before touching GPU.
    # If preload is still in flight, the job sits as "processing" briefly;
    # if preload already finished, this returns immediately.
    if not models_ready.is_set():
        update_job(job_id, stage_name="Waiting for models to load")
        notify_update()
        await models_ready.wait()

    job_dir = str(UPLOAD_DIR / job_id)
    video_path = os.path.join(job_dir, "input.mp4")
    target_lang = job["target_lang"]
    nllb_code = LANGUAGE_MAP[target_lang]

    update_job(
        job_id,
        status="processing",
        started_at=datetime.now(timezone.utc).isoformat(),
    )
    notify_update()

    try:
        # Stage 1
        _begin_stage(job_id, 1)
        audio_path = await _run_in_thread(extract_audio, video_path, os.path.join(job_dir, "audio.wav"))
        total_duration_ms = _get_duration_ms(audio_path)
        _end_stage(job_id, 1)

        # Stage 2
        _begin_stage(job_id, 2)
        segments = await _run_in_thread(transcribe, audio_path)
        _end_stage(job_id, 2)

        # Stage 3
        _begin_stage(job_id, 3)
        segments = await _run_in_thread(translate_segments, segments, nllb_code)
        _end_stage(job_id, 3)

        # Stage 4 — route to Indic or standard TTS with voice selection
        _begin_stage(job_id, 4)
        voice_id = job.get("voice_id")
        if target_lang in INDIAN_LANGUAGES:
            clip_paths = await _run_in_thread(
                generate_tts_clips_indic,
                segments, audio_path, job_dir, target_lang, voice_id
            )
        else:
            clip_paths = await _run_in_thread(
                generate_tts_clips,
                segments, audio_path, job_dir, target_lang, voice_id or "en_female_1"
            )
        _end_stage(job_id, 4)

        # Stage 5
        _begin_stage(job_id, 5)
        stretched_paths = await _run_in_thread(time_stretch_clips, segments, clip_paths, job_dir)
        _end_stage(job_id, 5)

        # Stage 6
        _begin_stage(job_id, 6)
        dubbed_audio = await _run_in_thread(
            build_audio_timeline,
            segments, stretched_paths, total_duration_ms, job_dir
        )
        _end_stage(job_id, 6)

        # Stage 7
        _begin_stage(job_id, 7)
        output_path = os.path.join(job_dir, "output.mp4")
        await _run_in_thread(mux_video, video_path, dubbed_audio, output_path)
        if not os.path.exists(output_path) or os.path.getsize(output_path) == 0:
            raise RuntimeError(
                "Processing error: ffmpeg completed but output.mp4 is missing or empty."
            )
        _end_stage(job_id, 7)

        update_job(
            job_id,
            status="completed",
            stage_name="Complete",
            finished_at=datetime.now(timezone.utc).isoformat(),
        )
        notify_update()

    except Exception as e:
        update_job(
            job_id,
            status="failed",
            error=f"{e}\n{traceback.format_exc()}",
            finished_at=datetime.now(timezone.utc).isoformat(),
        )
        notify_update()
