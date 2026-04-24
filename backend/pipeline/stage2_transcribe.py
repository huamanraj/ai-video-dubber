import json
import os
import subprocess
import tempfile

from config import SARVAM_API_KEY, SARVAM_SOURCE_LANGUAGE, SARVAM_STT_MODEL


def transcribe(audio_path: str) -> list[dict]:
    try:
        from sarvamai import SarvamAI
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "sarvamai SDK not installed. Run: uv add sarvamai"
        ) from exc

    if not SARVAM_API_KEY:
        raise RuntimeError("SARVAM_API_KEY is not set")

    client = SarvamAI(api_subscription_key=SARVAM_API_KEY)

    # with_timestamps is NOT a valid batch API param — diarization gives us
    # per-segment timestamps via diarized_transcript.entries which is reliable.
    job_kwargs: dict = {
        "model": SARVAM_STT_MODEL,
        "mode": "transcribe",
        "with_diarization": True,
    }
    if SARVAM_SOURCE_LANGUAGE and SARVAM_SOURCE_LANGUAGE.lower() != "unknown":
        job_kwargs["language_code"] = SARVAM_SOURCE_LANGUAGE

    job = client.speech_to_text_job.create_job(**job_kwargs)
    job.upload_files(file_paths=[audio_path])
    job.start()
    job.wait_until_complete()

    file_results = job.get_file_results()
    if file_results["failed"]:
        err = file_results["failed"][0].get("error_message", "unknown error")
        raise RuntimeError(f"Sarvam batch STT failed: {err}")

    with tempfile.TemporaryDirectory() as out_dir:
        job.download_outputs(output_dir=out_dir)
        json_files = [f for f in os.listdir(out_dir) if f.endswith(".json")]
        if not json_files:
            raise RuntimeError("Sarvam batch STT returned no output files")
        with open(os.path.join(out_dir, json_files[0]), encoding="utf-8") as f:
            data = json.load(f)

    return _parse(data, audio_path)


def _parse(data: dict, audio_path: str) -> list[dict]:
    # Prefer diarized_transcript.entries — most reliable per-segment timing
    entries = (data.get("diarized_transcript") or {}).get("entries") or []
    if entries:
        segments = [
            {
                "start": float(e["start_time_seconds"]),
                "end": float(e["end_time_seconds"]),
                "text": e["transcript"].strip(),
            }
            for e in entries
            if e.get("transcript", "").strip()
        ]
        if segments:
            return segments

    # Fall back to chunk-level timestamps array
    ts = data.get("timestamps") or {}
    chunks = ts.get("words") or []
    starts = ts.get("start_time_seconds") or []
    ends = ts.get("end_time_seconds") or []

    if chunks and starts and ends:
        segments = [
            {"start": float(s), "end": float(e), "text": t.strip()}
            for t, s, e in zip(chunks, starts, ends)
            if t.strip()
        ]
        if segments:
            return segments

    # Last resort: distribute the full transcript evenly across the audio duration
    text = data.get("transcript", "").strip()
    if not text:
        return []

    duration = _audio_duration(audio_path)
    words = text.split()
    # Split into ~10-word chunks spaced evenly across the duration
    chunk_size = 10
    word_chunks = [words[i:i + chunk_size] for i in range(0, len(words), chunk_size)]
    n = len(word_chunks)
    return [
        {
            "start": duration * i / n,
            "end": duration * (i + 1) / n,
            "text": " ".join(chunk),
        }
        for i, chunk in enumerate(word_chunks)
    ]


def _audio_duration(path: str) -> float:
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", path],
        capture_output=True, text=True, check=True,
    )
    return float(r.stdout.strip())
