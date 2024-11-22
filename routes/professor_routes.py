from fastapi import APIRouter, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from repositories.usuario_repo import UsuarioRepo


router = APIRouter(prefix="/professor")
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def get_root(request: Request):
    return templates.TemplateResponse(
        "pages/professor/index.html", {"request": request}
    )

@router.get("/alunos")
async def get_alunos(request: Request):
    alunos = UsuarioRepo.obter_por_perfil(1)
    return templates.TemplateResponse("pages/professor/alunos.html", {"request": request, "alunos": alunos})