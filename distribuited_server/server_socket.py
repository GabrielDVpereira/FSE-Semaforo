import socket
import json
from threading import Thread, Event

HOST = '164.41.98.26'   
PORT = 10160   


connection = None
def config_socket():
    global connection
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dest = (HOST, PORT)
    connection.connect(dest)

    while True:
        msg_rec = connection.recv(1024)
        msg_rec = json.loads(msg_rec)
        print(msg_rec)
      
    connection.close()

def init_socket():
    socket_thread = Thread(target=config_socket)
    socket_thread.start()

def send_message(message):
    global connection
    if connection:
        connection.send(json.dumps(message))
