from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes.public_routes import router as public_router
from routes.usuario_routes import router as usuario_router


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


app.include_router(public_router)
app.include_router(usuario_router)