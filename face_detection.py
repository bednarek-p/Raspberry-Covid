from mask_detector import MaskDetector
from pynput.keyboard import Key, Listener

def on_press(key):
    
    if key == Key.tab:
        mask_detector = MaskDetector()
        mask_detector.take_frame()
        mask_detector.face_detection()
          
    if key != Key.tab:
        print("Escape hit, closing...")
        return False
          
    
  
# Collect all event until released
with Listener(on_press = on_press) as listener:
    listener.join()


