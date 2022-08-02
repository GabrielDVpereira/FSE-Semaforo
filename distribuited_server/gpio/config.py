import RPi.GPIO as GPIO

def set_outputs(outputs):
    for port in outputs:
        GPIO.setup(outputs[port], GPIO.OUT)

def set_input_buttons(buttons):
    for port in buttons:
        GPIO.setup(buttons[port], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def set_input_sensors(sensors):
    for port in sensors:
        GPIO.setup(sensors[port], GPIO.IN, pull_up_down=GPIO.PUD_UP)

current_ports = None
def config_gpio(ports):
    global current_ports
    current_ports = ports

    print('Setting up gpio ports...')
    GPIO.setmode(GPIO.BCM)
    set_outputs(ports['outputs'])
    set_input_buttons(ports['buttons'])
    set_input_sensors(ports['speed_sensors'])
    set_input_sensors(ports['car_sensors'])





