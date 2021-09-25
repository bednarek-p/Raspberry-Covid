from mask_detector import MaskDetector
from lcd_screen import LcdScreen
from temp_sensor import TemperatureSensor
from button import Button
from pir_sensor import PirSensor

#INITIALIZATION
button = Button()
pir_sensor = PirSensor()
lcd_screen = LcdScreen()
mask_detector = MaskDetector()
temp_sensor = TemperatureSensor()


lcd_screen.write("Press button\nto start!")

while True:
	if button.is_pressed() == True:
		lcd_screen.write("Starting all\nProcedures")
		lcd_screen.wait(3)
		lcd_screen.clear()

		lcd_screen.count_down(3,"Temperature\n check: ")
		temperature=temp_sensor.get_target_temperature()
		lcd_screen.write(f"Temperature:\n{temperature}*C")
		lcd_screen.wait(2)

		if float(temperature) >= 35 and float(temperature) <= 37:
			lcd_screen.count_down(5,"Mask check. Face\nthe Camera: ")
			mask_detector.take_frame()
			lcd_screen.write("Processing Image\nPlease wait...")
			result, txt_result = mask_detector.face_detection()
			if result == True:
				lcd_screen.write(f"MASK ON!\nConfidance:{txt_result}%")
				lcd_screen.wait(3)
				lcd_screen.write("You can walk in!")
				pir_sensor.wait_for_walk_in()
				lcd_screen.write("Press button\nto start!")
			else:
				lcd_screen.write(f"NO MASK!\nConfidance:{txt_result}%")
				lcd_screen.wait(3)
				lcd_screen.write("Press button\nto start!")
		else:
			lcd_screen.write("Incorrect\ntemperature!")
			lcd_screen.wait(3)
			lcd_screen.write("Press button\nto start!")
			
