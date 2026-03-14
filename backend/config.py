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

# Sarvam AI Voice IDs for each language
SARVAM_VOICES = {
    # Indian regional voices
    "hi": ["hi_female_1", "hi_male_1", "hi_female_2"],
    "bn": ["bn_female_1", "bn_male_1"],
    "ta": ["ta_female_1", "ta_male_1"],
    "te": ["te_female_1", "te_male_1"],
    "kn": ["kn_female_1", "kn_male_1"],
    "ml": ["ml_female_1", "ml_male_1"],
    "mr": ["mr_female_1", "mr_male_1"],
    "gu": ["gu_female_1", "gu_male_1"],
    "pa": ["pa_female_1", "pa_male_1"],
    "or": ["or_female_1", "or_male_1"],
    "ur": ["ur_female_1", "ur_male_1"],
    "as": ["as_female_1", "as_male_1"],
    "mai": ["hi_female_1"],  # Fallback to Hindi
    "sa": ["hi_female_1"],  # Fallback to Hindi
    "raj": ["hi_female_1"],  # Fallback to Hindi
    "bho": ["hi_female_1"],  # Fallback to Hindi
    "doi": ["hi_female_1"],  # Fallback to Hindi
    "kok": ["mr_female_1"],  # Fallback to Marathi
    "mni": ["bn_female_1"],  # Fallback to Bengali
    "sat": ["bn_female_1"],  # Fallback to Bengali
    "sd": ["ur_female_1"],  # Fallback to Urdu
    # International voices (fallback to English)
    "es": ["en_female_1"],
    "fr": ["en_female_1"],
    "de": ["en_female_1"],
    "pt": ["en_female_1"],
    "ar": ["en_female_1"],
    "ja": ["en_female_1"],
    "ko": ["en_female_1"],
    "zh": ["en_female_1"],
    "tr": ["en_female_1"],
    "it": ["en_female_1"],
    "ru": ["en_female_1"],
    "id": ["en_female_1"],
    "vi": ["en_female_1"],
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
