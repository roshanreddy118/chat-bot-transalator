import logging
import asyncio
import os
from typing import Optional

import requests

logger = logging.getLogger(__name__)


# -------------------------------------------
# HuggingFace Inference API
# -------------------------------------------

async def chat_with_huggingface(message: str, user_language: str = "en") -> Optional[str]:
    """Primary HF API call with stable model"""
    
    api_key = os.getenv("HUGGINGFACE_API_KEY")
    if not api_key:
        logger.error("❌ Missing HuggingFace API key")
        return None
    
    model = "mistralai/Mistral-7B-Instruct-v0.2"
    url = f"https://api-inference.huggingface.co/models/{model}"

    if user_language == "hi":
        prompt = f"Respond in Hindi: {message}"
    else:
        prompt = f"Respond in English: {message}"

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 256,
            "temperature": 0.7,
            "do_sample": True
        }
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    logger.info(f"➡ Calling HuggingFace model: {model}")

    try:
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: requests.post(url, json=payload, headers=headers, timeout=40)
        )

        logger.info(f"HF status: {response.status_code}")

        if response.status_code == 200:
            try:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    text = result[0].get("generated_text", "").strip()
                    if len(text) > 5:
                        return text
            except Exception as json_err:
                logger.error(f"JSON parse err: {json_err}")
                logger.error(f"Raw: {response.text[:200]}")

        elif response.status_code == 503:
            logger.warning("⚠ HF model loading… return None")
            return None

        else:
            logger.error(f"⚠ HF Error {response.status_code}: {response.text[:200]}")
            return None

    except Exception as e:
        logger.error(f"Request error: {e}")

    return None


# -------------------------------------------
# Keyword Detection (kept minimal)
# -------------------------------------------

def is_ai_question(message: str) -> bool:
    keywords = ["what", "explain", "how", "why", "?",
                "kya", "batao", "samjhao"]
    msg = message.lower()
    return any(k in msg for k in keywords)


# -------------------------------------------
# MAIN AI HANDLER
# -------------------------------------------

async def get_ai_response(message: str, user_language: str = "en") -> str:
    """Route request to HuggingFace only"""

    logger.info("⚙ Getting AI response...")

    answer = await chat_with_huggingface(message, user_language)
    
    if answer:
        logger.info("✔ HuggingFace succeeded")
        return answer
    
    logger.warning("⚠ Fallback triggered")

    return (
        "अभी AI service उपलब्ध नहीं है, कृपया बाद में कोशिश करें। 🙏"
        if user_language == "hi"
        else "I'm having trouble responding right now. Please try again later 😊"
    )
