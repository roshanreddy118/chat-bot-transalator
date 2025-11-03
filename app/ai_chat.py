# app/ai_chat.py
import logging
import asyncio
import json
from typing import Optional
from .config import (
    AI_MODEL_BACKEND, OPENAI_API_KEY, OPENAI_MODEL,
    HUGGINGFACE_API_KEY, HUGGINGFACE_CHAT_MODEL,
    OLLAMA_URL, OLLAMA_MODEL, GROQ_API_KEY, TOGETHER_AI_KEY
)

logger = logging.getLogger(__name__)

async def chat_with_huggingface_free(message: str, user_language: str = "en") -> Optional[str]:
    """Use Hugging Face Inference API - completely free, no API key needed"""
    try:
        import requests
        
        # Use text generation models that work well without API keys
        models_to_try = [
            "microsoft/DialoGPT-large",
            "google/flan-t5-large",
            "microsoft/DialoGPT-medium",
            "google/flan-t5-base",
            "facebook/blenderbot-400M-distill"
        ]
        
        for model in models_to_try:
            try:
                url = f"https://api-inference.huggingface.co/models/{model}"
                
                # Format the prompt based on model type
                if "flan-t5" in model:
                    if user_language == "hi":
                        prompt = f"Answer this question in Hindi: {message}"
                    else:
                        prompt = f"Answer this question: {message}"
                elif "blenderbot" in model:
                    prompt = message
                else:
                    if user_language == "hi":
                        prompt = f"User: {message}\nBot (respond in Hindi):"
                    else:
                        prompt = f"User: {message}\nBot:"
                
                payload = {
                    "inputs": prompt,
                    "parameters": {
                        "max_new_tokens": 200,
                        "temperature": 0.7,
                        "do_sample": True,
                        "return_full_text": False
                    }
                }
                
                headers = {"Content-Type": "application/json"}
                
                loop = asyncio.get_event_loop()
                response = await loop.run_in_executor(
                    None,
                    lambda: requests.post(url, headers=headers, json=payload, timeout=10)
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    if isinstance(result, list) and len(result) > 0:
                        generated_text = result[0].get("generated_text", "").strip()
                        if generated_text and len(generated_text) > 10:
                            # Clean up the response
                            clean_text = generated_text.replace(prompt, "").strip()
                            if "Bot:" in clean_text:
                                clean_text = clean_text.split("Bot:")[-1].strip()
                            if clean_text and len(clean_text) > 5:
                                logger.info(f"Success with HuggingFace model: {model}")
                                return clean_text
                    
                elif response.status_code == 503:
                    # Model is loading, try next one
                    logger.info(f"Model {model} is loading, trying next...")
                    continue
                else:
                    logger.warning(f"HuggingFace model {model} returned status: {response.status_code}")
                    
            except Exception as e:
                logger.error(f"Error with HuggingFace model {model}: {e}")
                continue
        
        return None
        
    except Exception as e:
        logger.error(f"HuggingFace free API error: {e}")
        return None

async def chat_with_cohere_free(message: str, user_language: str = "en") -> Optional[str]:
    """Try Cohere's free tier"""
    try:
        import requests
        
        # Cohere has a free trial tier
        url = "https://api.cohere.ai/v1/generate"
        
        if user_language == "hi":
            prompt = f"Question: {message}\nAnswer in Hindi:"
        else:
            prompt = f"Question: {message}\nAnswer:"
        
        payload = {
            "model": "command",
            "prompt": prompt,
            "max_tokens": 150,
            "temperature": 0.7
        }
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer trial-key"  # Some services allow trial access
        }
        
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: requests.post(url, headers=headers, json=payload, timeout=8)
        )
        
        if response.status_code == 200:
            result = response.json()
            if "generations" in result and len(result["generations"]) > 0:
                generated_text = result["generations"][0]["text"].strip()
                if generated_text and len(generated_text) > 10:
                    logger.info("Success with Cohere free API")
                    return generated_text
                    
    except Exception as e:
        logger.error(f"Cohere free API error: {e}")
        
    return None

async def chat_with_together_ai_free(message: str, user_language: str = "en") -> Optional[str]:
    """Try Together AI's free tier"""
    try:
        import requests
        
        url = "https://api.together.xyz/inference"
        
        if user_language == "hi":
            prompt = f"Human: {message}\nAssistant (respond in Hindi):"
        else:
            prompt = f"Human: {message}\nAssistant:"
        
        payload = {
            "model": "togethercomputer/llama-2-7b-chat",
            "prompt": prompt,
            "max_tokens": 150,
            "temperature": 0.7
        }
        
        headers = {"Content-Type": "application/json"}
        
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: requests.post(url, headers=headers, json=payload, timeout=8)
        )
        
        if response.status_code == 200:
            result = response.json()
            if "output" in result and "choices" in result["output"]:
                generated_text = result["output"]["choices"][0]["text"].strip()
                if generated_text and len(generated_text) > 10:
                    logger.info("Success with Together AI free")
                    return generated_text
                    
    except Exception as e:
        logger.error(f"Together AI error: {e}")
        
    return None

async def chat_with_replicate_free(message: str, user_language: str = "en") -> Optional[str]:
    """Try Replicate's free tier"""
    try:
        import requests
        
        url = "https://api.replicate.com/v1/predictions"
        
        if user_language == "hi":
            prompt = f"Question: {message}\nProvide a detailed answer in Hindi:"
        else:
            prompt = f"Question: {message}\nProvide a detailed answer:"
        
        payload = {
            "version": "meta/llama-2-7b-chat",
            "input": {
                "prompt": prompt,
                "max_length": 200,
                "temperature": 0.7
            }
        }
        
        headers = {"Content-Type": "application/json"}
        
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: requests.post(url, headers=headers, json=payload, timeout=8)
        )
        
        if response.status_code in [200, 201]:
            result = response.json()
            if "output" in result and result["output"]:
                generated_text = "".join(result["output"]).strip()
                if generated_text and len(generated_text) > 10:
                    logger.info("Success with Replicate free")
                    return generated_text
                    
    except Exception as e:
        logger.error(f"Replicate error: {e}")
        
    return None

async def chat_with_local_ollama(message: str, user_language: str = "en") -> Optional[str]:
    """Use local Ollama models - prioritized since they're available"""
    try:
        import requests
        
        # Your available models (detected: gemma3:4b)
        models_to_try = ["gemma3:4b", "llama3.2", "llama3.1", "llama2", "phi3", "gemma2"]
        
        for model in models_to_try:
            try:
                url = f"{OLLAMA_URL}/api/generate"
                
                # Craft better prompts for Gemma3
                if user_language == "hi":
                    prompt = f"""You are a helpful AI assistant. Please respond in Hindi language only.
                    
Question: {message}

Please provide a clear, informative answer in Hindi:"""
                else:
                    prompt = f"""You are a helpful AI assistant. Please provide a clear, informative answer.

Question: {message}

Answer:"""
                
                payload = {
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "num_predict": 300,
                        "top_p": 0.9,
                        "repeat_penalty": 1.1
                    }
                }
                
                loop = asyncio.get_event_loop()
                response = await loop.run_in_executor(
                    None,
                    lambda: requests.post(url, json=payload, timeout=30)
                )
                
                if response.status_code == 200:
                    result = response.json()
                    generated_text = result.get("response", "").strip()
                    
                    if generated_text and len(generated_text) > 15:
                        # Clean up the response
                        clean_text = generated_text.strip()
                        
                        # Remove any prompt echoing
                        if "Answer:" in clean_text:
                            clean_text = clean_text.split("Answer:")[-1].strip()
                        
                        logger.info(f"✅ Success with local Ollama model: {model}")
                        return clean_text
                        
                else:
                    logger.warning(f"Ollama model {model} returned status: {response.status_code}")
                    
            except requests.exceptions.ConnectionError:
                logger.error(f"Cannot connect to Ollama at {OLLAMA_URL}. Is Ollama running?")
                return None
            except Exception as e:
                logger.error(f"Ollama model {model} error: {e}")
                continue
        
        return None
        
    except Exception as e:
        logger.error(f"Ollama connection error: {e}")
        return None

async def chat_with_openai_free_api(message: str, user_language: str = "en") -> Optional[str]:
    """Use OpenAI-compatible free APIs that don't require authentication"""
    try:
        import requests
        
        # Free OpenAI-compatible APIs
        free_apis = [
            {
                "url": "https://api.deepinfra.com/v1/openai/chat/completions",
                "model": "microsoft/WizardLM-2-8x22B"
            },
            {
                "url": "https://api.together.xyz/v1/chat/completions", 
                "model": "meta-llama/Llama-2-7b-chat-hf"
            }
        ]
        
        for api in free_apis:
            try:
                if user_language == "hi":
                    system_prompt = "You are a helpful AI assistant. Always respond in Hindi language. Keep responses concise and informative."
                else:
                    system_prompt = "You are a helpful AI assistant. Always respond in English. Keep responses concise and informative."
                
                payload = {
                    "model": api["model"],
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": message}
                    ],
                    "max_tokens": 300,
                    "temperature": 0.7
                }
                
                headers = {"Content-Type": "application/json"}
                
                loop = asyncio.get_event_loop()
                response = await loop.run_in_executor(
                    None,
                    lambda: requests.post(api["url"], headers=headers, json=payload, timeout=10)
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if "choices" in result and len(result["choices"]) > 0:
                        content = result["choices"][0]["message"]["content"].strip()
                        if content and len(content) > 10:
                            logger.info(f"Success with free API: {api['url']}")
                            return content
                            
            except Exception as e:
                logger.error(f"Free API {api['url']} error: {e}")
                continue
        
        return None
        
    except Exception as e:
        logger.error(f"OpenAI-compatible free APIs error: {e}")
        return None

async def chat_with_huggingface_spaces(message: str, user_language: str = "en") -> Optional[str]:
    """Use HuggingFace Spaces that host free models"""
    try:
        import requests
        
        # Working HuggingFace Spaces
        spaces = [
            "https://api-inference.huggingface.co/models/google/flan-t5-xl",
            "https://api-inference.huggingface.co/models/EleutherAI/gpt-j-6b"
        ]
        
        for space_url in spaces:
            try:
                if "flan-t5" in space_url:
                    if user_language == "hi":
                        prompt = f"Answer in Hindi: {message}"
                    else:
                        prompt = f"Answer: {message}"
                else:
                    if user_language == "hi":
                        prompt = f"Human: {message}\nAssistant (in Hindi):"
                    else:
                        prompt = f"Human: {message}\nAssistant:"
                
                payload = {
                    "inputs": prompt,
                    "parameters": {
                        "max_new_tokens": 200,
                        "temperature": 0.7,
                        "do_sample": True
                    }
                }
                
                headers = {"Content-Type": "application/json"}
                
                loop = asyncio.get_event_loop()
                response = await loop.run_in_executor(
                    None,
                    lambda: requests.post(space_url, headers=headers, json=payload, timeout=8)
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    if isinstance(result, list) and len(result) > 0:
                        generated_text = result[0].get("generated_text", "").strip()
                        if generated_text:
                            clean_text = generated_text.replace(prompt, "").strip()
                            if clean_text and len(clean_text) > 10:
                                logger.info(f"Success with HuggingFace Space: {space_url}")
                                return clean_text
                                
            except Exception as e:
                logger.error(f"HuggingFace Space {space_url} error: {e}")
                continue
        
        return None
        
    except Exception as e:
        logger.error(f"HuggingFace Spaces error: {e}")
        return None

async def chat_with_groq_api(message: str, user_language: str = "en") -> Optional[str]:
    """Try Groq API with free tier"""
    try:
        import requests
        
        # Groq provides free API access
        url = "https://api.groq.com/openai/v1/chat/completions"
        
        if user_language == "hi":
            system_prompt = "You are a helpful AI assistant. Always respond in Hindi language."
        else:
            system_prompt = "You are a helpful AI assistant. Always respond in English."
        
        payload = {
            "model": "llama3-8b-8192",  # Free model
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            "max_tokens": 300,
            "temperature": 0.7
        }
        
        # Try without API key first (sometimes works for limited requests)
        headers = {"Content-Type": "application/json"}
        
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: requests.post(url, headers=headers, json=payload, timeout=10)
        )
        
        if response.status_code == 200:
            result = response.json()
            if "choices" in result and len(result["choices"]) > 0:
                content = result["choices"][0]["message"]["content"].strip()
                if content and len(content) > 10:
                    logger.info("Success with Groq free API")
                    return content
                    
    except Exception as e:
        logger.error(f"Groq API error: {e}")
        
    return None

def is_ai_question(message: str) -> bool:
    """
    Determine if a message is asking for AI assistance (not just translation)
    """
    ai_keywords = [
        "what is", "what are", "explain", "tell me about", "how does", "why",
        "define", "meaning of", "help me", "can you", "please", "?",
        "kya hai", "batao", "samjhao", "kaise", "kyun", "madad karo"
    ]
    
    message_lower = message.lower()
    return any(keyword in message_lower for keyword in ai_keywords)

async def get_ai_response(message: str, user_language: str = "en") -> str:
    """
    Get real-time AI response - prioritize local Ollama models
    """
    
    logger.info(f"Getting real-time AI response for: {message}")
    
    # Prioritize local Ollama since it's available and fast
    ai_services = [
        ("Local Ollama (Gemma3:4b)", chat_with_local_ollama),
        ("HuggingFace Free", chat_with_huggingface_free),
        ("Groq Free API", chat_with_groq_api),
        ("OpenAI-compatible Free APIs", chat_with_openai_free_api),
        ("HuggingFace Spaces", chat_with_huggingface_spaces),
    ]
    
    # Try services sequentially, starting with local Ollama
    for service_name, service_func in ai_services:
        try:
            logger.info(f"Trying {service_name}...")
            response = await service_func(message, user_language)
            
            if response and response.strip() and len(response.strip()) > 15:
                logger.info(f"✅ Success with {service_name}")
                return response.strip()
            else:
                logger.warning(f"❌ {service_name} returned empty/short response")
                
        except Exception as e:
            logger.error(f"❌ {service_name} failed: {e}")
            continue
    
    # If all services fail
    logger.warning("All AI services failed, returning fallback message")
    
    if user_language == "hi":
        return f"मुझे खुशी होगी '{message}' के बारे में बताने में, लेकिन अभी AI services से connection में समस्या है। कृपया सुनिश्चित करें कि Ollama चल रहा है: 'ollama serve'"
    else:
        return f"I'd love to help answer your question about '{message}', but I'm having trouble connecting to AI services. Please ensure Ollama is running with: 'ollama serve'"