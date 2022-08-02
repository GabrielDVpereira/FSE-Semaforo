import config_paths
from gpio.config import config_gpio
from core.crossings import init_crossing
from server_socket import init_socket
import json
import sys


if __name__ == "__main__":

    if len(sys.argv) < 4:
        print("[ERRO] Modo de uso: python main.py [ARQUIVO_CONFIGURACAO] [IP_SERVIDOR_TCP] [PORTA_SERVIDOR_TCP]")
        sys.exit()

    config_path = sys.argv[1]
    tcp_ip_address = sys.argv[2]
    tcp_port = int(sys.argv[3])

    ports = None
    with open(config_path) as json_file:
        ports = json.load(json_file)
    
    config_gpio(ports)
    init_socket(ports['crossing'], tcp_ip_address, tcp_port)
    init_crossing(ports)
