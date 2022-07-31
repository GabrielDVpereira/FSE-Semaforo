from gpio.config import main_red_lights, main_green_lights, main_yellow_lights
from gpio.config import aux_red_lights, aux_green_lights, aux_yellow_lights

main_timing_traffic_light = [
    {'active': main_red_lights, 'time_max': 1, 'time_min': 1 },
    {'active': main_green_lights, 'time_max': 20, 'time_min': 10 },
    {'active': main_yellow_lights, 'time_max': 3, 'time_min': 3 },
    {'active': main_red_lights, 'time_max': 1, 'time_min': 1 },
    {'active': main_red_lights, 'time_max': 10, 'time_min': 5 },
    {'active': main_red_lights, 'time_max': 3, 'time_min': 3 },
    {'active': main_yellow_lights, 'time_max': 1, 'time_min': 1 },
]

aux_timing_traffic_light = [
    {'active': aux_red_lights, 'time_max': 1, 'time_min': 1 },
    {'active': aux_red_lights, 'time_max': 20, 'time_min': 10 },
    {'active': aux_red_lights, 'time_max': 3, 'time_min': 3 },
    {'active': aux_red_lights, 'time_max': 1, 'time_min': 1 },
    {'active': aux_green_lights, 'time_max': 10, 'time_min': 5 },
    {'active': aux_yellow_lights, 'time_max': 3, 'time_min': 3 },
    {'active': aux_yellow_lights, 'time_max': 1, 'time_min': 1 },
]


