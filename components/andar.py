from components.carro import Carro
from components.vaga import Vaga
from RPi import GPIO
from time import sleep

class Andar:
    def __init__(
            self, 
            entrada_1: int, 
            entrada_2: int, 
            entrada_3: int, 
            sensor_de_vagas: int,
            sinal_de_lotado_fechado: int,
            num_andar: int
    ) -> None:
        self.entrada_1 = entrada_1
        self.entrada_2 = entrada_2
        self.entrada_3 = entrada_3
        self.sensor_de_vagas = sensor_de_vagas
        self.sinal_de_lotado_fechado = sinal_de_lotado_fechado
        self.vagas: list[Vaga] = []
        self.num_vagas_ocupadas = 0
        self.num_carros_andar = 0
        self.num_andar = num_andar
        self.init_vagas()
        
    def init_vagas(self) -> None:
        self.prefixo = "A" if self.num_andar == 1 else "B"
        for i in range(8):
            self.vagas.append(Vaga(0, f"{self.prefixo}{i+1}"))
    
    def monitorar_vagas(
            self, 
            lista_carros: list[Carro], 
            fila_carros_sair: list[Carro]
    ) -> None:
        while True:
            self.num_vagas_ocupadas = 0
            for i in range(0,8):
                GPIO.output(self.entrada_1, i & 0x01)
                GPIO.output(self.entrada_2, i & 0x02)
                GPIO.output(self.entrada_3, i & 0x04)
                sleep(0.1)
                
                if GPIO.input(self.sensor_de_vagas) == 1:
                    if self.vagas[i].status == 0:
                        lista_carros[-1].posicao_vaga = f"{self.prefixo}{i+1}"
                        self.vagas[i].id_carro = lista_carros[-1].id
                    self.vagas[i].status = 1
                else:
                    if self.vagas[i].status == 1:
                        carro_saindo = list(filter(
                            lambda carro : carro.posicao_vaga == f"{self.prefixo}{i+1}", lista_carros
                        ))[-1]
                        fila_carros_sair.append(carro_saindo)
                        self.vagas[i].id_carro = ""
                    self.vagas[i].status = 0
                
                if self.vagas[i].status == 1:
                    self.num_vagas_ocupadas += 1
            self.num_carros_andar = self.num_vagas_ocupadas
            sleep(0.1)
