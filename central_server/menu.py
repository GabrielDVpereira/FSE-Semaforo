from datetime import datetime
from time import sleep
from threading import Thread
import central_socket
from menu_model import MenuInfo
import utils

infos = {}

def init_menu():
    menu_thread = Thread(target=print_menu)
    menu_thread.start()
    menu_thread.join()

def print_menu():
    while True:
        print("SERVIDOR CENTRAL\n")
        print("Selecione uma das opções abaixo:\n\n")
        print("1 - Painel de monitoramento\n")
        print("2 - Painel de controle de ações\n")
        option = int(input("Selecione uma das opções de pressione ENTER: "))
        if option == 1: print_crossing_info()
        elif option == 2: print_crossing_actions()
        else: break

def print_crossing_info():
    global infos
    global interrupted
    while True:

        for crossing in infos:  
            print_menu_info(infos[crossing])

        print("Pressione CRTL + C Para voltar")
        sleep(1)
        utils.clear()
        if interrupted:
            interrupted = False
            break


def print_crossing_actions():
    global interrupted
    emergency_mode = False
    night_mode = False
    while True:
        utils.clear()
        print("CONTROLE DE ACÕES \n\n")
        print("1 - {} MODO DE EMERGÊNCIA".format("LIGAR" if not emergency_mode else "DESLIGAR"))
        print("2 - {} MODO DE NOTURNO".format("LIGAR" if not night_mode else "DESLIGAR"))
        print("3 - Voltar")
        
        option = int(input("Digite uma opção e pressine ENTER: "))
        
        if option == 1:
           if night_mode: 
                print("Desligue o modo noturno para ativar o modo de emergência")
                sleep(1)
           else: 
            emergency_mode = not emergency_mode
        elif option == 2:
            if emergency_mode: 
                print("Desligue o modo de emergencia para ativar o modo noturno")
                sleep(1)
            else: 
                night_mode = not night_mode
        elif option == 3: 
            if emergency_mode or night_mode: 
                print("Desligue todos os modos antes de sair")
                sleep(1)
            else:
                utils.clear()
                break
    
        central_socket.send_message({
            "emergency_mode": emergency_mode, 
            "night_mode": night_mode
        })

interrupted = False
def signal_handler(signal, frame):
    global interrupted
    interrupted = True

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
    global infos

    crossing = msg["crossing"]

    if crossing not in infos:
        return

    menu_info = infos[crossing]


    menu_info.car_count['line1'] = msg["data"]["line1"]
    menu_info.car_count['line2'] = msg["data"]["line2"]

def print_menu_info(menu_info):

    print("CRUZAMENTO {}".format(menu_info.crossing))
    print("\n")

    print("FLUXO DE TRÂNSITO SENTIDO 1 (VIA AUXILIAR): {} carros/min".format(menu_info.get_traffic_flow('line1')))
    print("FLUXO DE TRÂNSITO SENTIDO 2 (VIA AUXILIAR): {} carros/min".format(menu_info.get_traffic_flow('line2')))
    print("\n")


    print("VELOCIDADE MÉDIA NA VIA (VIA PRINCIPAL): {} km/h".format(menu_info.get_average_speed()))
    print("\n")

    print("INFRAÇÃO SINAL VERMELHO: {}".format(menu_info.get_red_light_infraction()))

    print("INFRAÇÃO VELOCIDADE ACIMA DO PERMITIDO: {}".format(menu_info.get_speed_infraction()))
    print("\n")







        