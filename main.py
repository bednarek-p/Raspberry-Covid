from mask_detector import MaskDetector
from lcd_screen import LcdScreen
from temp_sensor import TemperatureSensor
from button import Button


#INITIALIZATION
button = Button()
lcd_screen = LcdScreen()
mask_detector = MaskDetector()
temp_sensor = TemperatureSensor()
lcd_screen.write("Press button\nto start!")


while True:
	if button.is_pressed() == True:
		

		lcd_screen.write("Starting all\nProcedures")
		lcd_screen.wait(5)
		lcd_screen.clear()

		lcd_screen.count_down(5,"Temperature\n check: ")
		tmp=temp_sensor.get_target_temperature()
		lcd_screen.write(f"TEMP:{tmp}")
		lcd_screen.wait(2)


		lcd_screen.count_down(5,"Mask check. Face\nthe Camera: ")
		mask_detector.take_frame()
		lcd_screen.write("Processing Image\nPlease wait...")
		res = mask_detector.face_detection()
		lcd_screen.write(str(res))
		
		lcd_screen.wait(5)
		lcd_screen.write("Press button\nto start!")





