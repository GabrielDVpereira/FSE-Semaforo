from time import sleep
from config import main_timing_traffic_light, aux_timing_traffic_light

NUMBER_OF_STATES = 6

def handle_max_traffic_light_change():
    state = 0
    while True:
        state = next_state(state)
        

def next_state(current_state):
    return (current_state + 1) % NUMBER_OF_STATES

print(main_timing_traffic_light, aux_timing_traffic_light)
handle_max_traffic_light_change()