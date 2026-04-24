import os
import subprocess


def time_stretch_clips(
    segments: list[dict], clip_paths: list[str], output_dir: str
) -> list[str]:
    from pydub import AudioSegment

    stretched_dir = os.path.join(output_dir, "clips")
    os.makedirs(stretched_dir, exist_ok=True)

    stretched_paths = []
    for i, (seg, clip_path) in enumerate(zip(segments, clip_paths)):
        original_duration = seg["end"] - seg["start"]
        if original_duration <= 0:
            stretched_paths.append(clip_path)
            continue

        tts_audio = AudioSegment.from_wav(clip_path)
        tts_duration = len(tts_audio) / 1000.0
        if tts_duration <= 0:
            stretched_paths.append(clip_path)
            continue

        atempo = tts_duration / original_duration

        # Only stretch if meaningfully different (>5%) — avoids re-encoding for tiny diffs
        if abs(atempo - 1.0) < 0.05:
            stretched_paths.append(clip_path)
            continue

        stretched_path = os.path.join(stretched_dir, f"stretched_{i}.wav")
        subprocess.run(
            [
                "ffmpeg", "-y", "-i", clip_path,
                "-filter:a", _atempo_filter(atempo),
                stretched_path,
            ],
            check=True,
            capture_output=True,
        )
        stretched_paths.append(stretched_path)

    return stretched_paths


def _atempo_filter(atempo: float) -> str:
    """Build a chained atempo filter that handles values outside ffmpeg's [0.5, 2.0] limit."""
    # Hard cap: beyond 4x speed-up or 4x slow-down sounds terrible anyway
    atempo = max(0.25, min(4.0, atempo))

    filters = []
    remaining = atempo
    while remaining > 2.0:
        filters.append("atempo=2.0")
        remaining /= 2.0
    while remaining < 0.5:
        filters.append("atempo=0.5")
        remaining /= 0.5
    filters.append(f"atempo={remaining:.4f}")
    return ",".join(filters)
