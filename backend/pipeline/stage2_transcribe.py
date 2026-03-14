import gc
import sys
import torch
from config import WHISPER_MODEL, WHISPER_COMPUTE, WHISPER_SOURCE_LANGUAGE


def transcribe(audio_path: str) -> list[dict]:
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

    model = whisperx.load_model(
        WHISPER_MODEL,
        device=device,
        compute_type=WHISPER_COMPUTE,
    )

    transcribe_kwargs = {"batch_size": batch_size}
    if WHISPER_SOURCE_LANGUAGE:
        transcribe_kwargs["language"] = WHISPER_SOURCE_LANGUAGE

    result = model.transcribe(audio_path, **transcribe_kwargs)
    detected_lang = result["language"]

    # Free whisper before loading alignment model (saves VRAM)
    del model
    gc.collect()
    torch.cuda.empty_cache()

    # Alignment — wav2vec2 models, no auth required
    align_model, metadata = whisperx.load_align_model(
        language_code=detected_lang,
        device=device,
    )
    result = whisperx.align(
        result["segments"], align_model, metadata, audio_path, device,
        return_char_alignments=False,
    )

    del align_model
    gc.collect()
    torch.cuda.empty_cache()

    return result["segments"]
