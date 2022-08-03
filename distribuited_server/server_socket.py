import socket
import json
from threading import Thread, Event

connection = None
message = { "night_mode": False, "emergency_mode": False }

def config_socket(crossing, tcp_ip_address, tcp_port):
    global connection
    global message
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dest = (tcp_ip_address, tcp_port)
    connection.connect(dest)
    try:
        connection.send(json.dumps({"type": "new_connection", "crossing": crossing}))
        while True:
            msg_rec = connection.recv(1024)
            msg_rec = json.loads(msg_rec)
            print(msg_rec)
            message = msg_rec
        
    except socket.error as e:
        print(e)
        connection.close()

def init_socket(crossing, tcp_ip_address, tcp_port):
    socket_thread = Thread(target=config_socket, args=(crossing,tcp_ip_address, tcp_port))
    socket_thread.start()

def get_message():
    global message
    return message

def send_message(message):
    global connection
    try:
        if connection:
            connection.send(json.dumps(message))
    except socket.error as e:
        print(e)

