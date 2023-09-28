from uuid import uuid4
from datetime import datetime
from typing import Union


class Carro:
    def __init__(self) -> None:
        self.id = str(uuid4())
        self.datatime_entrada: datetime = datetime.now()
        self.datatime_saida: Union[datetime,None] = None
        self.posicao_vaga: str = ""

    def __repr__(self) -> str:
        return f"Carro(id={self.id}, datatime_entrada={self.datatime_entrada}, datatime_saida={self.datatime_saida}, posicao_vaga={self.posicao_vaga})"
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "datatime_entrada": str(self.datatime_entrada),
            "datatime_saida": str(self.datatime_saida),
            "posicao_vaga": self.posicao_vaga
        }
