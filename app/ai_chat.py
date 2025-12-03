import logging
import asyncio
import os
from typing import Optional
import requests

logger = logging.getLogger(__name__)

TOGETHER_API_URL = "https://api.together.xyz/v1/chat/completions"
MODEL_NAME = "meta-llama/Llama-3-8b-instruct"  # Free-tier model

async def chat_with_together(message: str, user_language: str = "en") -> Optional[str]:
    api_key = os.getenv("TOGETHER_API_KEY")
    if not api_key:
        logger.error("❌ Missing Together API Key")
        return None

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    system_msg = (
        "You are a helpful assistant. Always reply in Hindi."
        if user_language == "hi"
        else "You are a helpful assistant. Always reply in English."
    )

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": message}
        ],
        "max_tokens": 300,
        "temperature": 0.7
    }

    try:
        response = requests.post(TOGETHER_API_URL, json=payload, headers=headers, timeout=45)
        logger.info(f"Together status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            logger.info(f"Together resp preview: {str(data)[:200]}")
            return data["choices"][0]["message"]["content"]

        logger.error(f"Together error: {response.text[:200]}")
        return None

    except Exception as e:
        logger.error(f"Together request error: {e}")
        return None


def is_ai_question(message: str) -> bool:
    keywords = ["what", "explain", "how", "why", "define", "?", "kya", "batao", "kaise", "samjhao"]
    msg = message.lower()
    return any(k in msg for k in keywords)


async def get_ai_response(message: str, user_language: str = "en") -> str:
    logger.info("⚙ Calling Together AI...")
    reply = await chat_with_together(message, user_language)

    if reply:
        return reply

    logger.warning("⚠ Fallback used")
    return (
        "AI सेवा में समस्या है, कृपया बाद में कोशिश करें। 🙏"
        if user_language == "hi"
        else "I'm having trouble responding right now. Please try again later 😊"
    )
