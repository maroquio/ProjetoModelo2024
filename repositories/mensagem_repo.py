from typing import Optional
from models.mensagem_model import Mensagem
from sql.mensagem_sql import *
from util.db import obter_conexao


class MensagemRepo:

    @staticmethod
    def criar_tabela():
        with obter_conexao() as db:
            cursor = db.cursor()
            cursor.execute(SQL_CRIAR_TABELA)

    @staticmethod
    def inserir(mensagem: Mensagem) -> Optional[Mensagem]:
        with obter_conexao() as db:
            cursor = db.cursor()
            cursor.execute(
                SQL_INSERIR,
                (
                    mensagem.id_remetente,
                    mensagem.id_destinatario,
                    mensagem.conteudo,                    
                ),
            )
            if cursor.rowcount == 0:
                return None
            mensagem.id = cursor.lastrowid
            return mensagem

    @staticmethod
    def obter_conversa(id_remetente: int, id_destinatario: int) -> list[Mensagem]:
        with obter_conexao() as db:
            cursor = db.cursor()
            cursor.execute(SQL_OBTER_CONVERSA, (id_remetente, id_destinatario))
            dados = cursor.fetchall()
            if dados is None:
                return []
            return [Mensagem(**mensagem) for mensagem in dados]