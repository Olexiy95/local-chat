from fastapi import APIRouter, WebSocket, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from typing import List
from sqlite3 import Connection
from db import get_db

router = APIRouter()
templates = Jinja2Templates(directory="templates")


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@router.get("/chat")
async def get_chat(request: Request, db: Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT timestamp, username, content FROM chat")
    messages = cursor.fetchall()
    return templates.TemplateResponse(
        "index.html", {"request": request, "messages": messages}
    )


@router.post("/clear_chat")
async def clear_chat(db: Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("DELETE FROM messages")
    db.commit()
    return JSONResponse(content={"message": "Chat cleared"}, status_code=200)


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, db: Connection = Depends(get_db)):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive()
            if data["type"] == "websocket.receive" and "text" in data:
                text_data = data["text"]
                cursor = db.cursor()
                cursor.execute(
                    "INSERT INTO messages (user_id, content) VALUES (1, ?)",
                    (text_data,),
                )
                db.commit()
                await manager.broadcast(text_data)
            elif data["type"] == "websocket.receive" and "bytes" in data:
                binary_data = data["bytes"]
                cursor = db.cursor()
                cursor.execute(
                    "INSERT INTO voice_messages (content) VALUES (?)", (binary_data,)
                )
                db.commit()
                await manager.broadcast("New voice message received")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        manager.disconnect(websocket)
