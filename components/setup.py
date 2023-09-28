import json


class GpioIO:
    def __init__(self, name: str, gpio: int, type: str, state: bool = False) -> None:
        self.name = name
        self.gpio = gpio
        self.type = type
        self.state = state


class SetupEstacionamento:
    def __init__(self):
        with open("./jsons/configs.json") as json_file:
            configs = json.load(json_file)
        with open(f"./jsons/{configs['nome_arquivo_estacionamento']}") as a:
            data_json = json.loads(a.read())
            andar_1 = data_json["andar_1"]
            andar_2 = data_json["andar_2"]
        
        self.endereco_01_a1 = GpioIO(
            "ENDERECO_01", 
            andar_1["ENDERECO_01"]["gpio"],
            andar_1["ENDERECO_01"]["type"]
        )

        self.endereco_02_a1 = GpioIO(
            "ENDERECO_02", 
            andar_1["ENDERECO_02"]["gpio"],
            andar_1["ENDERECO_02"]["type"]
        )

        self.endereco_03_a1 = GpioIO(
            "ENDERECO_03", 
            andar_1["ENDERECO_03"]["gpio"],
            andar_1["ENDERECO_03"]["type"]
        )

        self.sensor_de_vaga_a1 = GpioIO(
            "SENSOR_DE_VAGA", 
            andar_1["SENSOR_DE_VAGA"]["gpio"],
            andar_1["SENSOR_DE_VAGA"]["type"]
        )

        self.sinal_de_lotado_fechado_a1 = GpioIO(
            "SINAL_DE_LOTADO_FECHADO", 
            andar_1["SINAL_DE_LOTADO_FECHADO"]["gpio"],
            andar_1["SINAL_DE_LOTADO_FECHADO"]["type"]
        )

        self.sensor_abertura_cancela_entrada_a1 = GpioIO(
            "SENSOR_ABERTURA_CANCELA_ENTRADA", 
            andar_1["SENSOR_ABERTURA_CANCELA_ENTRADA"]["gpio"],
            andar_1["SENSOR_ABERTURA_CANCELA_ENTRADA"]["type"]
        )

        self.sensor_fechamento_cancela_entrada_a1 = GpioIO(
            "SENSOR_FECHAMENTO_CANCELA_ENTRADA", 
            andar_1["SENSOR_FECHAMENTO_CANCELA_ENTRADA"]["gpio"],
            andar_1["SENSOR_FECHAMENTO_CANCELA_ENTRADA"]["type"]
        )

        self.motor_cancela_entrada_a1 = GpioIO(
            "MOTOR_CANCELA_ENTRADA", 
            andar_1["MOTOR_CANCELA_ENTRADA"]["gpio"],
            andar_1["MOTOR_CANCELA_ENTRADA"]["type"]
        )

        self.sensor_abertura_cancela_saida_a1 = GpioIO(
            "SENSOR_ABERTURA_CANCELA_SAIDA", 
            andar_1["SENSOR_ABERTURA_CANCELA_SAIDA"]["gpio"],
            andar_1["SENSOR_ABERTURA_CANCELA_SAIDA"]["type"]
        )

        self.sensor_fechamento_cancela_saida_a1 = GpioIO(
            "SENSOR_FECHAMENTO_CANCELA_SAIDA", 
            andar_1["SENSOR_FECHAMENTO_CANCELA_SAIDA"]["gpio"],
            andar_1["SENSOR_FECHAMENTO_CANCELA_SAIDA"]["type"]
        )

        self.motor_cancela_saida_a1 = GpioIO(
            "MOTOR_CANCELA_SAIDA", 
            andar_1["MOTOR_CANCELA_SAIDA"]["gpio"],
            andar_1["MOTOR_CANCELA_SAIDA"]["type"]
        )
        
        self.endereco_01_a2 = GpioIO(
            "ENDERECO_01", 
            andar_2["ENDERECO_01"]["gpio"],
            andar_2["ENDERECO_01"]["type"]
        )

        self.endereco_02_a2 = GpioIO(
            "ENDERECO_02", 
            andar_2["ENDERECO_02"]["gpio"],
            andar_2["ENDERECO_02"]["type"]
        )

        self.endereco_03_a2 = GpioIO(
            "ENDERECO_03", 
            andar_2["ENDERECO_03"]["gpio"],
            andar_2["ENDERECO_03"]["type"]
        )

        self.sensor_de_vaga_a2 = GpioIO(
            "SENSOR_DE_VAGA", 
            andar_2["SENSOR_DE_VAGA"]["gpio"],
            andar_2["SENSOR_DE_VAGA"]["type"]
        )

        self.sinal_de_lotado_fechado_a2 = GpioIO(
            "SINAL_DE_LOTADO_FECHADO", 
            andar_2["SINAL_DE_LOTADO_FECHADO"]["gpio"],
            andar_2["SINAL_DE_LOTADO_FECHADO"]["type"]
        )

        self.sensor_de_passagem_1_a2 = GpioIO(
            "SENSOR_DE_PASSAGEM_1", 
            andar_2["SENSOR_DE_PASSAGEM_1"]["gpio"],
            andar_2["SENSOR_DE_PASSAGEM_1"]["type"]
        )

        self.sensor_de_passagem_2_a2 = GpioIO(
            "SENSOR_DE_PASSAGEM_2", 
            andar_2["SENSOR_DE_PASSAGEM_2"]["gpio"],
            andar_2["SENSOR_DE_PASSAGEM_2"]["type"]
        )
