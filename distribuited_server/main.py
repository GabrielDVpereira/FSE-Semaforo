import config_paths
from gpio.config import config_gpio
from core.crossings import init_crossing

if __name__ == "__main__":
    config_gpio()
    init_crossing()
