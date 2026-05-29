import socket
import time
import random

HOST = '127.0.0.2'
PORT = 8000

def consumidor():
    """Função para o consumidor, que se conecta ao servidor de consumo e solicita produtos aleatoriamente, esperando um tempo aleatório entre as solicitações."""
    opcoes_produtos = ['Lista A', 'Lista B', 'Lista C']
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                print('Conectado! Iniciando consumo...')
                while True:
                    msg = random.choice(opcoes_produtos)
                    tempo = random.randint(7, 10)
                    print(f'Solicitando produto da {msg}...')
                    s.send(msg.encode('utf-8'))
                    resposta = s.recv(1024).decode('utf-8')
                    if not resposta:
                        raise socket.error("Conexão fechada pelo servidor")
                    print(f'[RECEBIDO] Consumiu produto: "{resposta}" da {msg}')
                    time.sleep(tempo)
        except (ConnectionRefusedError, ConnectionResetError, socket.error):
            print(f'Servidor offline em {HOST}:{PORT}. Tentando conectar em 2 segundos...')
            time.sleep(2)

if __name__ == "__main__":
    consumidor()