from central_socket import init_socket
from menu import init_menu
import menu
import signal

if __name__ == "__main__":
    signal.signal(signal.SIGINT, menu.signal_handler)
    init_socket()
    init_menu()
