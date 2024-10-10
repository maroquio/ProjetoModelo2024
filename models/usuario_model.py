from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Usuario:
    id: Optional[int]
    nome: Optional[str]
    data_nascimento: Optional[date]
    email: Optional[str]
    telefone: Optional[str]
    senha: Optional[str]
    perfil: Optional[int]
    tema: Optional[str]