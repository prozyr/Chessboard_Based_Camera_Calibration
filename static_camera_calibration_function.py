import numpy as np
import glob
import cv2
import logging
import threading


class CameraModel:
    def __init__(self, newcameramtx, roi, mtx, dist):
        self.newcameramtx = newcameramtx
        self.roi = roi
        self.mtx = mtx
        self.dist = dist

    def undistort_img(self, img):
        h, w = img.shape[:2]
        mapx, mapy = cv2.initUndistortRectifyMap(self.mtx, self.dist, None, self.newcameramtx, (w, h), 5)
        dst = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)
        x, y, w, h = self.roi
        dst = dst[y:y + h, x:x + w]
        return dst


def process_image(img, objpoints, points_array, CHESS_BOARD_SIZES):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, corners = cv2.findChessboardCorners(img_gray, CHESS_BOARD_SIZES, None)
    logging.info('Chessboard Corners has been found' if ret else 'None chessboard Corners has been found')

    if ret:
        objp = np.zeros((6*9, 3), np.float32)
        objp[:, :2] = np.mgrid[0:9, 0:6].T.reshape(-1, 2)

        objpoints.append(objp)
        cornersSubPix = cv2.cornerSubPix(img_gray,
                                         corners,
                                         (11, 11),
                                         (-1, -1),
                                         (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001))
        points_array.append(cornersSubPix)
        cv2.drawChessboardCorners(img, CHESS_BOARD_SIZES, cornersSubPix, ret)


def static_camera_calibration_function(photos):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Statistic arrays and constants
    logging.info("Create statistic arrays and constants")
    CHESS_BOARD_SIZES = (9, 6)
    objpoints = []
    points_array = []
    threads = []

    logging.info("Starting looping in images")
    for img in photos:
        thread = threading.Thread(target=process_image, args=(img, objpoints, points_array, CHESS_BOARD_SIZES))
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    if len(points_array) > 0:
        logging.info("Start camera calibration")
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, points_array, photos[0].shape[::-1], None, None)
        with open('parameters.txt', 'w') as file:
            file.write("RET" + '\n' + str(ret) + '\n' + "MTX" + '\n' + str(mtx) + '\n' + "DIST" + '\n' + str(dist) + '\n' +
                       'RVECS' + '\n' + str(rvecs) + '\n' + "TVECS" + '\n' + str(tvecs))
        print("Successful calibration")
    else:
        print("There is no points. ERROR.")
        return None

    h,  w = img.shape[:2]
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))

    return CameraModel(newcameramtx, roi, mtx, dist)
