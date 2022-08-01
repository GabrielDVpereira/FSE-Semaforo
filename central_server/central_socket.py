import socket
import json
import os
import menu
from threading import Thread, Event


HOST = '164.41.98.26'    
PORT = 10160     


connection = None

def config_socket():
    global connection
    print("Initalizing socket...")
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    orig = (HOST, PORT)
    tcp.bind(orig)
    tcp.listen(1)
    while True:
        con, cliente = tcp.accept()
        connection = con
        print('Concetado por: {}'.format(cliente))

        while True:
            msg = con.recv(1024)
            if not msg: break
            msg = json.loads(msg)
            menu.update_menu_info(msg)

        print('Finalizando conexao do cliente: {}'.format(cliente))
        con.close()

def send_message(message):
    global connection
    print(message)
    if connection:
        connection.send(json.dumps(message).encode())

def init_socket():
    socket_thread = Thread(target=config_socket)
    socket_thread.start()