import base64
import gc
import os
import requests
import time
import json

import numpy as np
import soundfile as sf
from config import SARVAM_API_KEY, SARVAM_API_BASE_URL, SARVAM_LANGUAGE_MAP


def _generate_with_sarvam(
    text: str,
    voice_id: str,
    language: str,
    output_path: str,
    sample_rate: int = 16000
) -> bool:
    """Generate TTS using Sarvam AI API for Indian languages."""
    
    if not SARVAM_API_KEY:
        raise ValueError("SARVAM_API_KEY is not set in environment variables")
    
    # Convert language code to Sarvam format (e.g., "hi" -> "hi-IN")
    sarvam_lang = SARVAM_LANGUAGE_MAP.get(language)
    
    if sarvam_lang is None:
        raise ValueError(f"Language '{language}' is not supported by Sarvam TTS API. Supported languages: hi, bn, ta, te, kn, ml, mr, gu, pa, or")
    
    headers = {
        "api-subscription-key": SARVAM_API_KEY,
        "Content-Type": "application/json",
    }
    
    payload = {
        "text": text,
        "target_language_code": sarvam_lang,
        "speaker": voice_id,
        "model": "bulbul:v3",
        "speech_sample_rate": sample_rate,
    }
    
    try:
        response = requests.post(
            f"{SARVAM_API_BASE_URL}/text-to-speech",
            headers=headers,
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            if "audios" in result and result["audios"]:
                audio_data = base64.b64decode(result["audios"][0])
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                return True
            else:
                print(f"Sarvam API error: No audio in response")
                return False
        else:
            print(f"Sarvam API error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"Sarvam TTS generation error: {e}")
        return False


def generate_tts_clips_indic(
    segments: list[dict],
    original_audio_path: str,
    output_dir: str,
    lang: str,
    voice_id: str = None,
) -> list[str]:
    """Generate TTS clips for Indian languages using Sarvam AI API."""
    
    from config import SARVAM_VOICES
    
    # Get default voice for language if not specified
    from config import DEFAULT_VOICE
    if not voice_id and lang in SARVAM_VOICES:
        voice_id = SARVAM_VOICES[lang][0]
    elif not voice_id:
        voice_id = DEFAULT_VOICE  # Use "shubh" as fallback
    
    clips_dir = os.path.join(output_dir, "clips")
    os.makedirs(clips_dir, exist_ok=True)
    
    clip_paths = []
    for i, seg in enumerate(segments):
        out_path = os.path.join(clips_dir, f"clip_{i}.wav")
        text = seg.get("translated_text", "").strip()
        
        if not text:
            sf.write(out_path, np.zeros(8000, dtype=np.float32), 16000)
            clip_paths.append(out_path)
            continue
        
        success = _generate_with_sarvam(text, voice_id, lang, out_path)
        
        if not success:
            sf.write(out_path, np.zeros(8000, dtype=np.float32), 16000)
        
        clip_paths.append(out_path)
        time.sleep(0.1)
    
    gc.collect()
    return clip_paths
