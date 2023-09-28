from threading import Thread
from central.utils import Utils


def main() -> list[Thread]:
    utils = Utils()

    t_menu = Thread(target=utils.menu_principal, args=())
    t_menu.start()
    
    t_verificar_lotacao = Thread(target=utils.verificar_lotacao, args=())
    t_verificar_lotacao.start()
    
    t_socket = Thread(target=utils.conectar_socket(), args=())
    t_socket.start()
    

    return [t_socket, t_menu, t_verificar_lotacao]


if __name__ == "__main__":
    from configs.auxiliares import init_config
    import json
    
    with open("./jsons/configs.json") as json_file:
        configs = json.load(json_file)
    with open(f"./jsons/{configs['nome_arquivo_estacionamento']}") as arquivo:
        estacionamento = json.loads(arquivo.read())
    
    init_config(estacionamento)
    
    threads = main()
    
    for t in threads:
        t.join()
