import socket
import json
from threading import Thread, Event

HOST = '127.0.0.1'    
PORT = 10160   

connetion = None

def config_socket():
    global connetion
    print("Initalizing socket...")
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    orig = (HOST, PORT)
    tcp.bind(orig)
    tcp.listen(1)
    while True:
        con, cliente = tcp.accept()
        connetion = con
        print 'Concetado por', cliente

        while True:
            msg = con.recv(1024)
            if not msg: break
            msg = json.loads(msg)
            print cliente, msg

        print 'Finalizando conexao do cliente', cliente
        con.close()

def init_socket():
    socket_thread = Thread(target=config_socket)
    socket_thread.start()

def send_message(message):
    global connetion
    print('send_message: {}'.format(connetion))
    if connetion:
        connetion.send(json.dumps(message))
