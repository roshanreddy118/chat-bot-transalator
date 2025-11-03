# app/main.py
import json
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from .connection_manager import ConnectionManager
from .translator import translate_text
from .ai_chat import get_ai_response, is_ai_question
from .config import APP_NAME

app = FastAPI(title=APP_NAME)

# Serve static frontend
app.mount("/static", StaticFiles(directory="static"), name="static")

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Handles real-time WebSocket connections with AI chat and translation."""
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)
            msg_type = payload.get("type")
            
            print(f"DEBUG: Received message type: {msg_type}, payload: {payload}")

            if msg_type == "join":
                name = payload.get("name", "Anon")
                lang = payload.get("lang", "en")
                manager.meta[websocket] = {"name": name, "lang": lang}
                print(f"DEBUG: User {name} joined with language {lang}")
                await manager.broadcast_json({"type": "system", "msg": f"{name} joined ({lang})"})

            elif msg_type == "message":
                sender_meta = manager.meta.get(websocket, {"name": "Anon", "lang": "en"})
                sender_name = sender_meta["name"]
                sender_lang = payload.get("lang", sender_meta.get("lang", "en"))
                text = payload.get("text", "")
                
                print(f"DEBUG: Processing message from {sender_name} ({sender_lang}): '{text}'")

                # Check if this is an AI question
                if is_ai_question(text):
                    print(f"DEBUG: Detected AI question, getting AI response")
                    
                    # Send AI response back to user and broadcast to others
                    tasks = []
                    for conn in list(manager.active_connections):
                        recipient_meta = manager.meta.get(conn, {"lang": "en"})
                        recipient_lang = recipient_meta.get("lang", "en")
                        
                        # Get AI response in English first (Gemma3 responds in English by default)
                        ai_response_en = await get_ai_response(text, "en")
                        print(f"DEBUG: AI response (English): '{ai_response_en}'")
                        
                        # Translate AI response to recipient's language if needed
                        if recipient_lang != "en":
                            translated_response = await translate_text(ai_response_en, "en", recipient_lang)
                            print(f"DEBUG: Translated AI response to {recipient_lang}: '{translated_response}'")
                        else:
                            translated_response = ai_response_en
                        
                        async def send_ai_response(conn_ref, response, to_lang):
                            out = {
                                "type": "ai_chat",
                                "from": "🤖 AI Assistant",
                                "from_lang": "en",
                                "text": f"Q: {text}",
                                "translated_text": f"A: {response}",
                                "to_lang": to_lang,
                                "original_question": text
                            }
                            print(f"DEBUG: Sending AI response: {out}")
                            await conn_ref.send_json(out)
                        
                        tasks.append(send_ai_response(conn, translated_response, recipient_lang))
                    
                    await asyncio.gather(*tasks)
                
                else:
                    # Regular chat message - translate and send as before
                    print(f"DEBUG: Regular chat message, translating")
                    tasks = []
                    for conn in list(manager.active_connections):
                        recipient_meta = manager.meta.get(conn, {"lang": "en"})
                        recipient_lang = recipient_meta.get("lang", "en")
                        
                        print(f"DEBUG: Translating '{text}' from {sender_lang} to {recipient_lang}")

                        async def send_to(conn_ref, to_lang):
                            translated = await translate_text(text, sender_lang, to_lang)
                            print(f"DEBUG: Translation result: '{translated}'")
                            out = {
                                "type": "chat",
                                "from": sender_name,
                                "from_lang": sender_lang,
                                "text": text,
                                "translated_text": translated,
                                "to_lang": to_lang
                            }
                            print(f"DEBUG: Sending message: {out}")
                            await conn_ref.send_json(out)

                        tasks.append(send_to(conn, recipient_lang))

                    await asyncio.gather(*tasks)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"DEBUG: WebSocket error: {e}")
        manager.disconnect(websocket)

@app.get("/")
async def root():
    """Serves the main frontend page."""
    with open("static/index.html", "r", encoding="utf-8") as f:
        html = f.read()
    return HTMLResponse(html)
