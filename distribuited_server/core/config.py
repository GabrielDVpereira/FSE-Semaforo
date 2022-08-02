def get_main_states(output_ports):
    main_timing_traffic_light = [
        {'active': output_ports['traffic_light_red_2'], 'time_max': 1, 'time_min': 1 },
        {'active': output_ports['traffic_light_green_2'], 'time_max': 20, 'time_min': 10 },
        {'active': output_ports['traffic_light_yellow_2'], 'time_max': 3, 'time_min': 3 },
        {'active': output_ports['traffic_light_red_2'], 'time_max': 1, 'time_min': 1 },
        {'active': output_ports['traffic_light_red_2'], 'time_max': 10, 'time_min': 5 },
        {'active': output_ports['traffic_light_red_2'], 'time_max': 3, 'time_min': 3 },
        {'active': output_ports['traffic_light_yellow_2'], 'time_max': 1, 'time_min': 1 },
    ]
    return main_timing_traffic_light

def get_aux_states(output_ports):
    aux_timing_traffic_light = [
        {'active': output_ports['traffic_light_red_1'], 'time_max': 1, 'time_min': 1 },
        {'active': output_ports['traffic_light_red_1'], 'time_max': 20, 'time_min': 10 },
        {'active': output_ports['traffic_light_red_1'], 'time_max': 3, 'time_min': 3 },
        {'active': output_ports['traffic_light_red_1'], 'time_max': 1, 'time_min': 1 },
        {'active': output_ports['traffic_light_green_1'], 'time_max': 10, 'time_min': 5 },
        {'active': output_ports['traffic_light_yellow_1'], 'time_max': 3, 'time_min': 3 },
        {'active': output_ports['traffic_light_yellow_1'], 'time_max': 1, 'time_min': 1 },
    ]
    return aux_timing_traffic_light


