import socket
import time
import random
import sys

HOST = '127.0.0.2'
PORT = 8000
msg = "Lista "+sys.argv[1].upper()
def consumidor():
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                print(f'Conectado! Iniciando consumo da: [ {msg} ]')
                while True:
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