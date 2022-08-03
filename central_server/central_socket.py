import socket
import json
import menu
from threading import Thread

connections = []

def connection_thread(con):
    while True:
        try:
            msg = con.recv(1024)
            if not msg: break
            msg = json.loads(msg)
            menu.update_menu_info(msg)
        except ValueError:
            print("Decoding JSON has failed")

def config_socket(tcp_ip_address, tcp_port):
    global connections

    print("Initalizing socket...")
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    orig = (tcp_ip_address, tcp_port)
    tcp.bind(orig)
    tcp.listen(1)
    while True:
        con, client = tcp.accept()
        connections.append(con)
        read_message_thread = Thread(target=connection_thread, args=(con,))
        read_message_thread.start()

def send_message(message):
    global connections
    print(message)
    if len(connections) > 0:
        for c in connections:
            c.send(json.dumps(message).encode())

def init_socket(tcp_ip_address, tcp_port):
    global connections
    socket_thread = Thread(target=config_socket, args=(tcp_ip_address, tcp_port))
    socket_thread.start()

    for con in connections:
        con.close()