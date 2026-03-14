import gc
import os
import requests
import time
import json

import numpy as np
import soundfile as sf
from config import SARVAM_API_KEY, SARVAM_API_BASE_URL, SARVAM_BULBUL_V3_MODEL


def _get_device() -> str:
    """Simple device detection - Sarvam runs on their servers."""
    return "api"


def _generate_with_sarvam(
    text: str,
    voice_id: str,
    language: str,
    output_path: str,
    sample_rate: int = 16000
) -> bool:
    """Generate TTS using Sarvam AI API."""
    
    if not SARVAM_API_KEY:
        raise ValueError("SARVAM_API_KEY is not set in environment variables")
    
    headers = {
        "api-subscription-key": SARVAM_API_KEY,
        "Content-Type": "application/json",
    }
    
    payload = {
        "inputs": [{"text": text}],
        "target_language_code": language,
        "voice_id": voice_id,
        "model_id": SARVAM_BULBUL_V3_MODEL,
        "speaker_gender": "female" if "female" in voice_id else "male",
        "encoding": "wav",
        "sample_rate": sample_rate,
    }
    
    try:
        # Make API request
        response = requests.post(
            f"{SARVAM_API_BASE_URL}/tts",
            headers=headers,
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            # Save the audio file
            with open(output_path, "wb") as f:
                f.write(response.content)
            return True
        else:
            print(f"Sarvam API error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"Sarvam TTS generation error: {e}")
        return False


def generate_tts_clips(
    segments: list[dict],
    original_audio_path: str,  # kept for API compatibility
    output_dir: str,
    lang: str = "en",
    voice_id: str = "en_female_1",  # Default voice
) -> list[str]:
    """
    Generate TTS clips using Sarvam AI API.
    
    Args:
        segments: List of segments with translated_text
        original_audio_path: Path to original audio (not used)
        output_dir: Output directory for clips
        lang: Language code
        voice_id: Sarvam voice ID to use
    
    Returns:
        List of paths to generated audio clips
    """
    
    clips_dir = os.path.join(output_dir, "clips")
    os.makedirs(clips_dir, exist_ok=True)
    
    clip_paths = []
    for i, seg in enumerate(segments):
        out_path = os.path.join(clips_dir, f"clip_{i}.wav")
        text = seg.get("translated_text", "").strip()
        
        if not text:
            # Write 0.5s silence for empty segments
            sf.write(out_path, np.zeros(8000, dtype=np.float32), 16000)
            clip_paths.append(out_path)
            continue
        
        # Generate TTS with Sarvam
        success = _generate_with_sarvam(text, voice_id, lang, out_path)
        
        if not success:
            # Fallback: create silent clip
            sf.write(out_path, np.zeros(8000, dtype=np.float32), 16000)
        
        clip_paths.append(out_path)
        
        # Small delay to avoid rate limiting
        time.sleep(0.1)
    
    gc.collect()
    return clip_paths