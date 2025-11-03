# app/connection_manager.py
from fastapi import WebSocket
from typing import List, Dict, Any

class ConnectionManager:
    """Handles active WebSocket connections and user metadata."""
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.meta: Dict[WebSocket, Dict[str, str]] = {}

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        if websocket in self.meta:
            del self.meta[websocket]

    async def broadcast_json(self, payload: Any):
        """Send JSON payload to all connected clients."""
        dead = []
        for conn in list(self.active_connections):
            try:
                await conn.send_json(payload)
            except Exception:
                dead.append(conn)
        for d in dead:
            self.disconnect(d)
