from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Mensagem:
    id: Optional[int] = None
    id_remetente: Optional[int] = None
    id_destinatario: Optional[int] = None
    conteudo: Optional[str] = None
    data_hora: Optional[datetime] = None    