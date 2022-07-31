import RPi.GPIO as GPIO


def watch_input_event(port, callback, rising = True):
    GPIO.add_event_detect(port, GPIO.RISING if rising else GPIO.FALLING, callback=callback, bouncetime=300)

def remove_input_event(port):
    GPIO.remove_event_detect(port)
