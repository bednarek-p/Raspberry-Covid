import numpy as np
import cv2
import keyboard

from mask_detector import MaskDetector
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model



print("LETS GO")
while True:  # making a loop
	#ESCAPE PRESED
	if keyboard.is_pressed('q'):  
		print("Escape hit, closing...")
		break
	# SPACE pressed
	elif keyboard.is_pressed('t'):
		mask_detector = MaskDetector()
		mask_detector.take_frame()
		mask_detector.face_detection()
