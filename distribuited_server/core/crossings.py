from time import sleep
from threading import Thread, Event
from config import main_timing_traffic_light, aux_timing_traffic_light
from server_socket import send_message
from gpio.output_functions import turn_up_port, turn_off_port
from gpio.input_functions import watch_input_event


from gpio.config import PEDESTRIAN_BUTTON_1_C1, PEDESTRIAN_BUTTON_2_C1, MOVEMENT_SENSOR_1_C1, MOVEMENT_SENSOR_2_C1
from gpio.config import PEDESTRIAN_BUTTON_1_C2, PEDESTRIAN_BUTTON_2_C2, MOVEMENT_SENSOR_1_C2, MOVEMENT_SENSOR_2_C2


NUMBER_OF_STATES = 6
MAIN_TRAFFIC_GREEN = 0
AUX_TRAFFIC_GREEN = 3
stop_event = Event()

def handle_traffic_light_change():
    state = MAIN_TRAFFIC_GREEN
    sec = 0

    while True:

        main_curr_state = main_timing_traffic_light[state]
        aux_curr_state = aux_timing_traffic_light[state]
        
        main_active = main_curr_state['active']
        aux_active = aux_curr_state['active']

        handle_lights_on(main_active)
        handle_lights_on(aux_active)
        
        sleep(1)
        sec += 1
        if is_stop_event_active() and is_min_timer(sec, main_curr_state['time_min']):
            handle_lights_off(main_active)
            handle_lights_off(aux_active)
            state = AUX_TRAFFIC_GREEN
            sec = 0
            clear_button()
        elif is_max_timer(sec, main_curr_state['time_max']):
            sec = 0
            handle_lights_off(main_active)
            handle_lights_off(aux_active)
            state = next_state(state)

def handle_input_event(channel):
    print("stoping sign... channel={}".format(channel))
    stop_event.set()


def handle_lights_on(lights):
    for l in lights:
        turn_up_port(l)

def handle_lights_off(lights):
    for l in lights:
        turn_off_port(l)

def clear_button():
     stop_event.clear()

def is_stop_event_active():
    return stop_event.is_set()

def is_max_timer(sec, timer):
    print("sec: {}".format(sec))
    print("max time: {}".format(timer))
    return sec == timer

def is_min_timer(sec, timer):
    print("sec: {}".format(sec))
    print("min time: {}".format(timer))
    return sec >= timer

def next_state(current_state):
    return (current_state + 1) % NUMBER_OF_STATES

def watch_pedestrian_button():
    buttons =  [PEDESTRIAN_BUTTON_1_C1, PEDESTRIAN_BUTTON_2_C1, PEDESTRIAN_BUTTON_1_C2, PEDESTRIAN_BUTTON_2_C2]
    for port in buttons:
        watch_input_event(port, handle_input_event)

def watch_pass_sensor():
    sensors =  [MOVEMENT_SENSOR_1_C1, MOVEMENT_SENSOR_2_C1, MOVEMENT_SENSOR_1_C2, MOVEMENT_SENSOR_2_C2]
    for port in sensors:
        watch_input_event(port, handle_input_event)   

def init_crossing():
    traffic_thread  = Thread(target=handle_traffic_light_change)
    traffic_thread.start()
    
    watch_pedestrian_button()
    watch_pass_sensor()

    traffic_thread.join()
