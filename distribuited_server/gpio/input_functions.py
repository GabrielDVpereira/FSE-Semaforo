import RPi.GPIO as GPIO


def watch_input_event(port, callback):
    GPIO.add_event_detect(port, GPIO.RISING, callback=callback, bouncetime=300)
