class Vaga:
    def __init__(self, status: int, posicao: str, id_carro: str = ""):
        self.status = status
        self.posicao = posicao
        self.id_carro = id_carro

    def __repr__(self) -> str:
        return f"Vaga(status={self.status}, posicao={self.posicao}, id_carro={self.id_carro})"
    
    def to_dict(self) -> dict:
        return {
            "status": self.status,
            "posicao": self.posicao,
            "id_carro": self.id_carro
        }
