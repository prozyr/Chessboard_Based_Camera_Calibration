import numpy as np
import glob
import cv2
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logging.info('Loading list of image files...')
images_paths = glob.glob('photos/Series1_*.jpg')
logging.info("Number of found paths: " + str(len(images_paths)))

CHESS_BOARD_SIZES = (9, 6)

for img_path in images_paths:
    img = cv2.imread(img_path)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, corners = cv2.findChessboardCorners(img_gray, CHESS_BOARD_SIZES, None)
    logging.info(ret if 'Chessboard Corners has been found' else 'None chessboard Corners has been found')

    if ret:
        corners2 = cv2.cornerSubPix(img_gray,
                                    corners,
                                    (11, 11),
                                    (-1, -1),
                                    (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001))
        cv2.drawChessboardCorners(img, CHESS_BOARD_SIZES, corners2, ret)
        cv2.imshow('img', img)
        cv2.waitKey(0)


cv2.destroyAllWindows()