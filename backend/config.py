import os
from pathlib import Path


# ── Paths ─────────────────────────────────────────────────────────────────────
UPLOAD_DIR = Path("uploads")

# ── API Keys ──────────────────────────────────────────────────────────────────
SARVAM_API_KEY = os.getenv("SARVAM_API_KEY", "")
SARVAM_API_BASE_URL = os.getenv("SARVAM_API_BASE_URL", "https://api.sarvam.ai")
SARVAM_BULBUL_V3_MODEL = os.getenv("SARVAM_BULBUL_V3_MODEL", "bulbul-v3")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


# ── Whisper (Stage 2) ─────────────────────────────────────────────────────────
# GTX 1650 (4GB VRAM) safe choices:
#   "small"  ~2GB  → fast, good accuracy          ✅ recommended
#   "medium" ~3GB  → best quality that safely fits ✅ current
#   "large"  ~5GB  → ❌ OOM on 4GB VRAM
WHISPER_MODEL = "medium"
WHISPER_COMPUTE = "int8"        # int8 saves VRAM vs float16, same accuracy
WHISPER_SOURCE_LANGUAGE = os.getenv("WHISPER_SOURCE_LANGUAGE", "").strip() or None


# ── Translation (Stage 3) ─────────────────────────────────────────────────────
NLLB_MODEL = "facebook/nllb-200-distilled-600M"  # free, no auth, ~2.3GB


# ── TTS (Stage 4) ─────────────────────────────────────────────────────────────
# F5_REF_DURATION kept for backward compat but unused by MMS-TTS
F5_REF_DURATION = 6  # seconds


# ── Language routing maps ─────────────────────────────────────────────────────

# Language codes for UI and API
LANGUAGE_MAP = {
    # International
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "pt": "Portuguese",
    "ar": "Arabic",
    "ja": "Japanese",
    "ko": "Korean",
    "zh": "Chinese",
    "tr": "Turkish",
    "it": "Italian",
    "ru": "Russian",
    "id": "Indonesian",
    "vi": "Vietnamese",
    # Indian regional (19 languages)
    "hi": "Hindi",
    "bn": "Bengali",
    "ta": "Tamil",
    "te": "Telugu",
    "kn": "Kannada",
    "ml": "Malayalam",
    "mr": "Marathi",
    "gu": "Gujarati",
    "pa": "Punjabi",
    "or": "Odia",
    "ur": "Urdu",
    "as": "Assamese",
    "mai": "Maithili",
    "sa": "Sanskrit",
    "raj": "Rajasthani",
    "bho": "Bhojpuri",
    "doi": "Dogri",
    "kok": "Konkani",
    "mni": "Manipuri",
    "sat": "Santali",
    "sd": "Sindhi",
}

# Sarvam AI Voice IDs for each language (using new API speaker names)
SARVAM_VOICES = {
    # Indian regional voices
    "hi": ["priya", "shubh"],  # Female, Male
    "bn": ["priya", "shubh"],
    "ta": ["priya", "shubh"],
    "te": ["priya", "shubh"],
    "kn": ["priya", "shubh"],
    "ml": ["priya", "shubh"],
    "mr": ["priya", "shubh"],
    "gu": ["priya", "shubh"],
    "pa": ["priya", "shubh"],
    "or": ["priya", "shubh"],
    "ur": ["priya", "shubh"],
    "as": ["priya", "shubh"],
    "mai": ["priya"],  # Fallback to Hindi
    "sa": ["priya"],  # Fallback to Hindi
    "raj": ["priya"],  # Fallback to Hindi
    "bho": ["priya"],  # Fallback to Hindi
    "doi": ["priya"],  # Fallback to Hindi
    "kok": ["priya"],  # Fallback to Marathi
    "mni": ["priya"],  # Fallback to Bengali
    "sat": ["priya"],  # Fallback to Bengali
    "sd": ["priya"],  # Fallback to Urdu
    # International voices (fallback to English)
    "es": ["shubh"],
    "fr": ["shubh"],
    "de": ["shubh"],
    "pt": ["shubh"],
    "ar": ["shubh"],
    "ja": ["shubh"],
    "ko": ["shubh"],
    "zh": ["shubh"],
    "tr": ["shubh"],
    "it": ["shubh"],
    "ru": ["shubh"],
    "id": ["shubh"],
    "vi": ["shubh"],
}

# Sarvam API language codes (needs -IN suffix)
SARVAM_LANGUAGE_MAP = {
    "hi": "hi-IN",
    "bn": "bn-IN",
    "ta": "ta-IN",
    "te": "te-IN",
    "kn": "kn-IN",
    "ml": "ml-IN",
    "mr": "mr-IN",
    "gu": "gu-IN",
    "pa": "pa-IN",
    "or": "or-IN",
    "ur": "ur-IN",
    "as": "as-IN",
    "mai": "hi-IN",
    "sa": "hi-IN",
    "raj": "hi-IN",
    "bho": "hi-IN",
    "doi": "hi-IN",
    "kok": "mr-IN",
    "mni": "bn-IN",
    "sat": "bn-IN",
    "sd": "ur-IN",
    "es": "en-IN",
    "fr": "en-IN",
    "de": "en-IN",
    "pt": "en-IN",
    "ar": "en-IN",
    "ja": "en-IN",
    "ko": "en-IN",
    "zh": "en-IN",
    "tr": "en-IN",
    "it": "en-IN",
    "ru": "en-IN",
    "id": "en-IN",
    "vi": "en-IN",
}


# Indian regional languages (19 languages)
INDIAN_LANGUAGES = {
    "hi",   # Hindi
    "bn",   # Bengali
    "ta",   # Tamil
    "te",   # Telugu
    "kn",   # Kannada
    "ml",   # Malayalam
    "mr",   # Marathi
    "gu",   # Gujarati
    "pa",   # Punjabi
    "or",   # Odia
    "ur",   # Urdu
    "as",   # Assamese
    "mai",  # Maithili
    "sa",   # Sanskrit
    "raj",  # Rajasthani
    "bho",  # Bhojpuri
    "doi",  # Dogri
    "kok",  # Konkani
    "mni",  # Manipuri
    "sat",  # Santali
    "sd",   # Sindhi
}


# Mapping from lang code → indic_nlp_library normalizer code
# Used for Unicode/punctuation normalization
INDIC_NLP_LANG_MAP = {
    "hi": "hi",
    "bn": "bn",
    "ta": "ta",
    "te": "te",
    "kn": "kn",
    "ml": "ml",
    "mr": "mr",
    "gu": "gu",
    "pa": "pa",
    "or": "or",
    "ur": "ur",
    "as": "as",
    "mai": "hi",   # Maithili → Hindi normalizer
    "sa": "hi",    # Sanskrit → Hindi normalizer
    "raj": "hi",   # Rajasthani → Hindi normalizer
    "bho": "hi",   # Bhojpuri → Hindi normalizer
    "doi": "hi",   # Dogri → Hindi normalizer
    "kok": "mr",   # Konkani → Marathi normalizer
    "mni": "bn",   # Manipuri → Bengali normalizer
    "sat": "bn",   # Santali → Bengali normalizer
    "sd": "ur",    # Sindhi → Urdu normalizer
}


# ── Pipeline stage names (for job status UI) ──────────────────────────────────
STAGE_NAMES = {
    1: "Extracting audio",
    2: "Transcribing audio",
    3: "Translating segments",
    4: "Generating dubbed speech",
    5: "Syncing audio timing",
    6: "Assembling audio track",
    7: "Muxing final video",
}
