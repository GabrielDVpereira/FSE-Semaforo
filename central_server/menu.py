
from datetime import datetime
from time import sleep
from threading import Thread, Event

import central_socket

import sys
output_stream = sys.stdout

menu_info_c1 = {
    "car_speed": {
        "speed_amount": 0, 
        "car_count": 0, 
    }, 
    "red_light_infraction":{
        "count": 0
    },
    "speed_infraction":{
        "count": 0
    }, 
    "car_count":{
        "line1": 0,
        "line2": 0,
        "time": 0
    }
}

menu_info_c2 = {
    "car_speed": {
        "speed_amount": 0, 
        "car_count": 0
    }, 
    "red_light_infraction":{
        "count": 0
    },
    "speed_infraction":{
        "count": 0
    }, 
    "car_count":{
        "line1": 0,
        "line2": 0,
        "time": 0
    }
}

def update_menu_info(msg):
    msg_type = msg['type']

    if msg_type == "car_speed":
        handle_car_speed(msg)
    elif msg_type == "red_light_infraction":
        handle_red_light_infraction(msg)
    elif msg_type == "speed_infraction":
        handle_speed_infraction(msg)
    elif msg_type == "car_count":
        handle_car_count(msg)

def handle_car_speed(msg):
    global menu_info_c1
    global menu_info_c2
    
    speed_data = msg['data']
    crossing = msg['crossing']
    
    if crossing == 1:
        menu_info_c1["car_speed"]["speed_amount"]+= speed_data
        menu_info_c1["car_speed"]["car_count"]+= 1
    else:
        menu_info_c2["car_speed"]["speed_amount"]+= speed_data
        menu_info_c2["car_speed"]["car_count"]+= 1

def handle_red_light_infraction(msg):
    global menu_info_c1
    global menu_info_c2

    crossing = msg['crossing']

    if crossing == 1:
        menu_info_c1['red_light_infraction']['count']+=1
    else:
        menu_info_c2['red_light_infraction']['count']+=1

def handle_speed_infraction(msg):
    global menu_info_c1
    global menu_info_c2

    crossing = msg['crossing']

    if crossing == 1:
        menu_info_c1['speed_infraction']['count']+=1
    else:
        menu_info_c2['speed_infraction']['count']+=1 

date = None
def handle_car_count(msg):
    global date
    global menu_info_c1
    global menu_info_c2

    crossing = msg['crossing']

    if crossing == 1:
        menu_info_c1['car_count']['line1'] = msg["data"]["line1"]
        menu_info_c1['car_count']['line2'] = msg["data"]["line2"]
        menu_info_c1['car_count']['time'] = 1 if not date else (datetime.now() - date).total_seconds() / 60
    else:
        menu_info_c2['car_count']['line1'] = msg["data"]["line1"]
        menu_info_c2['car_count']['line2'] = msg["data"]["line2"]
        menu_info_c2['car_count']['time'] = 1 if not date else (datetime.now() - date).total_seconds() / 60

    date = datetime.now()    

def get_traffic_flow(meu_info):
    time =  meu_info['car_count']['time']
    line1 = meu_info['car_count']['line1']
    line2 = meu_info['car_count']['line2'] 

    flow1 = 0 if time == 0 else line1 / time
    flow2 = 0 if time == 0 else line2 / time

    return [str(flow1), str(flow2)]

def get_average_speed(meu_info):
    speed_amount = meu_info['car_speed']['speed_amount']
    car_count = meu_info['car_speed']['car_count']
    return  '0' if car_count == 0 else str(speed_amount / car_count)

def get_red_light_infraction(meu_info):
    return str(meu_info['red_light_infraction']['count'])

def get_speed_infraction(meu_info):
    return str(meu_info['speed_infraction']['count'])


def print_menu_info(crossing, meu_info):
    output_stream.write("CRUZAMENTO ")
    output_stream.write(str(crossing)) 
    output_stream.write("\n\n")

    output_stream.write("FLUXO DE TRÂNSITO SENTIDO 1 (VIA AUXILIAR): ")
    output_stream.write(get_traffic_flow(meu_info)[0])
    output_stream.write("\n")

    output_stream.write("FLUXO DE TRÂNSITO SENTIDO 2 (VIA AUXILIAR): ")
    output_stream.write(get_traffic_flow(meu_info)[1])
    output_stream.write("\n\n")


    output_stream.write("VELOCIDADE MÉDIA NA VIA (VIA PRINCIPAL): ")
    output_stream.write(get_average_speed(meu_info))
    output_stream.write("\n\n")

    output_stream.write("INFRAÇÃO SINAL VERMELHO: ")
    output_stream.write(get_red_light_infraction(meu_info))
    output_stream.write("\n")

    output_stream.write("INFRAÇÃO VELOCIDADE ACIMA DO PERMITIDO:")
    output_stream.write(get_speed_infraction(meu_info))
    output_stream.write("\n\n\n")


def config_menu():
    while True:
        print_menu_info(1, menu_info_c1)
        print_menu_info(2, menu_info_c2)
        output_stream.flush()
        sleep(1)


def config_menu_options():
    emergency_mode = False
    night_mode = False
    while True:
        print("1 - {} MODO DE EMERGÊNCIA \n".format("LIGAR" if not emergency_mode else "DESLIGAR"))
        print("2 - {} MODO DE NOTURNO \n\n".format("LIGAR" if not night_mode else "DESLIGAR"))
        
        option = int(input("Selecione uma opção: "))
        
        if option == 1:
           emergency_mode = not emergency_mode
        else:
            night_mode = not night_mode
 
        central_socket.send_message({
            "emergency_mode": emergency_mode, 
            "night_mode": night_mode
        })



def init_menu():
    menu_thread = Thread(target=config_menu_options)
    menu_thread.start()