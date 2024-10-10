from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from util.mensagens import adicionar_mensagem_erro


templates = Jinja2Templates(directory="templates")


def tratar_excecoes(app: FastAPI):

    @app.exception_handler(401)
    async def unauthorized_exception_handler(request, exc):
        return_url = f"?return_url={request.url.path}"
        response = RedirectResponse(f"/entrar{return_url}")
        adicionar_mensagem_erro(
            response,
            f"Você precisa estar autenticado para acessar a página do endereço {request.url.path}.",
        )
        return response

    @app.exception_handler(404)
    async def not_found_exception_handler(request, exc):
        return templates.TemplateResponse(
            "pages/404.html", {"request": request}, status_code=404
        )
