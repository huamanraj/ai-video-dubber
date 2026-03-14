import gc
import json
import requests
from typing import List, Dict
from config import GEMINI_API_KEY, GEMINI_MODEL, LANGUAGE_MAP


def _get_gemini_prompt(target_lang: str, text: str) -> str:
    """Generate a context-aware translation prompt for Gemini."""
    language_name = LANGUAGE_MAP.get(target_lang, target_lang)
    
    # Regional language specific instructions
    regional_prompts = {
        "hi": "हिंदी में अनुवाद करें, संदर्भ बनाए रखें, प्राकृतिक भाषा का प्रयोग करें।",
        "bn": "বাংলায় অনুবাদ করুন, প্রসঙ্গ বজায় রাখুন, প্রাকৃতিক ভাষা ব্যবহার করুন।",
        "ta": "தமிழில் மொழிபெயர்க்கவும், சூழலைப் பேணவும், இயற்கையான மொழியைப் பயன்படுத்தவும்।",
        "te": "తెలుగులో అనువదించండి, సందర్భాన్ని కాపాడండి, సహజ భాషను ఉపయోగించండి।",
        "kn": "ಕನ್ನಡದಲ್ಲಿ ಅನುವಾದಿಸಿ, ಸಂದರ್ಭವನ್ನು ಕಾಪಾಡಿ, ಸಹಜ ಭಾಷೆಯನ್ನು ಬಳಸಿ।",
        "ml": "മലയാളത്തിൽ വിവർത്തനം ചെയ്യുക, സന്ദർഭം സൂക്ഷിക്കുക, സ്വാഭാവിക ഭാഷ ഉപയോഗിക്കുക।",
        "mr": "मराठीत भाषांतर करा, संदर्भ राखा, नैसर्गिक भाषा वापरा।",
        "gu": "ગુજરાતીમાં અનુવાદ કરો, સંદર્ભ જાળવો, કુદરતી ભાષા વાપરો।",
        "pa": "ਪੰਜਾਬੀ ਵਿੱਚ ਅਨੁਵਾਦ ਕਰੋ, ਸੰਦਰਭ ਬਣਾਈ ਰੱਖੋ, ਕੁਦਰਤੀ ਭਾਸ਼ਾ ਦੀ ਵਰਤੋਂ ਕਰੋ।",
        "or": "ଓଡ଼ିଆରେ ଅନୁବାଦ କରନ୍ତୁ, ପ୍ରସଙ୍ଗ ରକ୍ଷା କରନ୍ତୁ, ପ୍ରାକୃତିକ ଭାଷା ବ୍ୟବହାର କରନ୍ତୁ।",
        "ur": "اردو میں ترجمہ کریں، سیاق و سباق برقرار رکھیں، قدرتی زبان استعمال کریں۔",
        "as": "অসমীয়াত অনুবাদ কৰক, প্ৰসংগ ৰাখক, প্ৰাকৃতিক ভাষা ব্যৱহাৰ কৰক।",
    }
    
    base_prompt = f"""Translate the following English text to {language_name} while maintaining the original context, tone, and meaning.

IMPORTANT INSTRUCTIONS:
1. Keep the translation natural and conversational
2. Preserve any technical terms, names, or proper nouns
3. Maintain the same emotional tone (formal, casual, excited, etc.)
4. Keep the same sentence structure and flow
5. Do not add or remove any information
6. Output ONLY the translated text, no explanations

Text to translate: "{text}"

Translated text in {language_name}:"""
    
    # Add regional language specific instruction if available
    if target_lang in regional_prompts:
        base_prompt = f"{regional_prompts[target_lang]}\n\n{base_prompt}"
    
    return base_prompt


def translate_segments(segments: List[Dict], target_lang_code: str) -> List[Dict]:
    """Translate segments using Google Gemini API."""
    
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not set in environment variables")
    
    headers = {
        "Content-Type": "application/json",
    }
    
    for seg in segments:
        text = seg.get("text", "").strip()
        if not text:
            seg["translated_text"] = ""
            continue
        
        try:
            prompt = _get_gemini_prompt(target_lang_code, text)
            
            payload = {
                "contents": [{
                    "parts": [{"text": prompt}]
                }],
                "generationConfig": {
                    "temperature": 0.2,
                    "topP": 0.8,
                    "topK": 40,
                    "maxOutputTokens": 1024,
                }
            }
            
            response = requests.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if "candidates" in result and result["candidates"]:
                    translated = result["candidates"][0]["content"]["parts"][0]["text"].strip()
                    # Clean up any extra text that might have been added
                    translated = translated.split('\n')[0].strip('"\'')
                    seg["translated_text"] = translated
                else:
                    seg["translated_text"] = text  # Fallback to original
            else:
                print(f"Gemini API error: {response.status_code} - {response.text}")
                seg["translated_text"] = text  # Fallback to original
                
        except Exception as e:
            print(f"Translation error for segment: {e}")
            seg["translated_text"] = text  # Fallback to original
    
    gc.collect()
    return segments