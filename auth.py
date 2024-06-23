from fastapi import APIRouter, Form, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from passlib.hash import bcrypt
from sqlite3 import Connection
from config import CHAT_DATABASE_NAME
from db import get_db
from db import DatabaseManager

router = APIRouter()
templates = Jinja2Templates(directory="templates")

db_manager = DatabaseManager(CHAT_DATABASE_NAME)

@router.get("/login")
async def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
async def login(
    username: str = Form(...),
    password: str = Form(...),
    db: Connection = Depends(get_db),
):
    cursor = db.cursor()
    user_info = cursor.execute(
        "SELECT id, password FROM users WHERE username = ?", (username,)
    ).fetchone()
    print("User:", user_info)
    if user_info is not None:
        user_id = user_info[0]
        stored_password = user_info[1]
        print("Stored password:", stored_password)
        if bcrypt.verify(password, stored_password):
            response = RedirectResponse(url="/chat", status_code=303)
            response.set_cookie(
                key="user_id", value=user_id, httponly=True
            )
            return response
    return HTMLResponse(content="Invalid username or password", status_code=400)


@router.get("/signup")
async def signup_form(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


@router.post("/signup")
async def signup(
    username: str = Form(...),
    password: str = Form(...),
    email: str = Form(...),
    name: str = Form(...),
    bio: str = Form(...),
):
    hashed_password = bcrypt.hash(password)
    db_manager.insert_user(username, hashed_password, email, name, bio)
    return RedirectResponse(url="/auth/login", status_code=303)