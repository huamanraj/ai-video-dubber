import os


def build_audio_timeline(
    segments: list[dict],
    stretched_paths: list[str],
    total_duration_ms: int,
    output_dir: str,
) -> str:
    from pydub import AudioSegment

    dubbed_audio = AudioSegment.silent(duration=total_duration_ms)

    for seg, clip_path in zip(segments, stretched_paths):
        clip = AudioSegment.from_wav(clip_path)
        position_ms = int(seg["start"] * 1000)
        dubbed_audio = dubbed_audio.overlay(clip, position=position_ms)

    output_path = os.path.join(output_dir, "dubbed_audio.wav")
    dubbed_audio.export(output_path, format="wav")
    return output_path
