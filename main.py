from fastapi import FastAPI
from fastapi.responses import HTMLResponse


app = FastAPI()


@app.get("/")
async def get_root():
    return HTMLResponse("<h1>Bem-vindo ao FastAPI</h1>")