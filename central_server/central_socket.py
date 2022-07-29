import socket
import json

HOST = '164.41.98.26'    
PORT = 10160     


connection = None

def init_socket():
    global connetion
    print("Initalizing socket...")
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    orig = (HOST, PORT)
    tcp.bind(orig)
    tcp.listen(1)
    while True:
        con, cliente = tcp.accept()
        connetion = con
        print('Concetado por: {}'.format(cliente))

        while True:
            msg = con.recv(1024)
            if not msg: break
            msg = json.loads(msg)
            print(cliente, msg)

        print('Finalizando conexao do cliente: {}'.format(cliente))
        con.close()

