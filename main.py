import numpy as np
import glob
import cv2 as cv
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logging.info('Loading list of image files...')
images = glob.glob('photos/Series1_*.jpg')
logging.info("Number of found paths: " + str(len(images)))

