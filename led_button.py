import RPi.GPIO as GPIO

LED_BUTTON_OUT = 21

class LedButton:
    def __init__(self):
        GPIO.setup(LED_BUTTON_OUT,GPIO.OUT)
        GPIO.output(LED_BUTTON_OUT,GPIO.LOW)

    def turn_on(self):
        GPIO.output(LED_BUTTON_OUT,GPIO.HIGH)

    def turn_off(self):
        GPIO.output(LED_BUTTON_OUT,GPIO.LOW)
