SQL_CRIAR_TABELA = """
    CREATE TABLE IF NOT EXISTS usuario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome VARCHAR(100) NOT NULL,
        data_nascimento DATE NOT NULL,
        email VARCHAR(100) NOT NULL,
        telefone VARCHAR(20) NOT NULL,
        senha VARCHAR(100) NOT NULL,
        perfil INTEGER NOT NULL,
        tema VARCHAR(20) NOT NULL
    )
"""

SQL_INSERIR = """
    INSERT INTO usuario (nome, data_nascimento, email, telefone, senha, perfil, tema)
    VALUES (?, ?, ?, ?, ?, ?, "default")
"""

SQL_CHECAR_CREDENCIAIS = """
    SELECT id, nome, email, perfil, tema
    FROM usuario
    WHERE email = ? AND senha = ?
"""

SQL_ATUALIZAR_DADOS = """
    UPDATE usuario
    SET nome = ?, data_nascimento = ?, email = ?, telefone = ?
    WHERE id = ?
"""

SQL_ATUALIZAR_SENHA = """
    UPDATE usuario
    SET senha = ?
    WHERE id = ?
"""

SQL_ATUALIZAR_TEMA = """
    UPDATE usuario
    SET tema = ?
    WHERE id = ?
"""

SQL_EXCLUIR = """
    DELETE FROM usuario
    WHERE id = ?
"""
