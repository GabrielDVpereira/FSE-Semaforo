from datetime import datetime
from time import sleep
from threading import Thread
import central_socket
import os
from menu_model import MenuInfo

infos = {}

def update_menu_info(msg):
    msg_type = msg['type']
    if msg_type == "new_connection":
        handle_new_connection(msg)
    elif msg_type == "car_speed":
        handle_car_speed(msg)
    elif msg_type == "red_light_infraction":
        handle_red_light_infraction(msg)
    elif msg_type == "speed_infraction":
        handle_speed_infraction(msg)
    elif msg_type == "car_count":
        handle_car_count(msg)
    
def handle_new_connection(msg):
    print("Handle new Connection: {}".format(msg))
    crossing = msg["crossing"]
    infos[crossing] = MenuInfo(crossing)
    
def handle_car_speed(msg):
    global infos
    crossing = msg["crossing"]

    menu_info = infos[crossing]
    
    speed_data = msg['data']
    
    menu_info.car_speed["speed_amount"]+= speed_data
    menu_info.car_speed["car_count"]+= 1
  

def handle_red_light_infraction(msg):
    global infos

    crossing = msg["crossing"]
    menu_info = infos[crossing]
    
    menu_info.red_light_infraction +=1

def handle_speed_infraction(msg):
    global infos

    crossing = msg["crossing"]
    menu_info = infos[crossing]

    menu_info.speed_infraction +=1 

def handle_car_count(msg):
    global date
    global infos

    if not infos:
        return # No instance initialized

    crossing = msg["crossing"]
    menu_info = infos[crossing]


    menu_info.car_count['line1'] = msg["data"]["line1"]
    menu_info.car_count['line2'] = msg["data"]["line2"]


def get_traffic_flow(menu_info, line_str):
    line = menu_info.car_count[line_str]
    now = datetime.now()

    time_diff = (now - menu_info.start_time).total_seconds() / 60 # Difference in minutes

    return line / time_diff

def get_average_speed(meu_info):
    speed_amount = meu_info.car_speed['speed_amount']
    car_count = meu_info.car_speed['car_count']
    return  '0' if car_count == 0 else str(speed_amount / car_count)

def get_red_light_infraction(meu_info):
    return str(meu_info.red_light_infraction)

def get_speed_infraction(meu_info):
    return str(meu_info.speed_infraction)


def print_menu_info(menu_info):

    print("CRUZAMENTO {}".format(menu_info.crossing))
    print("\n")

    print("FLUXO DE TRÂNSITO SENTIDO 1 (VIA AUXILIAR): {} carros/min".format(get_traffic_flow(menu_info, 'line1')))
    print("FLUXO DE TRÂNSITO SENTIDO 2 (VIA AUXILIAR): {} carros/min".format(get_traffic_flow(menu_info, 'line2')))
    print("\n")


    print("VELOCIDADE MÉDIA NA VIA (VIA PRINCIPAL): {} km/h".format(get_average_speed(menu_info)))
    print("\n")

    print("INFRAÇÃO SINAL VERMELHO: {}".format(get_red_light_infraction(menu_info)))

    print("INFRAÇÃO VELOCIDADE ACIMA DO PERMITIDO: {}".format(get_speed_infraction(menu_info)))
    print("\n")



def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

interrupted = False
def signal_handler(signal, frame):
    global interrupted
    interrupted = True

def print_crossing_info():
    global interrupted
    while True:

        for crossing in infos:  
            print_menu_info(infos[crossing])

        print("Pressione CRTL + C Para voltar")
        sleep(1)
        clear()
        if interrupted:
            interrupted = False
            break


def print_crossing_actions():
    global interrupted
    emergency_mode = False
    night_mode = False
    while True:
        clear()
        print("CONTROLE DE ACÕES \n\n")
        print("1 - {} MODO DE EMERGÊNCIA \n".format("LIGAR" if not emergency_mode else "DESLIGAR"))
        print("2 - {} MODO DE NOTURNO \n".format("LIGAR" if not night_mode else "DESLIGAR"))
        print("3 - Voltar")
        
        option = int(input("Selecione uma opção: "))
        
        if option == 1:
           emergency_mode = not emergency_mode
        elif option == 2:
            night_mode = not night_mode
        elif option == 3: 
            clear()
            break
    
        central_socket.send_message({
            "emergency_mode": emergency_mode, 
            "night_mode": night_mode
        })




def print_menu():
    while True:
        print("SERVIDOR CENTRAL\n")
        print("Selecione uma das opções abaixo:\n\n")
        print("1 - Painel de monitoramento\n")
        print("2 - Painel de controle de ações\n")
        option = int(input())
        if option == 1: print_crossing_info()
        elif option == 2: print_crossing_actions()
        else: break

        

def init_menu():
    menu_thread = Thread(target=print_menu)
    menu_thread.start()
    menu_thread.join()