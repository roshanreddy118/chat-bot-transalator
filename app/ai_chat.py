import logging
import asyncio
import os
from typing import Optional
import requests

logger = logging.getLogger(__name__)


# -------------------------------------------
# Hugging Face Chat Completion API
# -------------------------------------------

async def chat_with_huggingface(message: str, user_language: str = "en") -> Optional[str]:
    """AI conversation using Hugging Face ChatCompletions API"""

    api_key = os.getenv("HUGGINGFACE_API_KEY")
    if not api_key:
        logger.error("❌ Missing HuggingFace API Key")
        return None

    url = "https://router.huggingface.co/v1/chat/completions"
    model = "mistralai/Mistral-7B-Instruct-v0.2"

    if user_language == "hi":
        system_prompt = "आप एक सहायक AI हैं। हमेशा हिंदी में उपयोगकर्ता के प्रश्न का उत्तर दें।"
    else:
        system_prompt = "You are a helpful assistant. Always reply to the user in English."

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ],
        "max_tokens": 300,
        "temperature": 0.7
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    logger.info(f"➡ HF Request → Model: {model}")

    try:
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None, lambda: requests.post(url, json=payload, headers=headers, timeout=60)
        )

        logger.info(f"HF Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            logger.info(f"HF Response preview: {str(data)[:200]}")

            # Extract content properly
            try:
                text = data["choices"][0]["message"]["content"].strip()
                if len(text) > 3:
                    return text
            except Exception as parse_error:
                logger.error(f"Parsing Error: {parse_error}")
                logger.error(f"Raw Response: {data}")

        else:
            logger.error(f"HF Error Response: {response.text[:200]}")
            return None

    except Exception as e:
        logger.error(f"HF Request Error: {e}")

    return None


# -------------------------------------------
# Keyword Detection (Simple AI Intent Check)
# -------------------------------------------

def is_ai_question(message: str) -> bool:
    keywords = [
        "what", "explain", "how", "why", "define", "?",
        "kya", "batao", "samjhao", "kaise"
    ]
    msg = message.lower()
    return any(k in msg for k in keywords)


# -------------------------------------------
# Main AI Response Handler
# -------------------------------------------

async def get_ai_response(message: str, user_language: str = "en") -> str:
    logger.info(f"⚙ AI Request: {message}")

    answer = await chat_with_huggingface(message, user_language)

    if answer:
        logger.info("✔ HF Response Success")
        return answer

    logger.warning("⚠ Fallback Used")
    return (
        "अभी AI उत्तर देने में समस्या आ रही है, कृपया कुछ देर बाद फिर से प्रयास करें। 🙏"
        if user_language == "hi"
        else "I'm having trouble responding right now. Please try again later 😊"
    )
