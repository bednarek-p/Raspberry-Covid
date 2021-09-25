import RPi.GPIO as GPIO
import datetime

PIR_PIN_IN = 22

class PirSensor:
	def __init__(self):
		GPIO.setup(PIR_PIN_IN,GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
		
	def is_triggered(self):
		if GPIO.input(PIR_PIN_IN) == GPIO.HIGH:
			return True
		else:
			return False
		
	def wait_for_walk_in(self,timeout = 10):
		start_time = datetime.datetime.now()
		
		while not self.is_triggered():
			time_diff = (datetime.datetime.now() - start_time).total_seconds()
			if time_diff > timeout:
				break
