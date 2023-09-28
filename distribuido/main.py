from threading import Thread
import json

from components.setup import SetupEstacionamento
from components.carro import Carro
from components.cancela import Cancela
from components.andar import Andar
from distribuido.conexao_tcp import ConectionTCP
from configs.auxiliares import init_config


def main() -> list[Thread]:
    with open("./jsons/configs.json") as json_file:
        configs = json.load(json_file)
    with open(f"./jsons/{configs['nome_arquivo_estacionamento']}") as arquivo:
        estacionamento = json.loads(arquivo.read())
        
    init_config(estacionamento)

    e_setup = SetupEstacionamento()
    carros: list[Carro] = []
    fila_carros_a_sair: list[Carro] = []

    cancela_entrada = Cancela(
        sensor_abertura=e_setup.sensor_abertura_cancela_entrada_a1,
        sensor_fechamento=e_setup.sensor_fechamento_cancela_entrada_a1,
        motor=e_setup.motor_cancela_entrada_a1
    )
    cancela_saida = Cancela(
        sensor_abertura=e_setup.sensor_abertura_cancela_saida_a1,
        sensor_fechamento=e_setup.sensor_fechamento_cancela_saida_a1,
        motor=e_setup.motor_cancela_saida_a1
    )
    
    andar_1 = Andar(
        entrada_1=e_setup.endereco_01_a1.gpio,
        entrada_2=e_setup.endereco_02_a1.gpio,
        entrada_3=e_setup.endereco_03_a1.gpio,
        sensor_de_vagas=e_setup.sensor_de_vaga_a1.gpio,
        sinal_de_lotado_fechado=e_setup.sinal_de_lotado_fechado_a1.gpio,
        num_andar=1)
    andar_2 = Andar(
        entrada_1=e_setup.endereco_01_a2.gpio,
        entrada_2=e_setup.endereco_02_a2.gpio,
        entrada_3=e_setup.endereco_03_a2.gpio,
        sensor_de_vagas=e_setup.sensor_de_vaga_a2.gpio,
        sinal_de_lotado_fechado=e_setup.sinal_de_lotado_fechado_a2.gpio,
        num_andar=2
    )
    
    socket_distribuido = ConectionTCP(
        configs["ip_socket_central"], int(configs["porta_socket"])
    )

    try:
        t_cancela_entrada = Thread(
            target=cancela_entrada.monitorar_entrada, args=(carros,)
        )
        t_cancela_entrada.start()
        
        t_cancela_saida = Thread(
            target=cancela_saida.monitorar_saida, args=(fila_carros_a_sair,)
        )
        t_cancela_saida.start()
        
        t_monitora_vagas_andar_1 = Thread(
            target=andar_1.monitorar_vagas, args=(carros, fila_carros_a_sair)
        )
        t_monitora_vagas_andar_1.start()
        
        t_monitora_vagas_andar_2 = Thread(
            target=andar_2.monitorar_vagas, args=(carros, fila_carros_a_sair)
        )
        t_monitora_vagas_andar_2.start()
        
        t_envia_dados = Thread(
            target=socket_distribuido.enviar_dados, args=(carros,)
        )
        t_envia_dados.start()

        return [
            t_cancela_entrada, 
            t_cancela_saida, 
            t_monitora_vagas_andar_1, 
            t_monitora_vagas_andar_2, 
            t_envia_dados
        ]
        
    except Exception as err:
        print(str(err))


if __name__ == "__main__":
    from configs.auxiliares import init_config
    
    with open("./jsons/configs.json") as json_file:
        configs = json.load(json_file)
    with open(f"./jsons/{configs['nome_arquivo_estacionamento']}") as arquivo:
        estacionamento = json.loads(arquivo.read())
    
    init_config(estacionamento)
    
    threads = main()
    
    for t in threads:
        t.join()
