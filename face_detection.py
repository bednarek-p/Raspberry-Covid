import numpy as np
import cv2
import argparse

# camera setup
cam = cv2.VideoCapture(0)



while True:
    
    capture_status, frame = cam.read()
    if not capture_status:
        print("ERR: Can't take camera frame!")
        break
    
    cv2.imshow("Input", frame)
    k = cv2.waitKey(1)
    
    
    #ESCAPE PRESED
    if k % 256 == 27:
        print("Escape hit, closing...")
        break
    # SPACE pressed
    elif k % 256 == 32:
        # loading weights and caffemodel for face detection
        net_caffe = cv2.dnn.readNetFromCaffe("weights.txt", "res.caffemodel")

        # load and resize image to 300x300
        image = frame
        image = cv2.resize(image, (300, 300))
        (photo_height, photo_width) = image.shape[:2]

        photo_blob = cv2.dnn.blobFromImage(
            image, 1.0, (300, 300), (104, 117, 123))

        # make detections on the photo
        net_caffe.setInput(photo_blob)
        detections = net_caffe.forward()

        # loop over all detections
        for i in range(0, detections.shape[2]):
            # take confidence of prediction
            confidence = detections[0, 0, i, 2]

            # minimum confidence threshold
            if confidence > 0.5:
                box = detections[0, 0, i, 3:7] * \
                    np.array([photo_width, photo_height,
                             photo_width, photo_height])
                (x1, y1, x2, y2) = box.astype("int")
                cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 255), 2)

        image = cv2.resize(image, (800, 800))
        # show output
        cv2.imshow("Output", image)
        cv2.waitKey(0)


cam.release()
cv2.destroyAllWindows()
