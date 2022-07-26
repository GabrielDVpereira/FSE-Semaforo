from time import sleep
from threading import Thread, Event
from config import main_timing_traffic_light, aux_timing_traffic_light
from server_socket import send_message
from gpio.output_functions import turn_up_port, turn_off_port

NUMBER_OF_STATES = 6
stop_button_pressed = Event()

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

        print('SEC {}'.format(sec))
        print("PRINCIPAL: {} [STATE]: {}".format(main_active, state))
        print("AUXILIAR: {} [STATE]: {}".format(aux_active, state))
        print('\n')

        sleep(1)
        sec += 1

        if False  and is_button_pressed() and is_min_timer(sec, main_curr_state['time_min']):
            state = 0
            sec = 0
            handle_lights_off(main_active)
            handle_lights_off(aux_active)
            clear_button()
        elif is_max_timer(sec, main_curr_state['time_max']):
            sec = 0
            handle_lights_off(main_active)
            handle_lights_off(aux_active)
            state = next_state(state)

def handle_button_press():
    sleep(15)
    print("stoping sign...")
    stop_button_pressed.set()
    send_message({"message": "Changing lights!"})

def handle_lights_on(lights):
    for l in lights:
        turn_up_port(l)

def handle_lights_off(lights):
    for l in lights:
        turn_off_port(l)

def clear_button():
     stop_button_pressed.clear()

def is_button_pressed():
    return stop_button_pressed.is_set()

def is_max_timer(sec, timer):
    return sec == timer

def is_min_timer(sec, timer):
    return sec >= timer

def next_state(current_state):
    return (current_state + 1) % NUMBER_OF_STATES

def init_crossing():
    traffic_thread  = Thread(target=handle_traffic_light_change)
    # button_thread = Thread(target=handle_button_press)

    traffic_thread.start()
    # button_thread.start()

    traffic_thread.join()
    # button_thread.join()
