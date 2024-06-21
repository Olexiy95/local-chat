from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from db import init_db
from auth import router as auth_router
from chat import router as chat_router

app = FastAPI()

app.include_router(auth_router, prefix="/auth")
app.include_router(chat_router)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

init_db()


@app.get("/")
async def root():
    return RedirectResponse(url="/auth/login")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
