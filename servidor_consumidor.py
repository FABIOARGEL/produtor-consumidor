import socket
import threading
import time

HOST = '127.0.0.2'
PORT = 8000
PRODUTOS = {'Lista A': [],'Lista B': [],'Lista C': []}


def mensagens(conn, addr):
    print(f'[CLIENTE CONECTADO] {addr[0]}:{addr[1]}')
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                print(f'[CLIENTE DESCONECTADO] {addr[0]}:{addr[1]}')
                break
            msg = data.decode('utf-8').strip()
            if "Lista " + msg in PRODUTOS:
                PRODUTOS["Lista " + msg].append(msg)
                print(f'[SERVIDOR DE CONSUMO] Recebeu produto "{msg}" | Total na Lista {msg}: {len(PRODUTOS["Lista " + msg])}')
                conn.send('ok'.encode('utf-8'))
            elif msg in PRODUTOS:
                while not PRODUTOS[msg]:
                    time.sleep(1)
                produto = PRODUTOS[msg].pop(0)
                print(f'[ENTREGA] Consumidor levou "{produto}" da {msg} | Restam: {len(PRODUTOS[msg])}')
                conn.send(produto.encode('utf-8'))

def servidor_consumidor():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f'[SERVIDOR DE CONSUMO] Ouvindo na porta {PORT}...')
        while True:
            conn, addr = s.accept()
            t = threading.Thread(
                target=mensagens,
                args=(conn, addr)
            )

            t.start()

if __name__ == "__main__":
    servidor_consumidor()