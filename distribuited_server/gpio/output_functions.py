import RPi.GPIO as GPIO

def turn_up_port(port):
    GPIO.output(port, GPIO.HIGH)
    
def turn_off_port(port):
    GPIO.output(port, GPIO.LOW)