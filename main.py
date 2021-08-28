#from mask_detector import MaskDetector
from lcd_screen import LcdScreen
from temp_sensor import TemperatureSensor
from pynput.keyboard import Key, Listener

def on_press(key):
    
    if key == Key.tab:
#        mask_detector = MaskDetector()
#        mask_detector.take_frame()
#        mask_detector.face_detection()
         lcd_screen = LcdScreen()
#         lcd_screen.write("TEST TEST TEST \n TEST2 TEST2")
#         lcd_screen.scroll_right()
#         lcd_screen.scroll_left()
#         lcd_screen.clear()
         lcd_screen.count_down(10, "ODLICZANIE: ")
    if key != Key.tab:
        print("Escape hit, closing...")
        return False
          
    
  
# Collect all event until released
with Listener(on_press = on_press) as listener:
    listener.join()


