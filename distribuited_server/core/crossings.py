from time import sleep
from threading import Thread, Event
from config import main_timing_traffic_light, aux_timing_traffic_light
from server_socket import send_message
from gpio.output_functions import turn_up_port, turn_off_port
from gpio.input_functions import watch_input_event
from datetime import datetime
from utils import play_sound



from gpio.config import car_sensors, inputs_buttons, speed_sensors


NUMBER_OF_STATES = 6
MAIN_TRAFFIC_GREEN_STATE = 0
AUX_TRAFFIC_GREEN_STATE = 3
MAX_SPEED_PERMITTED = 60

car_count_dict = {
    "car_count_1": 0,
    "car_count_2": 0,
    "car_count_3": 0,
    "car_count_4": 0,
}

stop_event = Event()

def handle_traffic_light_change():
    state = MAIN_TRAFFIC_GREEN_STATE
    sec = 0

    while True:
        update_central_server_car_count(sec)
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
            state = AUX_TRAFFIC_GREEN_STATE
            sec = 0
            clear_button()
        elif is_max_timer(sec, main_curr_state['time_max']):
            sec = 0
            handle_lights_off(main_active)
            handle_lights_off(aux_active)
            state = next_state(state)

def handle_input_event(channel):
    global car_count_dict
    print("stoping sign... channel={}".format(channel))
    if channel in car_sensors:
        index = car_sensors.index(channel)
        event_type = "car_count_{}".format(index+1)
        car_count_dict[event_type]+=1

    stop_event.set()

date = None
def handle_speed_event(channel):
    global date
    print("A car has passed {}".format(channel))
    
    if not date:
        date = datetime.now()
        return
    
    time = datetime.now() - date 
    speed = (1 / time.total_seconds()) * 3.6

    if speed > MAX_SPEED_PERMITTED:
        play_sound()
    
    print("time: {}".format(time.total_seconds()))
    print("speed: {} km/h".format(speed))
    send_message({"type": "car_speed", "data": speed })
    date = None


def update_central_server_car_count(sec):
    global car_count_dict
    should_updade_central = sec % 2 == 0
    if should_updade_central:
        send_message({"type": "car_count", "data": car_count_dict })


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
    for port in inputs_buttons:
        watch_input_event(port, handle_input_event)

def watch_pass_sensor():
    for port in car_sensors:
        watch_input_event(port, handle_input_event)   

def watch_speed_sensor():
    for port in speed_sensors:
        watch_input_event(port, handle_speed_event)     

def init_crossing():
    traffic_thread  = Thread(target=handle_traffic_light_change)
    traffic_thread.start()
    
    watch_pedestrian_button()
    watch_pass_sensor()
    watch_speed_sensor()

    traffic_thread.join()
