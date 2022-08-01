from time import sleep
from threading import Thread, Event
from config import main_timing_traffic_light, aux_timing_traffic_light
from server_socket import send_message, get_message
from gpio.output_functions import turn_up_port, turn_off_port
from gpio.input_functions import watch_input_event, remove_input_event
from datetime import datetime
from utils import play_sound
from gpio.config import aux_red_lights, main_red_lights




from gpio.config import car_sensors, inputs_buttons, speed_sensors, speed_sensors_b, crossing_1, crossing_2, car_sensors_1, car_sensors_2


NUMBER_OF_STATES = 6
INITIAL_STATE = 0
MAIN_TRAFFIC_GREEN_STATE = 1
AUX_TRAFFIC_GREEN_STATE = 3
YELLOW_STATE = 6
MAX_SPEED_PERMITTED = 60

car_count = [
    {
        "line1": 0,
        "line2": 0,
    },
    {
        "line1": 0,
        "line2": 0,
    },
]

stop_event = Event()

state = INITIAL_STATE
def handle_traffic_light_change():
    global state
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
        if is_emergency_mode():
            print("if is_emergency_mode()")
            handle_lights_off(main_active)
            handle_lights_off(aux_active)
            state = MAIN_TRAFFIC_GREEN_STATE
        elif is_night_mode():
            print("if is_night_mode()")
            handle_lights_off(main_active)
            handle_lights_off(aux_active)
            sleep(1)
            state = YELLOW_STATE
        elif is_stop_event_active() and is_min_timer(sec, main_curr_state['time_min']):
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

def is_emergency_mode():
    info = get_message()
    print("[is_emergency_mode]")
    print(info)
    return info['emergency_mode']

def is_night_mode():
    info = get_message()
    print("[is_night_mode]")
    print(info)
    return info['night_mode']


def handle_pedestrean_button(channel):
    print("stoping sign... channel={}".format(channel))
    
    if is_aux_red_lights():
        stop_event.set()

def handle_car_sensor(channel):
    global car_count
    print("[handle_car_sensor]", channel)
    
    crossing = get_crossing(channel)
    crossing_index = crossing - 1

    if channel in car_sensors_1:
        car_count[crossing_index]['line1']+=1
    else:
        car_count[crossing_index]['line2']+=1

    if is_aux_red_lights():
        stop_event.set()

    remove_input_event(channel)
    watch_input_event(channel, handle_input_down_event, False)   

def handle_input_down_event(channel):
    print("[handle_input_down_event]", channel)
    remove_input_event(channel)

    if is_aux_red_lights():
        send_message({"type": "red_light_infraction", "crossing": get_crossing(channel) })
        play_sound()


    watch_input_event(channel, handle_car_sensor) 


 


date = None
def handle_speed_event(channel):
    global date
    print("[handle_speed_event]",channel)

    if not date and channel not in speed_sensors_b: 
        return

    if not date:
        date = datetime.now()
        return
    
    time = datetime.now() - date 
    speed = (1 / time.total_seconds()) * 3.6

    if speed > MAX_SPEED_PERMITTED:
        send_message({"type": "speed_infraction", "crossing": get_crossing(channel) })
        play_sound()

    if is_main_red_lights():
        send_message({"type": "red_light_infraction", "crossing": get_crossing(channel) })
        play_sound()
    
    # TODO: enviar contagem de carros para servidor central
    print("time: {}".format(time.total_seconds()))
    print("speed: {} km/h".format(speed))
    send_message({"type": "car_speed", "data": speed, "crossing": get_crossing(channel) })
    date = None


def update_central_server_car_count(sec):
    global car_count
    should_updade_central = sec % 2 == 0

    if should_updade_central:
        send_message({"type": "car_count", "data": car_count[0], "crossing": 1 })
        send_message({"type": "car_count", "data": car_count[1], "crossing": 2 })


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
    return sec >= timer

def is_min_timer(sec, timer):
    return sec >= timer

def is_aux_red_lights():
    global state
    aux_state_lights  = aux_timing_traffic_light[state]['active']
    return aux_state_lights == aux_red_lights

def is_main_red_lights():
    global state
    main_state_lights = main_timing_traffic_light[state]['active']
    return main_state_lights == main_red_lights

def get_crossing(channel):
    if channel in crossing_1: return 1
    elif channel in crossing_2: return 2
    return 0

def next_state(current_state):
    if current_state == YELLOW_STATE: return 0
    return (current_state + 1) % NUMBER_OF_STATES

def watch_pedestrian_button():
    for port in inputs_buttons:
        watch_input_event(port, handle_pedestrean_button)

def watch_pass_sensor():
    for port in car_sensors:
        watch_input_event(port, handle_car_sensor)   

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
