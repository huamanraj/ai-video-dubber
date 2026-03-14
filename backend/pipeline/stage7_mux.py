import subprocess


def mux_video(original_video: str, dubbed_audio: str, output_path: str) -> str:
    subprocess.run(
        [
            "ffmpeg", "-y",
            "-i", original_video,
            "-i", dubbed_audio,
            "-c:v", "copy",
            "-map", "0:v:0",
            "-map", "1:a:0",
            "-shortest",
            output_path,
        ],
        check=True,
        capture_output=True,
    )
    return output_path
