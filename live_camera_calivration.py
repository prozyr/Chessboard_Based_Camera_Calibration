import numpy as np
import glob
import cv2
import logging
import time


last_time = 0


########## START ##########
video = cv2.VideoCapture(0)
success, img = video.read()
cv2.imshow('img', img)
cv2.moveWindow('img', 40,30)
cv2.waitKey(0)
while True:
    success, img = video.read()
    cv2.imshow('img', img)
    cv2.moveWindow('img', 40, 30)
    cv2.waitKey(0)