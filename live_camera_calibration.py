import numpy as np
import glob
import cv2
import logging
import time
from static_camera_calibration_function import CameraModel
from static_camera_calibration_function import static_camera_calibration_function


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
last_time = 0


########## START ##########
video = cv2.VideoCapture(0)
success, img = video.read()
cv2.imshow('img', img)
cv2.moveWindow('img', 40,30)
cv2.waitKey(0)

images_for_calibration = []
cameraModel = None
while True:
    counter = 0
    while time.time() - last_time < 0.1:
        counter += 1
        continue
    success, img = video.read()
    images_for_calibration.append(img)

    if len(images_for_calibration) == 5:
        logging.info("Start static_camera_calibration_function")
        cameraModel = static_camera_calibration_function(images_for_calibration)
        logging.info("Finish static_camera_calibration_function")
        print("Camera model" + str(cameraModel.newcameramtx))
        images_for_calibration = []

    if cameraModel is not None:
        img = cameraModel.undistort_img(img)

    cv2.imshow('img', img)
    cv2.waitKey(0)

