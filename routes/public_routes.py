from fastapi import APIRouter, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def get_root(request: Request):
    return RedirectResponse("/entrar", status.HTTP_303_SEE_OTHER)


@router.get("/entrar")
async def get_entrar(request: Request):
    return templates.TemplateResponse("pages/entrar.html", {"request": request})


@router.get("/testemacros")
async def get_testarmacros(request: Request):
    estados_civis = [
        {"value": 1, "label": "Solteiro(a)"},
        {"value": 2, "label": "Casado(a)"},
        {"value": 3, "label": "Divorciado(a)"},
        {"value": 4, "label": "Viúvo(a)"},
    ]
    return templates.TemplateResponse("pages/teste_macros.html", {"request": request, "estados_civis": estados_civis})
