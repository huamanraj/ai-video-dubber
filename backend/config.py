import os
from pathlib import Path


# ── Paths ─────────────────────────────────────────────────────────────────────
UPLOAD_DIR = Path("uploads")

# ── API Keys ──────────────────────────────────────────────────────────────────
SARVAM_API_KEY = os.getenv("SARVAM_API_KEY", "")
SARVAM_API_BASE_URL = os.getenv("SARVAM_API_BASE_URL", "https://api.sarvam.ai")
SARVAM_BULBUL_V3_MODEL = os.getenv("SARVAM_BULBUL_V3_MODEL", "bulbul-v3")
SARVAM_STT_MODEL = os.getenv("SARVAM_STT_MODEL", "saaras:v3")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


# ── STT (Stage 2 — Sarvam saarika:v2) ────────────────────────────────────────
# BCP-47 code of the source audio language, e.g. "hi-IN", "en-IN", "ta-IN".
# Leave blank (or "unknown") for auto-detection.
SARVAM_SOURCE_LANGUAGE = os.getenv("SARVAM_SOURCE_LANGUAGE", "unknown").strip() or "unknown"


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

# All available Sarvam AI voice models
ALL_SARVAM_VOICES = [
    "shubh", "aditya", "ritu", "priya", "neha", "rahul", "pooja", "rohan",
    "simran", "kavya", "amit", "dev", "ishita", "shreya", "ratan", "varun",
    "manan", "sumit", "roopa", "kabir", "aayan", "ashutosh", "advait", "anand",
    "tanya", "tarun", "sunny", "mani", "gokul", "vijay", "shruti", "suhani",
    "mohit", "kavitha", "rehan", "soham", "rupali"
]

# Sarvam AI Voice IDs for each language (all voices available for all languages)
SARVAM_VOICES = {
    # Indian regional voices - all voices available
    "hi": ALL_SARVAM_VOICES,
    "bn": ALL_SARVAM_VOICES,
    "ta": ALL_SARVAM_VOICES,
    "te": ALL_SARVAM_VOICES,
    "kn": ALL_SARVAM_VOICES,
    "ml": ALL_SARVAM_VOICES,
    "mr": ALL_SARVAM_VOICES,
    "gu": ALL_SARVAM_VOICES,
    "pa": ALL_SARVAM_VOICES,
    "or": ALL_SARVAM_VOICES,
    "ur": ALL_SARVAM_VOICES,
    "as": ALL_SARVAM_VOICES,
    "mai": ALL_SARVAM_VOICES,
    "sa": ALL_SARVAM_VOICES,
    "raj": ALL_SARVAM_VOICES,
    "bho": ALL_SARVAM_VOICES,
    "doi": ALL_SARVAM_VOICES,
    "kok": ALL_SARVAM_VOICES,
    "mni": ALL_SARVAM_VOICES,
    "sat": ALL_SARVAM_VOICES,
    "sd": ALL_SARVAM_VOICES,
    # International voices
    "es": ALL_SARVAM_VOICES,
    "fr": ALL_SARVAM_VOICES,
    "de": ALL_SARVAM_VOICES,
    "pt": ALL_SARVAM_VOICES,
    "ar": ALL_SARVAM_VOICES,
    "ja": ALL_SARVAM_VOICES,
    "ko": ALL_SARVAM_VOICES,
    "zh": ALL_SARVAM_VOICES,
    "tr": ALL_SARVAM_VOICES,
    "it": ALL_SARVAM_VOICES,
    "ru": ALL_SARVAM_VOICES,
    "id": ALL_SARVAM_VOICES,
    "vi": ALL_SARVAM_VOICES,
}

# Default voice for each language (shubh is default)
DEFAULT_VOICE = "shubh"

# Sarvam API language codes (needs -IN suffix)
# Only supports: bn-IN, en-IN, gu-IN, hi-IN, kn-IN, ml-IN, mr-IN, od-IN, pa-IN, ta-IN, te-IN
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
    "or": "od-IN",  # Odia uses od-IN code
    # Non-supported languages - will fail at TTS stage
    # These are set to None to indicate TTS is not supported
    "ur": None,
    "as": None,
    "mai": None,
    "sa": None,
    "raj": None,
    "bho": None,
    "doi": None,
    "kok": None,
    "mni": None,
    "sat": None,
    "sd": None,
    "es": None,
    "fr": None,
    "de": None,
    "pt": None,
    "ar": None,
    "ja": None,
    "ko": None,
    "zh": None,
    "tr": None,
    "it": None,
    "ru": None,
    "id": None,
    "vi": None,
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
