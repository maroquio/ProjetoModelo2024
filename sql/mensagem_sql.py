SQL_CRIAR_TABELA = """
    CREATE TABLE IF NOT EXISTS mensagem (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_remetente INTEGER NOT NULL,
        id_destinatario INTEGER NOT NULL,
        conteudo VARCHAR(1024) NOT NULL,
        data_hora DATE NOT NULL
    )
"""

SQL_INSERIR = """
    INSERT INTO conteudo (id_remetente, id_destinatario, conteudo, data_hora)
    VALUES (?, ?, ?, CURRENT_TIMESTAMP)
"""

SQL_OBTER_CONVERSA = """
    SELECT conteudo, data_hora
    FROM conteudo
    WHERE id_remetente = ? AND id_destinatario = ?
    ORDERY BY data_hora DESC
"""