[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/OJtG4ZlI)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-718a45dd9cf7e7f842a935f5ebbe5719a5e09af4491e668f4dbf3b35d5cca122.svg)](https://classroom.github.com/online_ide?assignment_repo_id=11145457&assignment_repo_type=AssignmentRepo)


# Trabalho 1 (2023-1) - Controle de Estacionamentos

Trabalho 1 da disciplina de Fundamentos de Sistemas Embarcados (2023/1)


## Sobre

Este trabalho tem por objetivo a criação de um sistema distribuído para o controle e monitoramento de estacionamentos comerciais. Dentre os itens controlados teremos a entrada e saída de veículos, a ocupação de cada vaga individualmente, a ocupação do estacionamento como um todo e a cobrança por tempo de permanência.


## Requisitos

- Python 3.9 ou superior
- Biblioteca RPi.GPIO (https://pypi.org/project/RPi.GPIO/)


## Execução

Existem duas formas de executar o projeto.
- A primeira forma consiste em executar o arquivo ```main.py```, presente na raiz do projeto. Dessa forma ele executa o distribuido e a central paralelamente, sem a necessidade de abrir dois terminais. Exemplo de execução:
```
python3 main.py
```
- A segunda forma, é executar o arquivo ```main.py``` presente na pasta __central__ e o arquivo ```main.py``` presente na pasta __distribuido__. Exemplo de execução:
```
python3 -m central.main  # terminal 1
```

```
python3 -m distribuido.main  # terminal 2
```

**Obs**: Caso queira alterar o IP e/ou PORTA padrão do servidor central e configurações de estacionamento(GPIO), atualizar as variáveis no json ```jsons/configs.json```


## Apresentação

Link da aprensetação: https://youtu.be/9NGLgZkcz24
