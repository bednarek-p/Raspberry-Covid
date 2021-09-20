import RPi.GPIO as GPIO

BUTTON_PIN_IN = 20

class Button:
	def __init__(self):
		GPIO.setup(BUTTON_PIN_IN,GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
		
	def is_pressed(self):
		if GPIO.input(BUTTON_PIN_IN) == GPIO.HIGH:
			return True
