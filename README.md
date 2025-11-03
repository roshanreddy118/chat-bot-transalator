# 🤖🌍 AI Chatbot Translator

A powerful real-time multilingual chat application that combines **AI chat capabilities** with **instant translation**, built with **FastAPI**, **WebSockets**, and **Local AI Models**.

## ✨ Key Features

### 🤖 AI-Powered Chat
- **Local AI Integration**: Seamlessly integrates with Ollama models (Gemma3, Llama3, etc.) for private, fast AI responses
- **Multiple AI Backends**: Support for OpenAI, Groq, HuggingFace, and other AI services
- **Real-time AI Responses**: Get instant answers to technical questions, explanations, and general queries
- **Smart Question Detection**: Automatically detects when users are asking AI questions vs. casual chat

### 🌍 Advanced Translation System
- **Real-time Translation**: Messages are instantly translated between users speaking different languages
- **Multi-service Translation**: Google Translate API with fallback dictionary for common terms
- **Long Text Support**: Handles lengthy AI responses by chunking and reassembling translations
- **Language-aware AI**: AI responses are generated and translated to each user's preferred language

### 💬 Real-time Chat
- **WebSocket-based**: Real-time communication with multiple users
- **Multi-user Support**: Users can join with different languages and communicate seamlessly
- **Message Types**: Supports both casual chat and AI assistance in the same interface
- **Language Indicators**: Clear visual indicators showing original and translated content

## 🛠️ Technology Stack

- **Backend**: FastAPI with WebSocket support
- **AI Models**: Ollama (local), OpenAI, Groq, HuggingFace Inference API
- **Translation**: Google Translate API + fallback dictionary
- **Frontend**: Vanilla JavaScript with modern WebSocket handling
- **Real-time**: AsyncIO for concurrent message processing and translation

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- (Optional) Ollama with downloaded models for local AI

### Installation
```bash
git clone https://github.com/yourusername/ai-chatbot-translator.git
cd ai-chatbot-translator
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Running the Application
```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Open your browser to `http://127.0.0.1:8000`

### With Local AI (Recommended)
1. Install [Ollama](https://ollama.ai)
2. Download a model: `ollama pull gemma3:4b`
3. Start Ollama: `ollama serve`
4. Run the application as above

## 🎯 Use Cases

- **International Teams**: Team members speaking different languages can communicate naturally
- **Language Learning**: Practice conversations with AI assistance in multiple languages
- **Technical Support**: Get AI explanations about programming, DevOps, and technology topics
- **Educational Settings**: Students can ask questions and receive answers in their native language
- **Global Communities**: Build inclusive chat environments for diverse user bases

## 📱 How It Works

1. **Join Chat**: Users select their preferred language for receiving messages
2. **Multi-language Communication**: Type in any language, others see it translated to their preference
3. **AI Assistance**: Ask questions like "what is Docker?" or "explain machine learning" 
4. **Smart Translation**: AI responses are translated to each user's language preference
5. **Real-time Updates**: All communication happens instantly via WebSockets

## 🔧 Configuration

The application supports multiple AI and translation backends through environment variables:

```bash
# AI Model Backend
AI_MODEL_BACKEND=ollama  # ollama | openai | groq | huggingface

# Translation Backend  
TRANSLATOR_BACKEND=google  # google | libre

# API Keys (optional)
OPENAI_API_KEY=your_key_here
GROQ_API_KEY=your_key_here
HUGGINGFACE_API_KEY=your_key_here
```

## 🏗️ Architecture

- **`app/main.py`**: FastAPI application and WebSocket handling
- **`app/ai_chat.py`**: AI model integration and response generation
- **`app/translator.py`**: Translation services with multiple backends
- **`app/connection_manager.py`**: WebSocket connection management
- **`static/`**: Frontend HTML, CSS, and JavaScript
- **`tests/`**: Unit tests for translation functionality

## 🌟 Features in Detail

### AI Integration
- Prioritizes local Ollama models for privacy and speed
- Automatic fallback to cloud AI services
- Supports technical Q&A, general knowledge, and conversational AI
- Handles responses up to 500+ words with proper translation

### Translation System
- Handles both short chat messages and long AI responses
- Smart chunking for large text translation
- Fallback dictionary for common technical terms
- Support for Hindi, English, and extensible to other languages

### Real-time Chat
- Multiple users with different language preferences
- Visual indicators for original vs. translated content
- Special styling for AI responses vs. user messages
- Connection status and user presence indicators

## 🧪 Testing with Ollama Models

### Setting Up Local AI Testing

#### 1. Install Ollama
```bash
# macOS
brew install ollama

# Or download from https://ollama.ai
curl -fsSL https://ollama.ai/install.sh | sh
```

#### 2. Download Recommended Models for Testing
```bash
# Start Ollama service
ollama serve

# In another terminal, pull models:
# Lightweight model (2GB) - Fast responses
ollama pull gemma2:2b

# Balanced model (3.3GB) - Good quality responses  
ollama pull gemma3:4b

# Advanced model (4.1GB) - High quality responses
ollama pull llama3.2:3b

# Large model (7GB) - Best quality (if you have resources)
ollama pull llama3:8b
```

#### 3. Verify Model Installation
```bash
# List installed models
ollama list

# Test a model directly
ollama run gemma3:4b "What is Python programming?"
```

### 🚀 Real-time Testing Scenarios

#### Test 1: Basic AI Chat Functionality
1. Start the application: `uvicorn app.main:app --host 127.0.0.1 --port 8000`
2. Open browser to `http://127.0.0.1:8000`
3. Set language to English and join chat
4. Test these AI questions:
   ```
   - "what is Docker?"
   - "explain machine learning"
   - "how does FastAPI work?"
   - "what is the difference between Python and Java?"
   ```

#### Test 2: Multilingual AI Responses
1. Set "I want to receive in" to **Hindi**
2. Ask questions in English:
   ```
   - "what is artificial intelligence?"
   - "explain cloud computing"
   - "what is React?"
   ```
3. Verify AI responses are translated to Hindi

#### Test 3: Multi-user Multilingual Chat
1. **Open multiple browser tabs/windows**
2. **Tab 1**: Join as "User1" with English preference
3. **Tab 2**: Join as "User2" with Hindi preference  
4. **Test scenarios**:
   ```
   Tab 1: Ask "what is Kubernetes?"
   → Both users should see the AI response in their language
   
   Tab 1: Type "hello everyone" 
   Tab 2: Type "namaste sabko"
   → Each message appears translated for the other user
   ```

#### Test 4: Long AI Response Translation
1. Ask complex questions that generate long responses:
   ```
   - "explain the complete software development lifecycle"
   - "what are all the components of a modern web application?"
   - "describe the differences between SQL and NoSQL databases"
   ```
2. Verify the complete response is translated (not just first sentence)

#### Test 5: Performance Testing
```bash
# Monitor Ollama performance
ollama ps

# Check response times in browser developer tools
# Network tab → WebSocket messages
```

### 🔧 Testing Different Models

Update your configuration to test different models:

```bash
# Test with different models by updating the ollama model preference
# in app/ai_chat.py or via environment variable

export OLLAMA_MODEL=gemma3:4b    # Default - balanced performance
export OLLAMA_MODEL=llama3.2:3b  # Alternative high-quality model
export OLLAMA_MODEL=gemma2:2b    # Lightweight for testing
```

### 🐛 Troubleshooting Tests

#### Ollama Not Responding
```bash
# Check if Ollama is running
ps aux | grep ollama

# Restart Ollama
killall ollama
ollama serve

# Check Ollama logs
ollama logs
```

#### Poor AI Response Quality
```bash
# Try a larger model
ollama pull llama3:8b

# Or adjust model parameters in app/ai_chat.py:
# Increase temperature for more creative responses
# Adjust num_predict for longer responses
```

#### Translation Issues
```bash
# Test translation independently
curl -X POST "http://127.0.0.1:8000/test-translation" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world", "from": "en", "to": "hi"}'
```

### 📊 Expected Test Results

#### Performance Benchmarks
- **Local Ollama Response**: 1-3 seconds (depending on model size)
- **Translation Time**: 0.5-1 second for short text, 2-5 seconds for long AI responses
- **WebSocket Latency**: <100ms for message delivery
- **Memory Usage**: 2-8GB (depending on model)

#### Quality Expectations
- **Technical Questions**: Comprehensive, accurate responses
- **Translation Accuracy**: 85-95% for common languages
- **Multilingual Consistency**: Same information in different languages
- **Real-time Performance**: Smooth chat experience with multiple users

### 🎯 Automated Testing

Run the included test suite:
```bash
# Run translation tests
python -m pytest tests/test_translator.py -v

# Test with different models
OLLAMA_MODEL=gemma2:2b python -m pytest tests/ -v
OLLAMA_MODEL=llama3.2:3b python -m pytest tests/ -v

# Run performance tests
python -m pytest tests/ -v --benchmark
```

### 📝 Testing Checklist

- [ ] Ollama service is running
- [ ] At least one model is downloaded and tested
- [ ] Basic AI questions work in English  
- [ ] AI responses translate to other languages
- [ ] Multi-user chat works simultaneously
- [ ] Long AI responses translate completely
- [ ] WebSocket connections are stable
- [ ] Translation fallbacks work when services fail
- [ ] Performance is acceptable for your use case

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙋‍♂️ Support

- Create an [issue](https://github.com/yourusername/ai-chatbot-translator/issues) for bug reports
- Start a [discussion](https://github.com/yourusername/ai-chatbot-translator/discussions) for feature requests
- Check the [wiki](https://github.com/yourusername/ai-chatbot-translator/wiki) for detailed documentation

## 🏷️ Tags

`ai-chatbot` `translation` `multilingual` `fastapi` `websockets` `ollama` `real-time-chat` `python` `javascript` `machine-translation`

---

**Built with ❤️ for global communication and AI accessibility**
