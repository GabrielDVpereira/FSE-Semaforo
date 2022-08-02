import config_paths
from gpio.config import config_gpio
from core.crossings import init_crossing
from server_socket import init_socket
import json
import sys


if __name__ == "__main__":
    config_path = sys.argv[1]
    ports = None
    with open(config_path) as json_file:
        ports = json.load(json_file)
    
    
    config_gpio(ports)
    # init_socket()
    init_crossing(ports)
