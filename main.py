from distribuido.main import main as distribuido
from central.main import main as central


if __name__ == "__main__":
    try:
        threads_distribuido = distribuido()
        threads_central = central()

        for thread in threads_distribuido:
            thread.join()
            
        for thread in threads_central:
            thread.join()

            
    except Exception as erro:
        if Exception == KeyboardInterrupt:
            print("Finalizando execução...")
        else:
            print(str(erro))
        exit(0)
