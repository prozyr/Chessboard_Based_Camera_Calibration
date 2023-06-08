import numpy as np
import glob
import cv2
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logging.info('Loading list of image files...')
images_paths = glob.glob('photos/Series1_*.jpg')
logging.info("Number of found paths: " + str(len(images_paths)))

# Statistic arrays and constants
CHESS_BOARD_SIZES = (9, 6)
objpoints = []
points_array = []
objp = np.zeros((6*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)




for img_path in images_paths:
    img = cv2.imread(img_path)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, corners = cv2.findChessboardCorners(img_gray, CHESS_BOARD_SIZES, None)
    logging.info(ret if 'Chessboard Corners has been found' else 'None chessboard Corners has been found')

    if ret:
        objpoints.append(objp)
        cornersSubPix = cv2.cornerSubPix(img_gray,
                                    corners,
                                    (11, 11),
                                    (-1, -1),
                                    (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001))
        points_array.append(cornersSubPix)
        cv2.drawChessboardCorners(img, CHESS_BOARD_SIZES, cornersSubPix, ret)
        cv2.imshow('img', img)
        cv2.waitKey(0)

cv2.destroyAllWindows()


if len(points_array) > 0:
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, points_array, img_gray.shape[::-1], None, None)
    with open('parameters.txt','w') as file:
        file.write("RET"+ '\n' +str(ret) + '\n' + "MTX" + '\n' +str(mtx) + '\n' + "DIST" + '\n' + str(dist) + '\n' + 'RVECS' + '\n' + str(rvecs) + '\n' + "TVECS" + '\n' + str(tvecs))
        file.close()
    print("Successful calibration")
else:
    print("Error with points")



cv2.imshow('img',img)
cv2.waitKey(0)
h,  w = img.shape[:2]
newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))

# undistort
mapx, mapy = cv2.initUndistortRectifyMap(mtx, dist, None, newcameramtx, (w,h), 5)
dst = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)
# crop the image
x, y, w, h = roi
dst = dst[y:y+h, x:x+w]
cv2.imshow('wynik', dst)
cv2.imwrite('C:/Users/Maciej Wecki/Desktop/Studia Magisterskie/CVAPR/Result.jpg', dst)  # Modify the file path here
cv2.waitKey(0)


mean_error = 0
for i in range(len(obj_points)):
    imgpoints2, _ = cv2.projectPoints(obj_points[i], rvecs[i], tvecs[i], mtx, dist)
    error = cv2.norm(img_points[i], imgpoints2, cv2.NORM_L2)/len(imgpoints2)
    mean_error += error
print( "total error: {}".format(mean_error/len(obj_points)) )

with open('C:/Users/Maciej Wecki/Desktop/Studia Magisterskie/CVAPR/Projekt/parametry.txt','a') as file:
        file.write('\n' + "ERROR" + '\n' + str(mean_error/len(obj_points)))
        file.close()