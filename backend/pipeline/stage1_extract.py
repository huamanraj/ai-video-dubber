import subprocess


def extract_audio(video_path: str, output_path: str) -> str:
    subprocess.run(
        [
            "ffmpeg", "-y", "-i", video_path,
            "-vn", "-ac", "1", "-ar", "16000", "-acodec", "pcm_s16le",
            output_path,
        ],
        check=True,
        capture_output=True,
    )
    return output_path
