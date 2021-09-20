import RPi.GPIO as GPIO

PIR_PIN_IN = 22

class PirSensor:
	def __init__(self):
		GPIO.setup(PIR_PIN_IN,GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
		
	def is_triggered(self):
		if GPIO.input(PIR_PIN_IN) == GPIO.HIGH:
			return True
		else:
			return False
