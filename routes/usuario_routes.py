from fastapi import APIRouter, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from util.auth import remover_token_jwt


router = APIRouter(prefix="/usuario")
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def get_root(request: Request):
    return templates.TemplateResponse("pages/usuario/index.html", {"request": request})


@router.get("/tema")
async def get_tema(request: Request):
    temas = [
        {"value": 1, "label": "Claro"},
        {"value": 2, "label": "Escuro"},
    ]
    return templates.TemplateResponse(
        "pages/usuario/tema.html", {"request": request, "temas": temas}
    )


@router.post("/tema")
async def post_tema(request: Request):
    return RedirectResponse("/usuario", status.HTTP_303_SEE_OTHER)


@router.get("/dados")
async def get_dados(request: Request):
    return templates.TemplateResponse("pages/usuario/dados.html", {"request": request})


@router.post("/dados")
async def post_dados(request: Request):
    return RedirectResponse("/usuario", status.HTTP_303_SEE_OTHER)


@router.get("/senha")
async def get_senha(request: Request):
    return templates.TemplateResponse("pages/usuario/senha.html", {"request": request})


@router.post("/senha")
async def post_senha(request: Request):
    return RedirectResponse("/usuario", status.HTTP_303_SEE_OTHER)


@router.get("/sair")
async def get_sair(request: Request):
    response = RedirectResponse("/", status.HTTP_303_SEE_OTHER)
    remover_token_jwt(response)
    return response
