import logging
import asyncio
from typing import Optional
import os

logger = logging.getLogger(__name__)

# -------------------------------------------
# Hugging Face Inference API
# -------------------------------------------

async def chat_with_huggingface_free(message: str, user_language: str = "en") -> Optional[str]:
    """Use Hugging Face Inference API with free-tier key"""
    try:
        import requests

        api_key = os.getenv("HUGGINGFACE_API_KEY")
        if not api_key:
            logger.error("HUGGINGFACE_API_KEY missing")
            return None

        models_to_try = [
            "google/flan-t5-xl",
            "google/flan-t5-large",
            "google/flan-t5-base",
        ]

        for model in models_to_try:
            try:
                url = f"https://api-inference.huggingface.co/models/{model}"

                if user_language == "hi":
                    prompt = f"Answer in Hindi: {message}"
                else:
                    prompt = f"Answer: {message}"

                payload = {
                    "inputs": prompt,
                    "parameters": {
                        "max_new_tokens": 250,
                        "temperature": 0.7,
                        "do_sample": True
                    }
                }

                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {api_key}"
                }

                loop = asyncio.get_event_loop()
                response = await loop.run_in_executor(
                    None,
                    lambda: requests.post(url, headers=headers, json=payload, timeout=20)
                )

                if response.status_code == 200:
                    result = response.json()
                    if isinstance(result, list) and len(result) > 0:
                        text = result[0].get("generated_text", "").strip()
                        if len(text) > 10:
                            logger.info(f"Success with HF model: {model}")
                            return text

                elif response.status_code == 503:
                    logger.info(f"{model} loading, trying next...")
                    continue

            except Exception as e:
                logger.error(f"{model} error: {e}")
                continue

        return None

    except Exception as e:
        logger.error(f"HuggingFace API error: {e}")
        return None


# -------------------------------------------
# Hugging Face Spaces backup (optional)
# -------------------------------------------

async def chat_with_huggingface_spaces(message: str, user_language: str = "en") -> Optional[str]:
    """Backup - use HF Spaces"""
    try:
        import requests
        api_key = os.getenv("HUGGINGFACE_API_KEY")

        spaces = [
            "https://api-inference.huggingface.co/models/EleutherAI/gpt-j-6b",
        ]

        for url in spaces:
            try:
                prompt = f"Answer: {message}"

                if user_language == "hi":
                    prompt = f"Answer in Hindi: {message}"

                payload = {
                    "inputs": prompt,
                    "parameters": {"max_new_tokens": 200}
                }

                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {api_key}"
                }

                loop = asyncio.get_event_loop()
                response = await loop.run_in_executor(
                    None,
                    lambda: requests.post(url, headers=headers, json=payload, timeout=20)
                )

                if response.status_code == 200:
                    result = response.json()
                    if isinstance(result, list) and len(result) > 0:
                        text = result[0].get("generated_text", "").strip()
                        if len(text) > 10:
                            return text

            except Exception as e:
                logger.error(f"HF Space error: {e}")
                continue

        return None

    except Exception as e:
        logger.error(f"HuggingFace Spaces error: {e}")
        return None


# -------------------------------------------
# Keyword Detection
# -------------------------------------------

def is_ai_question(message: str) -> bool:
    ai_keywords = [
        "what", "explain", "how", "why", "define", "?", "kya", "batao", "samjhao"
    ]
    m = message.lower()
    return any(word in m for word in ai_keywords)


# -------------------------------------------
# MAIN AI ROUTING FUNCTION
# -------------------------------------------

async def get_ai_response(message: str, user_language: str = "en") -> str:
    """Get AI answer using HuggingFace only (works on Render)"""

    logger.info(f"AI Response for: {message}")

    services = [
        ("HuggingFace Free API", chat_with_huggingface_free),
        ("HuggingFace Spaces", chat_with_huggingface_spaces),
    ]

    for name, func in services:
        try:
            logger.info(f"Using {name}...")
            result = await func(message, user_language)
            if result and len(result.strip()) > 10:
                return result.strip()
        except Exception as e:
            logger.error(f"{name} failed: {e}")

    logger.warning("Fallback response triggered")

    if user_language == "hi":
        return "अभी मुझे जवाब देने में समस्या हो रही है, कृपया थोड़ी देर में दोबारा कोशिश करें। 😊"
    return "I’m having trouble responding right now. Please try again in a moment. 😊"
