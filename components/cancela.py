from components.carro import Carro
from components.setup import GpioIO
from datetime import datetime
from RPi import GPIO
from time import sleep


class Cancela:
    def __init__(
            self,
            sensor_abertura: GpioIO, 
            sensor_fechamento: GpioIO, 
            motor: GpioIO
    ) -> None:
        self.sensor_abertura = sensor_abertura
        self.sensor_fechamento = sensor_fechamento
        self.motor = motor
    
    def verificar_sensor_abertura(self) -> bool:
        return GPIO.input(self.sensor_abertura.gpio) == 1
    
    def verificar_sensor_fechamento(self) -> bool:
        return GPIO.input(self.sensor_fechamento.gpio) == 1
    
    def levantar_cancela(self) -> None:
        GPIO.output(self.motor.gpio, GPIO.HIGH)
        self.motor.state = True
    
    def abaixar_cancela(self) -> None:
        GPIO.output(self.motor.gpio, GPIO.LOW)
        self.motor.state = False

    def monitorar_entrada(self, lista_carros: list[Carro]) -> None:
        while True:
            if self.verificar_sensor_abertura():
                if not self.motor.state:
                    new_carro = Carro()
                    lista_carros.append(new_carro)
                self.levantar_cancela()
            if self.verificar_sensor_fechamento():
                self.abaixar_cancela()
            sleep(0.2)
            
    def monitorar_saida(self, fila_saida_carros: list[Carro]) -> None:
        while True:
            if self.verificar_sensor_abertura() and len(fila_saida_carros) > 0:
                if not self.motor.state:
                    fila_saida_carros[0].datatime_saida = datetime.now()
                    fila_saida_carros.pop(0)
                self.levantar_cancela()
            if self.verificar_sensor_fechamento():
                self.abaixar_cancela()
            sleep(0.2)
