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
        atempo = max(0.5, min(2.0, atempo))

        stretched_path = os.path.join(stretched_dir, f"stretched_{i}.wav")
        subprocess.run(
            [
                "ffmpeg", "-y", "-i", clip_path,
                "-filter:a", f"atempo={atempo:.4f}",
                stretched_path,
            ],
            check=True,
            capture_output=True,
        )
        stretched_paths.append(stretched_path)

    return stretched_paths
