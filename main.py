import numpy as np
import glob
import cv2
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logging.info('Loading list of image files...')
images_paths = glob.glob('photos/Series1_*.jpg')
logging.info("Number of found paths: " + str(len(images_paths)))

for img_path in images_paths:
    img = cv2.imread(img_path)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow('img', img)
    cv2.waitKey(0)


cv2.destroyAllWindows()