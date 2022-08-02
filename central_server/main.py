from central_socket import init_socket
from menu import init_menu
import menu
import signal
import sys

if __name__ == "__main__":
    signal.signal(signal.SIGINT, menu.signal_handler)

    if len(sys.argv) < 3:
        print("[ERRO] Modo de uso: python main.py [IP_SERVIDOR_TCP] [PORTA_SERVIDOR_TCP]")
        sys.exit()

    tcp_ip_address = sys.argv[1]
    tcp_port = int(sys.argv[2])
    
    init_socket(tcp_ip_address, tcp_port)
    init_menu()
