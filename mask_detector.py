import numpy as np
import cv2
import sys
import os


from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model



class MaskDetector:
    def __init__(self):
        self.cam = cv2.VideoCapture(0)
        self.net_caffe_model = cv2.dnn.readNetFromCaffe("./Face_detection_models/weights.txt", "./Face_detection_models/res.caffemodel")


    def __del__(self):
        self.cam.release()
        cv2.destroyAllWindows()

    def take_frame(self):
        capture_status, self.image = self.cam.read()
        if not capture_status:
            print("ERR: Can't take camera frame!")
            sys.exit(1)

    def face_detection(self):
        self.take_frame()
        self.image = cv2.resize(self.image, (300, 300))
        (photo_height, photo_width) = self.image.shape[:2]
        photo_blob = cv2.dnn.blobFromImage(self.image, 1.0, (300, 300), (104, 117, 123))

        # make detections on the photo
        self.net_caffe_model.setInput(photo_blob)
        self.detections = self.net_caffe_model.forward()
        
        # loop over all detections
        for i in range(0, self.detections.shape[2]):
            # take confidence of prediction
            confidence = self.detections[0, 0, i, 2]

            # minimum confidence threshold
            if confidence > 0.5:
                box = self.detections[0, 0, i, 3:7] * np.array([photo_width, photo_height,photo_width, photo_height])
                (x1, y1, x2, y2) = box.astype("int")
                # ensure the bounding boxes fall within the dimensions of
                # the frame
                (x1, y1) = (max(0, x1), max(0, y1))
                (x2, y2) = (min(photo_width - 1, x2), min(photo_height - 1, y2))
                cv2.rectangle(self.image, (x1, y1), (x2, y2), (255, 0, 255), 2)

                #printing face coordinates
                print(f"x1={x1}")
                print(f"x2={x2}")
                print(f"y1={y1}")
                print(f"y2={y2}")
                
                #MASK DETECTION
                face = self.image[y1 : y2,x1 : x2]
                face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
                face = cv2.resize(face, (224,224))
                face = img_to_array(face)
                face = preprocess_input(face)
                face = np.expand_dims(face, axis=0)
                
                #making mask predictions
                self.mask_detection_model = load_model("./Mask_detection_model/mask.model")
                (mask_prediction, no_mask_prediction) = self.mask_detection_model.predict(face)[0]
                #print(f"mask prediction: {mask_prediction} ")
                #print(f"no mask prediction: {no_mask_prediction}")
                
                if mask_prediction > no_mask_prediction:
                    label = "MASK "
                    pred = round(max(mask_prediction,no_mask_prediction) * 100)
                    label += str(pred)
                    #DEBUG
                    label_color = (0,255,0)
                    cv2.putText(self.image,label,(x1,y1 - 5),cv2.FONT_HERSHEY_SIMPLEX, 0.5, label_color, 2)
                    self.image = cv2.resize(self.image, (800, 800))
                    cv2.imshow("Output", self.image)
                    cv2.waitKey(0)
                    return label

                else:
                    label = "NO MASK "
                    pred = round(max(mask_prediction,no_mask_prediction) * 100)
                    label += str(pred)
                    #DEBUG
                    label_color = (0,0,255)
                    cv2.putText(self.image,label,(x1,y1 - 5),cv2.FONT_HERSHEY_SIMPLEX, 0.5, label_color, 2)
                    self.image = cv2.resize(self.image, (800, 800))
                    cv2.imshow("Output", self.image)
                    cv2.waitKey(0)
                    return label
