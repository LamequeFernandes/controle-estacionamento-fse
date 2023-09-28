from RPi import GPIO


def get_numbers_gpio(estacionamento: dict, type: str):
    gpio_numbers = []
    for andar in ["andar_1", "andar_2"]:
        gpio_numbers += [
            estacionamento[andar][key]["gpio"] 
            for key in estacionamento[andar].keys() 
            if estacionamento[andar][key]["type"] == type
        ]
    return gpio_numbers


def init_config(estacionamento):
    out_list = get_numbers_gpio(estacionamento, "out")
    in_list = get_numbers_gpio(estacionamento, "in")
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    GPIO.setup(out_list, GPIO.OUT)
    GPIO.setup(in_list, GPIO.IN)
