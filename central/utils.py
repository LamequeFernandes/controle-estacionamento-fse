from RPi import GPIO
from time import sleep
import socket
import pickle
import json
from datetime import datetime
from components.setup import SetupEstacionamento
from components.sensor_passagem import SensorPassagem


class Utils:
    def __init__(self):
        self.e = SetupEstacionamento()
        self.fechar_estacionamento = False
        self.bloquear_segundo_andar = False
        self.dados = None
        self.status_carro = ""
        self.sensor_passagem = SensorPassagem(
            self.e.sensor_de_passagem_1_a2, self.e.sensor_de_passagem_2_a2
        )
        with open("./jsons/configs.json") as json_file:
            self.configs = json.load(json_file)

    def conectar_socket(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.configs["ip_socket_central"], int(self.configs["porta_socket"])))
        sock.listen(1)

        conexao, endereco = sock.accept()

        while True:
            dados_serializados = conexao.recv(2048)
            try:
                dados_socket = pickle.loads(dados_serializados)
                self.dados = dados_socket
            except EOFError:
                sock.listen(1)
                conexao, endereco = sock.accept()
                continue

            if dados_socket:
                conexao.send("Deu bom".encode())
            sleep(1)


    def estado_estacionamento(self):
        print("interface, dados -> ",self.dados)
        
        if self.dados != None:
            qtd_carros_andar_1 = int(self.dados["num_carros_andar_1"])
            qtd_carros_andar_2 = int(self.dados["num_carros_andar_2"])
            total_carros = qtd_carros_andar_1 + qtd_carros_andar_2

            carro = self.dados["ultimo_carro"]
            if carro == None:
                carro = {
                    "id": "************************************",
                    "datatime_entrada": "*******************",
                    "datatime_saida": "*******************"
                }
                valor_a_pagar = "R$ ********"
            else:
                valor_a_pagar = self.get_valor_a_pagar(
                    carro["datatime_entrada"], carro["datatime_saida"]
                )
                valor_a_pagar = f"R$ {valor_a_pagar:.2f}"

        else:
            qtd_carros_andar_1 = 0
            qtd_carros_andar_2 = 0
            total_carros = 0

            carro = {
                "id": "************************************",
                "datatime_entrada": "*******************",
                "datatime_saida": "*******************"
            }
            valor_a_pagar = "R$ ********"
        
        if self.status_carro == "descendo":
            qtd_carros_andar_1 += 1
        elif self.status_carro == "subindo":
            qtd_carros_andar_2 += 1
        
        print("\n")
        print("===============================================================================")
        print("                           NÚMERO DE CARROS POR ANDAR                         ")
        print(f"                 ANDAR 1: 0{qtd_carros_andar_1}             |            ANDAR 2: 0{qtd_carros_andar_2}           ")
        print("===============================================================================")
        print("                          VAGAS DISPONIVEIS POR ANDAR                         ")
        print(f"                 ANDAR 1: 0{8-qtd_carros_andar_1}             |            ANDAR 2: 0{8-qtd_carros_andar_2}           ")
        print("===============================================================================")
        print("                      TOTAL DE CARROS NO ESTACIONAMENTO                     ")
        print(f"                                        {total_carros}                                ")
        print("===============================================================================")
        print("                              TOTAL A SER PAGO                               ")
        print(f"                    CARRO: {carro['id']}                                      ")
        print(f"  ENTRADA: {carro['datatime_entrada']}   |   SAÍDA: {carro['datatime_saida']}                ")
        print(f"                                    {valor_a_pagar}                            ")
        print("===============================================================================")
        print("                          PRECIONE A TECLA ENTER PARA SAIR                     ")
        print("===============================================================================")
        print("\n")
        input()
        "5:29.120599"

    def get_valor_a_pagar(self, datatime_entrada: str, datatime_saida: str) -> float:
        tempo_total = (
            datetime.strptime(datatime_saida, '%Y-%m-%d %H:%M:%S.%f') -
            datetime.strptime(datatime_entrada, '%Y-%m-%d %H:%M:%S.%f')
        )
        total_mins = (tempo_total.total_seconds()) // 60
        return total_mins * 0.15

    def menu_principal(self, ):
        while True:
            print("\n")
            print("===============================================================================")
            print("                            CONTROLE DE ESTACIONAMENTO                         ")
            print("===============================================================================")
            print("                              1 - Informações atuais                           ")
            print("                              2 - Fecha estacionamento                         ")
            print("                              3 - Liberar estacionamento                       ")
            print("                              4 - Bloquear 2º Andar                            ")
            print("                              5 - Liberar 2º Andar                             ")
            print("===============================================================================")
            opacao_selecionada = int(input("Digite uma opção: "))
            print()
            
            if opacao_selecionada == 1:
                self.estado_estacionamento()
            elif opacao_selecionada == 2:
                self.fechar_estacionamento = True
                sleep(0.2)
                print("Estacionamento fechado")
            elif opacao_selecionada == 3:
                self.fechar_estacionamento = False
                sleep(0.2)
                print("Estacionamento liberado")
            elif opacao_selecionada == 4:
                self.bloquear_segundo_andar = True
            elif opacao_selecionada == 5:
                self.bloquear_segundo_andar = False
            else:
                print("Opção inválida, seleciona uma opção válida")
                sleep(1)


    def verificar_lotacao(self,) -> None:
        while True:
            try:
                if self.fechar_estacionamento == True:
                    GPIO.output(self.e.sinal_de_lotado_fechado_a1.gpio, GPIO.HIGH)
                    GPIO.output(self.e.sinal_de_lotado_fechado_a2.gpio, GPIO.HIGH)
                else:
                    if self.dados["num_carros_andar_1"] == 8:
                        GPIO.output(self.e.sinal_de_lotado_fechado_a1.gpio, GPIO.HIGH)
                    elif self.dados["num_carros_andar_1"] < 8:
                        GPIO.output(self.e.sinal_de_lotado_fechado_a1.gpio, GPIO.LOW)
                        
                    if self.bloquear_segundo_andar == True:
                        GPIO.output(self.e.sinal_de_lotado_fechado_a2.gpio, GPIO.HIGH)
                    elif self.dados["num_carros_andar_2"] == 8:
                        GPIO.output(self.e.sinal_de_lotado_fechado_a2.gpio, GPIO.HIGH)
                    elif self.dados["num_carros_andar_2"] < 8:
                        GPIO.output(self.e.sinal_de_lotado_fechado_a2.gpio, GPIO.LOW)
                sleep(0.2)
            except:
                if self.bloquear_segundo_andar == True:
                    GPIO.output(self.e.sinal_de_lotado_fechado_a2.gpio, GPIO.HIGH)
                else:
                    GPIO.output(self.e.sinal_de_lotado_fechado_a2.gpio, GPIO.LOW)

    def monitorar_passagem(self) -> None:
        while True:
            if self.sensor_passagem.verificar_sensor_1():
                sleep(0.3)
                if self.sensor_passagem.verificar_sensor_2():
                    self.status_carro = "subindo"
            elif self.sensor_passagem.verificar_sensor_2():
                sleep(0.3)
                if self.sensor_passagem.verificar_sensor_1():
                    self.status_carro = "descendo"
            else:
                self.status_carro = ""
            sleep(0.3)
