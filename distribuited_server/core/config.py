# from gpio.congig import SEMAFORO_1_VERDE_C1, SEMAFORO_1_AMARELO_C1, SEMAFORO_1_VERMELHO_C1, SEMAFORO_2_VERDE_C1, SEMAFORO_2_AMARELO_C1, SEMAFORO_2_VERMELHO_C1, SEMAFORO_1_VERDE_C2, SEMAFORO_1_AMARELO_C2, SEMAFORO_1_VERMELHO_C2, SEMAFORO_2_VERDE_C2, SEMAFORO_2_AMARELO_C2, SEMAFORO_2_VERMELHO_C2


''' CRUZAMENTO 1  '''
SEMAFORO_1_VERDE_C1 = 1
SEMAFORO_1_AMARELO_C1 = 26
SEMAFORO_1_VERMELHO_C1 = 21

SEMAFORO_2_VERDE_C1 = 20
SEMAFORO_2_AMARELO_C1 = 16
SEMAFORO_2_VERMELHO_C1 = 12

BOTAO_PEDESTRE_1_C1 = 8
BOTAO_PEDESTRE_2_C1 = 7

SENSOR_PASSAGEM_1_C1 = 14
SENSOR_PASSAGEM_2_C1 = 15

SENSOR_VELOCIDADE_1_A_C1 = 18
SENSOR_VELOCIDADE_1_B_C1 = 23

SENSOR_VELOCIDADE_2_A_C1 = 24
SENSOR_VELOCIDADE_2_B_C1 = 25

''' CRUZAMENTO 2  '''
SEMAFORO_1_VERDE_C2 = 2
SEMAFORO_1_AMARELO_C2 = 3
SEMAFORO_1_VERMELHO_C2 = 11

SEMAFORO_2_VERDE_C2 = 0
SEMAFORO_2_AMARELO_C2 = 15
SEMAFORO_2_VERMELHO_C2 = 6

BOTAO_PEDESTRE_1_C2 = 10
BOTAO_PEDESTRE_2_C2 = 9

SENSOR_PASSAGEM_1_C2 = 4
SENSOR_PASSAGEM_2_C2 = 17 

SENSOR_VELOCIDADE_1_A_C2 = 27 
SENSOR_VELOCIDADE_1_B_C2 = 22

SENSOR_VELOCIDADE_2_A_C2 = 13
SENSOR_VELOCIDADE_2_B_C2 = 19

main_timing_traffic_light = [
    {'active': ['SEMAFORO_1_VERMELHO_C1', 'SEMAFORO_1_VERMELHO_C2'], 'time_max': 1, 'time_min': 1 },
    {'active': ['SEMAFORO_1_VERDE_C1', 'SEMAFORO_1_VERDE_C2'], 'time_max': 20, 'time_min': 10 },
    {'active': ['SEMAFORO_1_AMARELO_C1', 'SEMAFORO_1_AMARELO_C2'], 'time_max': 3, 'time_min': 3 },
    {'active': ['SEMAFORO_1_VERMELHO_C1', 'SEMAFORO_1_VERMELHO_C2'], 'time_max': 1, 'time_min': 1 },
    {'active': ['SEMAFORO_1_VERMELHO_C1', 'SEMAFORO_1_VERMELHO_C2'], 'time_max': 10, 'time_min': 5 },
    {'active': ['SEMAFORO_1_VERMELHO_C1', 'SEMAFORO_1_VERMELHO_C2'], 'time_max': 3, 'time_min': 3 },
    {'active': ['SEMAFORO_1_AMARELO_C1', 'SEMAFORO_1_AMARELO_C2'], 'time_max': 1, 'time_min': 1 },
]

aux_timing_traffic_light = [
    {'active': ['SEMAFORO_2_VERMELHO_C1', 'SEMAFORO_2_VERMELHO_C2'], 'time_max': 1, 'time_min': 1 },
    {'active': ['SEMAFORO_2_VERMELHO_C1', 'SEMAFORO_2_VERMELHO_C2'], 'time_max': 20, 'time_min': 10 },
    {'active': ['SEMAFORO_2_VERMELHO_C1', 'SEMAFORO_2_VERMELHO_C2'], 'time_max': 3, 'time_min': 3 },
    {'active': ['SEMAFORO_2_VERMELHO_C1', 'SEMAFORO_2_VERMELHO_C2'], 'time_max': 1, 'time_min': 1 },
    {'active': ['SEMAFORO_2_VERDE_C1', 'SEMAFORO_2_VERDE_C2'], 'time_max': 10, 'time_min': 5 },
    {'active': ['SEMAFORO_2_AMARELO_C1', 'SEMAFORO_2_AMARELO_C2'], 'time_max': 3, 'time_min': 3 },
    {'active': ['SEMAFORO_2_AMARELO_C1', 'SEMAFORO_2_AMARELO_C2'], 'time_max': 1, 'time_min': 1 },
]

from time import sleep
from threading import Thread

NUMBER_OF_STATES = 6

def handle_traffic_light_change(traffic_light, c_type):
    state = 0
    while True:
        curr_state = traffic_light[state]
        print("{}: {} [STATE]: {}".format(c_type, curr_state['active'], state))
        sleep(curr_state['time_max'])
        state = next_state(state)

def next_state(current_state):
    return (current_state + 1) % NUMBER_OF_STATES

main_thread = Thread(target=handle_traffic_light_change, args=(main_timing_traffic_light, 'principal'))
aux_thread = Thread(target=handle_traffic_light_change, args=(aux_timing_traffic_light, 'auxiliar'))

main_thread.start()
aux_thread.start()


