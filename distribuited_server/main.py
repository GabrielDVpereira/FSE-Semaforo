import config_paths
from gpio.config import config_gpio
from core.crossings import init_crossing
from server_socket import init_socket

if __name__ == "__main__":
    config_gpio()
    # init_socket()
    init_crossing()
