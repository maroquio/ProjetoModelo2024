from fastapi import APIRouter, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from repositories.usuario_repo import UsuarioRepo


router = APIRouter(prefix="/aluno")
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def get_root(request: Request):
    return templates.TemplateResponse("pages/aluno/index.html", {"request": request})

@router.get("/professores")
async def get_professores(request: Request):
    professores = UsuarioRepo.obter_por_perfil(2)
    return templates.TemplateResponse("pages/aluno/professores.html", {"request": request, "professores": professores})
