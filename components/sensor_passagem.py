from RPi import GPIO
from time import sleep
from components.setup import GpioIO


class SensorPassagem:
    def __init__(self, sensor_1: GpioIO, sensor_2: GpioIO) -> None:
        self.sensor_1 = sensor_1
        self.sensor_2 = sensor_2
        self.status_carro = ""
    
    def verificar_sensor_1(self) -> bool:
        return GPIO.input(self.sensor_1.gpio) == 1
    
    def verificar_sensor_2(self) -> bool:
        return GPIO.input(self.sensor_2.gpio) == 1
