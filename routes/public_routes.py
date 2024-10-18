from datetime import date, datetime, timedelta
import bcrypt
from fastapi import APIRouter, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from dto.usuario_autenticado_dto import UsuarioAutenticadoDto
from models.usuario_model import Usuario
from repositories.usuario_repo import UsuarioRepo
from util.auth import adicionar_token_jwt, criar_token_jwt
from util.mensagens import adicionar_mensagem_erro, adicionar_mensagem_sucesso
from util.validators import *


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def get_root(request: Request):
    usuario = request.state.usuario if hasattr(request.state, "usuario") else None
    if not usuario:
        return RedirectResponse("/entrar", status.HTTP_303_SEE_OTHER)
    nome_perfil = None
    match(usuario.perfil):
        case 1: nome_perfil = "aluno"
        case 2: nome_perfil = "professor"
        case _: nome_perfil = ""
    response = RedirectResponse(f"/{nome_perfil}", status.HTTP_303_SEE_OTHER)
    return response


@router.get("/cadastrar")
async def get_cadastrar(request: Request):
    perfis = [
        {"value": 1, "label": "Aluno"},
        {"value": 2, "label": "Professor"},
    ]
    return templates.TemplateResponse(
        "pages/cadastrar.html", {"request": request, "perfis": perfis}
    )


@router.post("/cadastrar")
async def post_cadastrar(request: Request):
    # capturar os dados do formulário de cadastro como um dicionário
    dados = dict(await request.form())
    # normalizar os dados para tipificar os valores corretamente
    dados["data_nascimento"] = date.fromisoformat(dados["data_nascimento"])
    dados["perfil"] = int(dados["perfil"])
    # validar dados do formulário
    erros = {}
    # validação da senha igual à confirmação da senha
    if is_matching_fields(dados["senha"], "senha", "Senha", dados["confirmacao_senha"], "Confirmação de Senha", erros):
        dados.pop("confirmacao_senha")
    # validação do nome
    is_person_fullname(dados["nome"], "nome", "Nome", erros)
    is_size_between(dados["nome"], "nome", "Nome", erros)
    # validação da data de nascimento
    data_minima = datetime.now() - timedelta(days=365 * 130)
    data_maxima = datetime.now() - timedelta(days=365 * 18)
    is_date_between(dados["data_nascimento"], "data_nascimento", "Data de Nascimento", data_minima, data_maxima, erros)
    # validação do email
    is_email(dados["email"], "email", "E-mail", erros)
    # validação do telefone
    is_size_between(dados["telefone"], "telefone", "Telefone", 14, 15, erros)    
    # validação da senha
    is_password(dados["senha"], "senha", "Senha", erros)
    # montagem da exibição dos erros
    if erros:
        response = templates.TemplateResponse(
            "pages/cadastrar.html",
            {"request": request, "dados": dados, "erros": erros},
        )
        adicionar_mensagem_erro(response, "Há erros no formulário. Corrija-os e tente novamente.")
        return response
    # criptografar a senha com bcrypt
    senha_hash = bcrypt.hashpw(dados["senha"].encode(), bcrypt.gensalt())
    dados["senha"] = senha_hash.decode()
    # criar um objeto Usuario com os dados do dicionário
    usuario = Usuario(**dados)
    # inserir o objeto Usuario no banco de dados usando o repositório
    usuario = UsuarioRepo.inserir(usuario)
    # se inseriu com sucesso, redirecionar para a página de login
    if usuario:
        response = RedirectResponse("/entrar", status.HTTP_303_SEE_OTHER)
        adicionar_mensagem_sucesso(response, "Cadastro realizado com sucesso!")
        return response
    # se não inseriu, redirecionar para a página de cadastro com mensagem de erro
    else:
        response = RedirectResponse("/cadastrar", status.HTTP_303_SEE_OTHER)
        adicionar_mensagem_erro(
            response,
            "Ocorreu um problema ao realizar seu cadastro. Tente novamente mais tarde.",
        )
        return response


@router.get("/entrar")
async def get_entrar(request: Request):
    return templates.TemplateResponse("pages/entrar.html", {"request": request})


@router.post("/entrar")
async def post_entrar(request: Request):
    dados = dict(await request.form())
    email = dados["email"]
    senha = dados["senha"]
    senha_hash = UsuarioRepo.obter_senha_por_email(email)
    if senha_hash and bcrypt.checkpw(senha.encode(), senha_hash.encode()):
        usuario = UsuarioRepo.obter_dados_por_email(email)
        usuarioAutenticadoDto = UsuarioAutenticadoDto(
            id=usuario.id,
            nome=usuario.nome,
            email=usuario.email,
            perfil=usuario.perfil,
            tema=usuario.tema,
        )
        token = criar_token_jwt(usuarioAutenticadoDto)
        nome_perfil = None
        match(usuarioAutenticadoDto.perfil):
            case 1: nome_perfil = "aluno"
            case 2: nome_perfil = "professor"
            case _: nome_perfil = ""
        response = RedirectResponse(f"/{nome_perfil}", status.HTTP_303_SEE_OTHER)
        adicionar_token_jwt(response, token)
        adicionar_mensagem_sucesso(response, "Login realizado com sucesso!")
        return response
    else:
        response = RedirectResponse("/entrar", status.HTTP_303_SEE_OTHER)
        adicionar_mensagem_erro(response, "Credenciais inválidas! Cheque os valores digitados e tente novamente.")
        return response


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
