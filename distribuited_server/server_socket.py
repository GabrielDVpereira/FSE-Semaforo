import socket
import json
from threading import Thread, Event

HOST = '164.41.98.26'   
PORT = 10160   


connection = None
message = { "night_mode": False, "emergency_mode": False }

def config_socket(crossing):
    global connection
    global message
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dest = (HOST, PORT)
    connection.connect(dest)
    connection.send(json.dumps({"type": "new_connection", "crossing": crossing}))
    while True:
        msg_rec = connection.recv(1024)
        msg_rec = json.loads(msg_rec)
        print(msg_rec)
        message = msg_rec
      
    connection.close()

def init_socket(crossing):
    socket_thread = Thread(target=config_socket, args=(crossing,))
    socket_thread.start()

def get_message():
    global message
    return message

def send_message(message):
    global connection
    if connection:
        connection.send(json.dumps(message))
