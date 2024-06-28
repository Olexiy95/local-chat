from fastapi import APIRouter, Cookie, Form, WebSocket, Request, Depends
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlite3 import Connection
from db import get_db, DatabaseManager
from classes import ConnectionManager
from models import Message
from config import CHAT_DATABASE_NAME

router = APIRouter()
templates = Jinja2Templates(directory="templates")
manager = ConnectionManager()

db_manager = DatabaseManager(CHAT_DATABASE_NAME)


@router.get("/chat")
async def get_chat(request: Request, user_id: str = Cookie(None)):
    if user_id is None:
        return RedirectResponse(url="/auth/login")

    messages = db_manager.get_chat()
    return templates.TemplateResponse(
        "index.html", {"request": request, "messages": messages}
    )


@router.post("/clear_chat")
async def clear_chat(db: Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("DELETE  FROM messages")
    db.commit()
    return JSONResponse(content={"message": "Chat cleared"}, status_code=200)


@router.get("/user/{user_id}")
async def get_profile(request: Request, user_id: str):
    user = db_manager.get_user(user_id)
    print("User:", user)
    if user is None:
        return JSONResponse(content={"message": "User not found"}, status_code=404)
    return templates.TemplateResponse(
        "profile.html", {"request": request, "user": user}
    )


@router.post("/user/{user_id}")
async def update_user(
    user_id: str,
    username: str = Form(None),
    password: str = Form(None),
    email: str = Form(None),
    name: str = Form(None),
    bio: str = Form(None),
    profile_picture: bytes = Form(None),
):
    db_manager.update_user(
        user_id, username, password, email, name, bio, profile_picture
    )
    return RedirectResponse(url=f"/user/{user_id}", status_code=303)


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    user_id: str = Cookie(None),
    db: Connection = Depends(get_db),
):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive()
            print("Raw data received:", data)
            if data["type"] == "websocket.receive" and data.get("text") is not None:
                text_data = data["text"]
                # cursor = db.cursor()
                # cursor.execute("BEGIN")
                try:
                    db_manager.insert_message(user_id, text_data)
                    inserted_message = db_manager.get_last_message(user_id)
                    print("Inserted message:", inserted_message, user_id)
                    # inserted_message_json = {
                    #     "content": inserted_message[2],
                    #     "username": inserted_message[1],
                    #     "timestamp": inserted_message[0],
                    # }
                    inserted_message_json = {
                        "content": inserted_message[2],
                        "username": inserted_message[1],
                        "timestamp": inserted_message[0],
                    }

                except Exception as e:
                    db.rollback()
                    print(f"Error during insert or query: {e}")
                    continue

                await manager.broadcast_json(inserted_message_json)
                # elif data["type"] == "websocket.receive" and data.get("bytes") is not None:
                #     binary_data = data["bytes"]
                #     print("Binary data received:", binary_data)
                #     cursor = db.cursor()
                #     cursor.execute(
                #         "INSERT INTO voice_messages (content) VALUES (?)", (binary_data,)
                #     )
                #     db.commit()

                #     # Get the last inserted row for the voice message
                #     cursor.execute(
                #         "SELECT * FROM voice_messages WHERE id = last_insert_rowid()"
                #     )
                #     inserted_voice_message = cursor.fetchone()

                #     # Send the inserted voice message back to the client
                #     await websocket.send_text("New voice message received")

                # await manager.broadcast_string("New voice message received")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        manager.disconnect(websocket)
