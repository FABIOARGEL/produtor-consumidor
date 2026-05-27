import socket
import threading
import time

HOST = '127.0.0.1'
PORT = 8000

PRODUTOS = {'Lista A': [],'Lista B': [],'Lista C': []}

def clientes_produtores(conn, addr):
    print(f'[PRODUTOR CONECTADO] {addr[0]}:{addr[1]}')
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                print(f'[PRODUTOR DESCONECTADO] {addr[0]}:{addr[1]}')
                break
            msg = data.decode('utf-8').upper().strip()
            if "Lista " + msg in PRODUTOS:
                PRODUTOS["Lista " + msg].append(msg)
                status = " | ".join([f"{k}: {len(v)} itens" for k, v in PRODUTOS.items()])
                print(f'[PRODUÇÃO] Produto "{msg}" adicionado à fila! ({status})')

def enviar_para_consumidor():
    C_HOST = '127.0.0.2'
    C_PORT = 8000
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((C_HOST, C_PORT))
                print('[CONEXÃO] Interligado com sucesso ao Servidor Consumidor!')
                while True:
                    for produto in PRODUTOS:
                        if PRODUTOS[produto]:
                            msg = PRODUTOS[produto][0]
                            try:
                                s.send(msg.encode('utf-8'))
                                resposta = s.recv(1024).decode('utf-8')
                                if not resposta:
                                    raise socket.error("Conexão fechada pelo servidor")
                                if resposta.strip().lower() == 'ok':
                                    PRODUTOS[produto].pop(0)
                                    print(f'[TRANSFERÊNCIA] Enviado "{msg}" para servidor de consumo')
                            except (socket.error, ConnectionResetError) as e:
                                raise e
                    time.sleep(0.1)
        except (ConnectionRefusedError, ConnectionResetError, socket.error):
            print(f'[CONEXÃO] Servidor Consumidor offline em {C_HOST}:{C_PORT}. Tentando novamente em 2 segundos...')
            time.sleep(2)

def servidor_produtor():
    consumidor = threading.Thread(
        target=enviar_para_consumidor,
        daemon=True
    )
    consumidor.start()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f'[SERVIDOR DE PRODUÇÃO] Ouvindo na porta {PORT}...')
        while True:
            conn, addr = s.accept()
            t = threading.Thread(
                target=clientes_produtores,
                args=(conn, addr)
            )
            t.start()

if __name__ == "__main__":
    servidor_produtor()