from fastapi import APIRouter, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates


router = APIRouter(prefix="/usuario")
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def get_root(request: Request):
    return RedirectResponse("/entrar", status.HTTP_303_SEE_OTHER)


@router.get("/tema")
async def get_tema(request: Request):
    temas = [
        {"value": 1, "label": "Claro"},
        {"value": 2, "label": "Escuro"},
    ]
    return templates.TemplateResponse("pages/usuario/tema.html", {"request": request, "temas": temas})
