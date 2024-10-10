from datetime import datetime, timedelta
import os
from typing import Optional
from fastapi import HTTPException, Request
from fastapi.responses import RedirectResponse
import jwt
from dto.usuario_autenticado_dto import UsuarioAutenticadoDto


def criar_token_jwt(usuarioAutenticadoDto: UsuarioAutenticadoDto) -> str:
    dados_token = {
        "id": usuarioAutenticadoDto.id,
        "nome": usuarioAutenticadoDto.nome,
        "email": usuarioAutenticadoDto.email,
        "perfil": usuarioAutenticadoDto.perfil,
        "exp": datetime.now() + timedelta(days=1)
    }
    secret_key = os.getenv("JWT_TOKEN_SECRET_KEY")
    return jwt.encode(dados_token, secret_key, "HS256")


def decodificar_token_jwt(token: str) -> Optional[UsuarioAutenticadoDto]:
    secret_key = os.getenv("JWT_TOKEN_SECRET_KEY")
    try:
        dados_token = jwt.decode(token, secret_key, "HS256")
        return UsuarioAutenticadoDto(
            id=int(dados_token["id"]),
            nome=dados_token["nome"],
            email=dados_token["email"],
            perfil=int(dados_token["perfil"]),
        )
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def adicionar_token_jwt(response: RedirectResponse, token: str):
    response.set_cookie(
        key="jwt_token",
        value=token,
        max_age=3600 * 24,
        httponly=True,
        samesite="strict",
    )


def remover_token_jwt(response: RedirectResponse):
    response.set_cookie(
        key="jwt_token",
        value="",
        max_age=0,
        httponly=True,
        samesite="strict",
    )


async def checar_autenticacao(request: Request, call_next):
    token = request.cookies.get("jwt_token", None)
    if token:
        usuario_autenticado_dto = decodificar_token_jwt(token)
        request.state.usuario = usuario_autenticado_dto
    response = await call_next(request)
    return response


async def checar_autorizacao(request: Request):
    usuario = request.state.usuario if hasattr(request.state, "usuario") else None
    area_do_usuario = request.url.path.startswith("/usuario")
    area_do_aluno = request.url.path.startswith("/aluno")
    area_do_professor = request.url.path.startswith("/professor")
    if (area_do_usuario or area_do_aluno or area_do_professor) and usuario is None:
        raise HTTPException(status_code=401, detail="Usuário não autenticado!")
    if area_do_aluno and usuario.perfil != 1:
        raise HTTPException(status_code=403, detail="Usuário não autorizado!")
    if area_do_professor and usuario.perfil != 2:
        raise HTTPException(status_code=403, detail="Usuário não autorizado!")