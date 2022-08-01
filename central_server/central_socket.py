import socket
import json
import os
from menu import update_menu_info
from threading import Thread, Event


HOST = '164.41.98.26'    
PORT = 10160     


connection = None

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
        print('Concetado por: {}'.format(cliente))

        while True:
            msg = con.recv(1024)
            if not msg: break
            msg = json.loads(msg)
            update_menu_info(msg)

        print('Finalizando conexao do cliente: {}'.format(cliente))
        con.close()

def init_socket():
    socket_thread = Thread(target=config_socket)
    socket_thread.start()