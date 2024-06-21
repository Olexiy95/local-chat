from fastapi import APIRouter, Form, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from passlib.hash import bcrypt
from sqlite3 import Connection
from db import get_db

router = APIRouter()
templates = Jinja2Templates(directory="templates")


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
    user = cursor.execute(
        "SELECT * FROM users WHERE username = ?", (username,)
    ).fetchone()
    if user is not None:
        stored_password = user[2]
        if bcrypt.verify(password, stored_password):
            response = RedirectResponse(url="/chat", status_code=303)
            response.set_cookie(
                key="session_token", value="session_token_here", httponly=True
            )
            return response
    return HTMLResponse(content="Invalid username or password", status_code=400)
