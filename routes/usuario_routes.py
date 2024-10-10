from datetime import date
import bcrypt
from fastapi import APIRouter, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from models.usuario_model import Usuario
from repositories.usuario_repo import UsuarioRepo
from util.auth import remover_token_jwt
from util.mensagens import adicionar_mensagem_erro, adicionar_mensagem_sucesso


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
    usuarioAutenticadoDto = (
        request.state.usuario if hasattr(request.state, "usuario") else None
    )
    usuario = UsuarioRepo.obter_por_id(usuarioAutenticadoDto.id)
    return templates.TemplateResponse(
        "pages/usuario/dados.html",
        {"request": request, "dados": usuario},
    )


@router.post("/dados")
async def post_dados(request: Request):
    dados = dict(await request.form())
    usuarioAutenticadoDto = (
        request.state.usuario if hasattr(request.state, "usuario") else None
    )
    dados["id"] = usuarioAutenticadoDto.id
    dados["data_nascimento"] = date.fromisoformat(dados["data_nascimento"])
    usuario = Usuario(**dados)
    if UsuarioRepo.atualizar_dados(usuario):
        response = RedirectResponse("/usuario", status.HTTP_303_SEE_OTHER)
        adicionar_mensagem_sucesso(response, "Cadastro atualizado com sucesso!")
        return response
    else:
        response = RedirectResponse("/usuario/dados", status.HTTP_303_SEE_OTHER)
        adicionar_mensagem_erro(
            response,
            "Ocorreu um problema ao atualizar seu cadastro. Tente novamente mais tarde.",
        )
        return response


@router.get("/senha")
async def get_senha(request: Request):
    return templates.TemplateResponse("pages/usuario/senha.html", {"request": request})


@router.post("/senha")
async def post_senha(request: Request):
    dados = dict(await request.form())
    usuarioAutenticadoDto = (
        request.state.usuario if hasattr(request.state, "usuario") else None
    )
    senha_atual = dados["senha_atual"]
    nova_senha = dados["nova_senha"]
    confirmacao_nova_senha = dados["confirmacao_nova_senha"]
    senha_hash = UsuarioRepo.obter_senha_por_email(usuarioAutenticadoDto.email)
    if not senha_hash or not bcrypt.checkpw(senha_atual.encode(), senha_hash.encode()):
        response = RedirectResponse("/usuario/senha", status.HTTP_303_SEE_OTHER)
        adicionar_mensagem_erro(
            response, "Senha atual inválida! Cheque o valor digitado e tente novamente."
        )
        return response
    if nova_senha != confirmacao_nova_senha:
        response = RedirectResponse("/usuario/senha", status.HTTP_303_SEE_OTHER)
        adicionar_mensagem_erro(
            response,
            "Nova senha e confirmação não conferem! Cheque os valores digitados e tente novamente.",
        )
        return response
    if nova_senha == senha_atual:
        response = RedirectResponse("/usuario/senha", status.HTTP_303_SEE_OTHER)
        adicionar_mensagem_erro(
            response,
            "Nova senha deve ser diferente da senha atual! Cheque os valores digitados e tente novamente.",
        )
        return response
    senha_hash = bcrypt.hashpw(nova_senha.encode(), bcrypt.gensalt())
    if UsuarioRepo.atualizar_senha(usuarioAutenticadoDto.id, senha_hash.decode()):
        response = RedirectResponse("/usuario", status.HTTP_303_SEE_OTHER)
        adicionar_mensagem_sucesso(response, "Senha atualizada com sucesso!")
        return response
    else:
        response = RedirectResponse("/usuario/senha", status.HTTP_303_SEE_OTHER)
        adicionar_mensagem_erro(
            response,
            "Ocorreu um problema ao atualizar sua senha. Tente novamente mais tarde.",
        )
        return response


@router.get("/sair")
async def get_sair(request: Request):
    response = RedirectResponse("/", status.HTTP_303_SEE_OTHER)
    remover_token_jwt(response)
    return response
