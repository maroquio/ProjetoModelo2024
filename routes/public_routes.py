from fastapi import APIRouter, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def get_root(request: Request):
    return RedirectResponse("/entrar", status.HTTP_303_SEE_OTHER)


@router.get("/cadastrar")
async def get_entrar(request: Request):
    perfis = [
        {"value": 1, "label": "Aluno"},
        {"value": 2, "label": "Professor"},
    ]
    return templates.TemplateResponse(
        "pages/cadastrar.html", {"request": request, "perfis": perfis}
    )


@router.post("/cadastrar")
async def post_cadastrar(request: Request):
    return RedirectResponse("/entrar", status.HTTP_303_SEE_OTHER)


@router.get("/entrar")
async def get_entrar(request: Request):
    return templates.TemplateResponse("pages/entrar.html", {"request": request})


@router.post("/entrar")
async def post_entrar(request: Request):
    return RedirectResponse("/usuario", status.HTTP_303_SEE_OTHER)


@router.get("/404")
async def get_not_found(request: Request):
    return templates.TemplateResponse("pages/404.html", {"request": request})


@router.get("/erro")
async def get_not_found(request: Request):
    return templates.TemplateResponse("pages/erro.html", {"request": request})


@router.get("/testemacros")
async def get_testarmacros(request: Request):
    estados_civis = [
        {"value": 1, "label": "Solteiro(a)"},
        {"value": 2, "label": "Casado(a)"},
        {"value": 3, "label": "Divorciado(a)"},
        {"value": 4, "label": "Viúvo(a)"},
    ]
    return templates.TemplateResponse(
        "pages/teste_macros.html", {"request": request, "estados_civis": estados_civis}
    )
