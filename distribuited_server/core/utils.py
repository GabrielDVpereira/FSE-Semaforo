import subprocess 
from threading import Thread

def play_sound():
    play_thread = Thread(target=subprocess.call, args=(['sh', './play_sound.sh'],))
    play_thread.start()
    play_thread.join()