import RPi.GPIO as GPIO
from time import sleep


''' CROSS 1  '''
TRAFFIC_LIGHT_1_GREEN_C1 = 1
TRAFFIC_LIGHT_1_YELLOW_C1 = 26
TRAFFIC_LOGHT_1_RED_C1 = 21

TRAFFIC_LIGHT_2_GREEN_C1 = 20
TRAFFIC_LIGHT_2_YELLOW_C1 = 16
TRAFFIC_LIGHT_2_RED_C1 = 12

PEDESTRIAN_BUTTON_1_C1 = 8
PEDESTRIAN_BUTTON_2_C1 = 7

MOVEMENT_SENSOR_1_C1 = 14
MOVEMENT_SENSOR_2_C1 = 15

SPEED_SENSOR_1_A_C1 = 18
SPEED_SENSOR_1_B_C1 = 23

SPEED_SENSOR_2_A_C1 = 24
SPEED_SENSOR_2_B_C1 = 25

''' CROSS 2  '''
TRAFFIC_LIGHT_1_GREEN_C2 = 2
TRAFFIC_LIGHT_1_YELLOW_C1_C2 = 3
TRAFFIC_LOGHT_1_RED_C2 = 11

TRAFFIC_LIGHT_2_GREEN_C2 = 0
TRAFFIC_LIGHT_2_YELLOW_C2 = 5
TRAFFIC_LIGHT_2_RED_C2 = 6

PEDESTRIAN_BUTTON_1_C2 = 10
PEDESTRIAN_BUTTON_2_C2 = 9

MOVEMENT_SENSOR_1_C2 = 4
MOVEMENT_SENSOR_2_C2 = 17 

SPEED_SENSOR_1_A_C2 = 27 
SPEED_SENSOR_1_B_C2 = 22

SPEED_SENSOR_2_A_C2 = 13
SPEED_SENSOR_2_B_C2 = 19

aux_red_lights = [TRAFFIC_LOGHT_1_RED_C1, TRAFFIC_LOGHT_1_RED_C2]
aux_green_lights = [TRAFFIC_LIGHT_1_GREEN_C1, TRAFFIC_LIGHT_1_GREEN_C2]
aux_yellow_lights = [TRAFFIC_LIGHT_1_YELLOW_C1, TRAFFIC_LIGHT_1_YELLOW_C1_C2]

main_red_lights = [TRAFFIC_LIGHT_2_RED_C1, TRAFFIC_LIGHT_2_RED_C2]
main_green_lights = [TRAFFIC_LIGHT_2_GREEN_C1, TRAFFIC_LIGHT_2_GREEN_C2]
main_yellow_lights = [TRAFFIC_LIGHT_2_YELLOW_C1, TRAFFIC_LIGHT_2_YELLOW_C2]

outputs = main_red_lights + main_green_lights + main_yellow_lights + aux_red_lights + aux_green_lights + aux_yellow_lights

inputs_buttons = [
    PEDESTRIAN_BUTTON_1_C1,  
    PEDESTRIAN_BUTTON_2_C1,  
    PEDESTRIAN_BUTTON_1_C2,
    PEDESTRIAN_BUTTON_2_C2,  
]

intputs_sensors = [
    MOVEMENT_SENSOR_1_C1,
    MOVEMENT_SENSOR_2_C1,
    MOVEMENT_SENSOR_1_C2, 
    MOVEMENT_SENSOR_2_C2, 
    SPEED_SENSOR_1_A_C1,
    SPEED_SENSOR_1_B_C1,
    SPEED_SENSOR_1_A_C2, 
    SPEED_SENSOR_1_B_C2,
    SPEED_SENSOR_2_A_C1,
    SPEED_SENSOR_2_B_C1,
    SPEED_SENSOR_2_A_C2,
    SPEED_SENSOR_2_B_C2,
]


def reset_outputs():
    for out in outputs:
        GPIO.output(out, GPIO.LOW)

def set_outputs():
    for out in outputs:
        GPIO.setup(out, GPIO.OUT)

def set_input_buttons():
    for b in inputs_buttons:
        GPIO.setup(b, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def set_input_sensors():
    for s in intputs_sensors:
        GPIO.setup(s, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def config_gpio():
    print('Setting up gpio ports...')
    GPIO.setmode(GPIO.BCM)
    set_outputs()
    set_input_buttons()
    set_input_sensors()
    reset_outputs()





