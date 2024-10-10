from fastapi import FastAPI
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="templates")


def tratar_excecoes(app: FastAPI):
    @app.exception_handler(404)
    async def not_found_exception_handler(request, exc):
        return templates.TemplateResponse("pages/404.html", {"request": request}, status_code=404)