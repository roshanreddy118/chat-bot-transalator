import logging
import asyncio
import os
from typing import Optional
import requests

logger = logging.getLogger(__name__)


# -------------------------------------------
# Hugging Face Inference API (Router v1)
# -------------------------------------------

async def chat_with_huggingface(message: str, user_language: str = "en") -> Optional[str]:
    """Primary HuggingFace call using router v1 endpoint"""

    api_key = os.getenv("HUGGINGFACE_API_KEY")
    if not api_key:
        logger.error("❌ Missing HuggingFace API key")
        return None

    model = "mistralai/Mistral-7B-Instruct-v0.2"
    url = f"https://router.huggingface.co/hf-inference/v1/models/{model}"

    if user_language == "hi":
        prompt = f"उत्तर हिंदी में दें: {message}"
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

    logger.info(f"➡ Calling HuggingFace Router v1 model: {model}")

    try:
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: requests.post(url, json=payload, headers=headers, timeout=60)
        )

        logger.info(f"HF status: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            logger.info(f"HF response preview: {str(result)[:200]}")

            # New router response format
            if isinstance(result, dict) and "generated_text" in result:
                text = result["generated_text"].strip()
                if len(text) > 5:
                    return text

        else:
            logger.error(f"⚠ HF Error {response.status_code}: {response.text[:200]}")
            return None

    except Exception as e:
        logger.error(f"❌ HuggingFace request error: {e}")

    return None


# -------------------------------------------
# Keyword Detection
# -------------------------------------------

def is_ai_question(message: str) -> bool:
    keywords = [
        "what", "explain", "how", "why", "define", "?",
        "kya", "batao", "samjhao", "kaise"
    ]
    msg = message.lower()
    return any(k in msg for k in keywords)


# -------------------------------------------
# Main AI Handler
# -------------------------------------------

async def get_ai_response(message: str, user_language: str = "en") -> str:
    logger.info("⚙ Getting AI response...")

    answer = await chat_with_huggingface(message, user_language)

    if answer:
        logger.info("✔ HuggingFace AI success")
        return answer

    logger.warning("⚠ Fallback triggered")

    return (
        "अभी AI सेवा उपलब्ध नहीं है, कृपया थोड़ी देर में कोशिश करें। 🙏"
        if user_language == "hi"
        else "I'm having trouble responding right now. Please try again later 😊"
    )
