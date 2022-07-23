from time import sleep
from threading import Thread, Event
from queue import Queue
from config import main_timing_traffic_light, aux_timing_traffic_light

NUMBER_OF_STATES = 6
stop_button_pressed = Event()

def handle_traffic_light_change():
    state = 0
    sec = 0

    while True:

        main_curr_state = main_timing_traffic_light[state]
        aux_curr_state = aux_timing_traffic_light[state]

        print('SEC {}'.format(sec))
        print("PRINCIPAL: {} [STATE]: {}".format(main_curr_state['active'], state))
        print("AUXILIAR: {} [STATE]: {}".format(aux_curr_state['active'], state))
        print('\n')

        sleep(1)
        sec += 1

        if is_button_pressed() and is_min_timer(sec, main_curr_state['time_min']):
            state = 0
            sec = 0
            clear_button()
        elif is_max_timer(sec, main_curr_state['time_max']):
            sec = 0
            state = next_state(state)

def handle_button_press():
    sleep(5)
    print("stoping sign...")
    stop_button_pressed.set()

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
    button_thread = Thread(target=handle_button_press)

    traffic_thread.start()
    button_thread.start()

    traffic_thread.join()
    button_thread.join()
