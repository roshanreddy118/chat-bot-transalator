# app/translator.py
import logging
import asyncio
from typing import Optional

logger = logging.getLogger(__name__)

async def translate_with_requests(text: str, source_lang: str, target_lang: str) -> Optional[str]:
    """Translate using direct Google Translate API calls with requests - handles long text"""
    try:
        import requests
        import urllib.parse
        
        # For very long text, we need to break it into chunks
        max_chunk_size = 4000  # Google Translate limit per request
        
        if len(text) > max_chunk_size:
            # Split text into chunks at sentence boundaries
            sentences = text.split('. ')
            chunks = []
            current_chunk = ""
            
            for sentence in sentences:
                if len(current_chunk + sentence + '. ') > max_chunk_size:
                    if current_chunk:
                        chunks.append(current_chunk.strip())
                    current_chunk = sentence + '. '
                else:
                    current_chunk += sentence + '. '
            
            if current_chunk:
                chunks.append(current_chunk.strip())
            
            # Translate each chunk
            translated_chunks = []
            for chunk in chunks:
                chunk_translation = await translate_single_chunk(chunk, source_lang, target_lang)
                if chunk_translation:
                    translated_chunks.append(chunk_translation)
                else:
                    translated_chunks.append(chunk)  # Keep original if translation fails
            
            return ' '.join(translated_chunks)
        else:
            # For shorter text, translate directly
            return await translate_single_chunk(text, source_lang, target_lang)
        
    except Exception as e:
        logger.error(f"Direct Google Translate API error: {e}")
        return None

async def translate_single_chunk(text: str, source_lang: str, target_lang: str) -> Optional[str]:
    """Translate a single chunk of text"""
    try:
        import requests
        
        # Google Translate API endpoint (free, no auth needed)
        url = "https://translate.googleapis.com/translate_a/single"
        params = {
            'client': 'gtx',
            'sl': source_lang,
            'tl': target_lang,
            'dt': 't',
            'q': text
        }
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # Run the synchronous request in a thread pool
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None, 
            lambda: requests.get(url, params=params, headers=headers, timeout=15)
        )
        
        if response.status_code == 200:
            result = response.json()
            if result and len(result) > 0 and len(result[0]) > 0:
                # Collect all translation segments
                translated_parts = []
                for segment in result[0]:
                    if segment and len(segment) > 0:
                        translated_parts.append(segment[0])
                
                if translated_parts:
                    full_translation = ''.join(translated_parts)
                    return full_translation
        
        return None
        
    except Exception as e:
        logger.error(f"Single chunk translation error: {e}")
        return None

async def translate_with_fallback_dict(text: str, source_lang: str, target_lang: str) -> Optional[str]:
    """Fallback dictionary for common words"""
    translations = {
        ("hi", "en"): {
            "tum": "you",
            "kaise ho": "how are you", 
            "namaste": "hello",
            "dhanyawad": "thank you",
            "haan": "yes",
            "nahi": "no",
            "kya": "what",
            "kahan": "where",
            "kab": "when",
            "kyun": "why",
            "kaun": "who",
            "acha": "good",
            "bura": "bad",
            "pani": "water",
            "khana": "food",
            "ghar": "home",
            "kaam": "work",
            "hello": "namaste",
            "hi": "namaste",
            # Add more Hindi words
            "katarnak": "dangerous",
            "kharab": "bad",
            "accha": "good",
            "bahut": "very",
            "thoda": "little",
            "zyada": "more",
            "kam": "less",
            "paani": "water",
            "doodh": "milk",
            "dhoodh": "milk",
            "roti": "bread",
            "chawal": "rice",
            "daal": "lentils",
            "sabzi": "vegetables",
            "mithai": "sweets",
            "chai": "tea",
            "kaha": "where",
            "kaise": "how",
            "kyun": "why",
            "koi": "someone",
            "kuch": "something",
            "sab": "all",
            "main": "I",
            "tum": "you",
            "woh": "he/she",
            "hum": "we",
            "aap": "you (formal)",
            "yeh": "this",
            "wahan": "there",
            "yahan": "here",
            "abhi": "now",
            "phir": "then",
            "jaldi": "quickly",
            "dhire": "slowly"
        },
        ("en", "hi"): {
            "you": "tum",
            "how are you": "kaise ho",
            "hello": "namaste", 
            "thank you": "dhanyawad",
            "yes": "haan",
            "no": "nahi",
            "what": "kya",
            "where": "kahan",
            "when": "kab",
            "why": "kyun",
            "who": "kaun",
            "good": "acha",
            "bad": "bura",
            "water": "pani",
            "food": "khana",
            "home": "ghar",
            "work": "kaam",
            "dangerous": "katarnak",
            "very": "bahut",
            "little": "thoda",
            "more": "zyada",
            "less": "kam",
            "milk": "doodh",
            "bread": "roti",
            "rice": "chawal",
            "tea": "chai"
        }
    }
    
    lang_pair = (source_lang, target_lang)
    if lang_pair in translations:
        text_lower = text.lower().strip()
        if text_lower in translations[lang_pair]:
            return translations[lang_pair][text_lower]
    
    return None

async def translate_text(text: str, source_lang: str, target_lang: str) -> str:
    """
    Translate text with multiple fallback strategies.
    """
    if not text or source_lang == target_lang:
        return text
    
    original_text = text
    
    # Strategy 1: Try direct Google Translate API
    try:
        result = await translate_with_requests(text, source_lang, target_lang)
        if result and result.strip() and result.strip() != text:
            logger.info(f"Translation successful (Google API): '{text}' -> '{result}' ({source_lang} -> {target_lang})")
            return result.strip()
    except Exception as e:
        logger.error(f"Google API translation failed: {e}")
    
    # Strategy 2: Use fallback dictionary for common words
    try:
        result = await translate_with_fallback_dict(text, source_lang, target_lang)
        if result:
            logger.info(f"Translation successful (Dictionary): '{text}' -> '{result}' ({source_lang} -> {target_lang})")
            return result
    except Exception as e:
        logger.error(f"Dictionary translation failed: {e}")
    
    # Strategy 3: If all else fails, return with indication
    logger.warning(f"All translation methods failed for: '{text}' ({source_lang} -> {target_lang})")
    return f"{text} (translation unavailable)"
