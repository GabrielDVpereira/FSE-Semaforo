import socket
import json
import os
import menu
from threading import Thread, Event


HOST = '164.41.98.26'    
PORT = 10160     

connections = []

def connection_thread(con):
    while True:
        msg = con.recv(1024)
        if not msg: break
        msg = json.loads(msg)
        menu.update_menu_info(msg)

    print('Finalizando conexao do cliente')
    con.close()

def config_socket():
    global connections

    print("Initalizing socket...")
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    orig = (HOST, PORT)
    tcp.bind(orig)
    tcp.listen(1)
    while True:
        con, cliente = tcp.accept()
        connections.append(con)
        print('Concetado por: {}'.format(cliente))

        read_message_thread = Thread(target=connection_thread, args=(con,))
        read_message_thread.start()

def send_message(message):
    global connections
    print(message)
    if len(connections) > 0:
        for c in connections:
            c.send(json.dumps(message).encode())

def init_socket():
    socket_thread = Thread(target=config_socket)
    socket_thread.start()