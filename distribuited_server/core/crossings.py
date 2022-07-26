from time import sleep
from threading import Thread, Event
from config import main_timing_traffic_light, aux_timing_traffic_light
from server_socket import send_message
from gpio.output_functions import turn_up_port, turn_off_port
from gpio.input_functions import watch_input_event


from gpio.config import PEDESTRIAN_BUTTON_1_C1, PEDESTRIAN_BUTTON_2_C1


NUMBER_OF_STATES = 6
stop_button_1_pressed = Event()
stop_button_2_pressed = Event()

def handle_traffic_light_change():
    state = 0
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

        if is_button_pressed() and is_min_timer(sec, main_curr_state['time_min']):
            handle_lights_off(main_active)
            handle_lights_off(aux_active)
            state = 3 if stop_button_1_pressed.is_set() else 0
            sec = 0
            clear_button()
        elif is_max_timer(sec, main_curr_state['time_max']):
            sec = 0
            handle_lights_off(main_active)
            handle_lights_off(aux_active)
            state = next_state(state)

def handle_button_press(channel):
    print("stoping sign... channel={}".format(channel))

    if channel == PEDESTRIAN_BUTTON_1_C1:
        stop_button_1_pressed.set()
        return

    stop_button_2_pressed.set()

def handle_lights_on(lights):
    for l in lights:
        turn_up_port(l)

def handle_lights_off(lights):
    for l in lights:
        turn_off_port(l)

def clear_button():
     stop_button_1_pressed.clear()
     stop_button_2_pressed.clear()

def is_button_pressed():
    return stop_button_1_pressed.is_set() or stop_button_2_pressed.is_set()

def is_max_timer(sec, timer):
    return sec == timer

def is_min_timer(sec, timer):
    print(sec)
    print(timer)
    return sec >= timer

def next_state(current_state):
    return (current_state + 1) % NUMBER_OF_STATES

def watch_pedestrian_button_1_c1():
    watch_input_event(PEDESTRIAN_BUTTON_1_C1, handle_button_press)

def watch_pedestrian_button_2_c1():
    watch_input_event(PEDESTRIAN_BUTTON_2_C1, handle_button_press)

def init_crossing():
    traffic_thread  = Thread(target=handle_traffic_light_change)
    traffic_thread.start()
    
    watch_pedestrian_button_1_c1()
    watch_pedestrian_button_2_c1()

    traffic_thread.join()
