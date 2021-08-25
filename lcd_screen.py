from time import sleep
from Adafruit_CharLCD import Adafruit_CharLCD

class LcdScreen:
    def __init__(self):
        self.lcd = Adafruit_CharLCD(rs=26, en=19,
                       d4=13, d5=6, d6=5, d7=24,
                       cols=16, lines=2)
        self.lcd.clear()

    def write(self,msg):
        self.lcd.message(msg)
        sleep(3)

    def scroll_right(self):
        for x in range(0,16):
            self.lcd.move_right()
            sleep(.2)
        sleep(3)
    
    def scroll_left(self):
        for x in range(0,16):
            self.lcd.move_left()
            sleep(.2)
        sleep(3)
    
    def wait(self, seconds):
        sleep(seconds)
    
    def clear(self):
        self.lcd.clear()
