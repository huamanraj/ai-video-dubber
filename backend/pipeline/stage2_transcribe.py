import gc
import sys
import torch
from config import WHISPER_MODEL, WHISPER_COMPUTE, WHISPER_SOURCE_LANGUAGE


_model = None
_align_model = None
_align_metadata = None
_detected_lang = None


def transcribe(audio_path: str) -> list[dict]:
    global _model, _align_model, _align_metadata, _detected_lang
    
    try:
        import whisperx
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "WhisperX is missing. "
            f"Install with: \"{sys.executable}\" -m pip install whisperx"
        ) from exc

    # GTX 1650 has 4GB VRAM — use cuda but keep batch_size safe
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # batch_size=16 OOMs on 4GB — use 4 for safety
    # If WHISPER_MODEL is large/large-v2/large-v3 you WILL OOM — use "small" or "medium"
    batch_size = 4 if device == "cuda" else 2

    # Cache model globally to avoid re-downloading each time
    if _model is None:
        print(f"Loading Whisper model: {WHISPER_MODEL}")
        _model = whisperx.load_model(
            WHISPER_MODEL,
            device=device,
            compute_type=WHISPER_COMPUTE,
        )

    transcribe_kwargs = {"batch_size": batch_size}
    if WHISPER_SOURCE_LANGUAGE:
        transcribe_kwargs["language"] = WHISPER_SOURCE_LANGUAGE

    result = _model.transcribe(audio_path, **transcribe_kwargs)
    detected_lang = result["language"]

    # Cache alignment model
    if _align_model is None or _align_metadata is None:
        _align_model, _align_metadata = whisperx.load_align_model(
            language_code=detected_lang,
            device=device,
        )
    
    result = whisperx.align(
        result["segments"], _align_model, _align_metadata, audio_path, device,
        return_char_alignments=False,
    )

    gc.collect()
    torch.cuda.empty_cache()

    return result["segments"]
