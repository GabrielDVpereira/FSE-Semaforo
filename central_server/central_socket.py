import socket
import json

HOST = '127.0.0.1'    
PORT = 3333     

def init_socket():
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dest = (HOST, PORT)
    tcp.connect(dest)
    print 'Para sair use CTRL+X\n'
    msg = raw_input()
    while msg <> '\x18':
        data = {"message": msg}
        tcp.send (json.dumps(data))
        msg_rec = tcp.recv(1024)
        msg_rec = json.loads(msg_rec)
        print msg_rec['message']
        msg = raw_input()
    tcp.close()