import socket
import time
import random
import sys

HOST = '127.0.0.1'
PORT = 8000

msg = sys.argv[1].upper()
def produtor():
    """Função para o produtor, que se conecta ao servidor de produção e envia produtos aleatoriamente, esperando um tempo aleatório entre as produções."""
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                print(f'Conectado! Iniciando produção de: [ {msg} ]')
                while True:
                    s.send(msg.encode('utf-8'))
                    print(f'[FABRICADO] Produto {msg} criado e enviado!')
                    tempo = 1
                    print(f'Aguardando {tempo}s para produzir o próximo...')
                    time.sleep(tempo)
        except (ConnectionRefusedError, ConnectionResetError, socket.error):
            print(f'Servidor offline em {HOST}:{PORT}. Tentando conectar em 2 segundos...')
            time.sleep(2)

if __name__ == "__main__":
    produtor()