import socket
import pickle
from time import sleep
from components.carro import Carro


class ConectionTCP:
    def __init__(self, ip: str, port: int):
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def connect(self):
        self.sock.connect((self.ip, self.port))

    def send(self, data):
        self.sock.send(data.encode())
        
    def receive(self):
        return self.sock.recv(2048).decode()
    
    def enviar_dados(
            self, 
            lista_carro: list[Carro],
    ):
        while True:
            if len(lista_carro) > 0:
                try:
                    num_carros_andar_1 = len(list(filter(
                        lambda carro: carro.datatime_saida == None and carro.posicao_vaga[0] == "A", lista_carro
                    )))
                    num_carros_andar_2 = len(list(filter(
                        lambda carro: carro.datatime_saida == None and carro.posicao_vaga[0] == "B", lista_carro
                    )))
                except:
                    pass
                ultimo_carro = list(filter(
                    lambda carro: carro.datatime_saida != None, lista_carro
                ))
                if len(ultimo_carro) > 0:
                    ultimo_carro = ultimo_carro[-1].to_dict()
                else:
                    ultimo_carro = None
            else:
                ultimo_carro = None
                num_carros_andar_1 = 0
                num_carros_andar_2 = 0
            dados = {
                "num_carros_andar_1": num_carros_andar_1,
                "num_carros_andar_2": num_carros_andar_2,
                "ultimo_carro": ultimo_carro,
            }
            try:
                data_serializada = pickle.dumps(dados)
                self.sock.send(data_serializada)
            except:
                self.reconectar()
            sleep(1)
    
    def receive_dict(self):
        return self.sock.recv(2048)

    def close(self):
        self.sock.close()

    def aguardar_conexao(self):
        self.sock.listen(1)
        self.conexao, self.endereco = self.sock.accept()
        
    def reconectar(self):
        try:
            self.sock.connect((self.ip, self.port))
        except:
            sleep(5)
