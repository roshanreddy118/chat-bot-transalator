# app/config.py
import os

# Configuration for translation backend
TRANSLATOR_BACKEND = os.getenv("TRANSLATOR_BACKEND", "google")  # google | libre | huggingface | azure
LIBRE_URL = os.getenv("LIBRE_URL", "https://libretranslate.de/translate")
LIBRE_API_KEY = os.getenv("LIBRE_API_KEY", "")

# Google Translate API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

# Azure Translator
AZURE_TRANSLATOR_KEY = os.getenv("AZURE_TRANSLATOR_KEY", "")
AZURE_TRANSLATOR_ENDPOINT = os.getenv("AZURE_TRANSLATOR_ENDPOINT", "")
AZURE_TRANSLATOR_REGION = os.getenv("AZURE_TRANSLATOR_REGION", "")

# Hugging Face API
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "")

# AI Chat Model Configuration
AI_MODEL_BACKEND = os.getenv("AI_MODEL_BACKEND", "free")  # openai | huggingface | ollama | free

# OpenAI API (ChatGPT)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

# Hugging Face Chat Models
HUGGINGFACE_CHAT_MODEL = os.getenv("HUGGINGFACE_CHAT_MODEL", "microsoft/DialoGPT-medium")

# Ollama (Local AI models)
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama2")

# Free AI APIs
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")  # Free Llama models
TOGETHER_AI_KEY = os.getenv("TOGETHER_AI_KEY", "")  # Free tier available

# General settings
APP_NAME = "AI Chatbot Translator"
