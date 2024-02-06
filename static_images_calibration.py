import numpy as np
import glob
import cv2
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Log information about loading image files
logging.info('Loading list of image files...')
images_paths = glob.glob('photos/*.jpg')
logging.info("Number of found paths: " + str(len(images_paths)))

# Loop through the first 3 images
for i in range(1, 4):
    # Chessboard size constants
    CHESS_BOARD_SIZES = (9, 6)

    # Arrays for calibration
    objpoints = []
    points_array = []

    # Create 3D chessboard points
    objp = np.zeros((CHESS_BOARD_SIZES[1] * CHESS_BOARD_SIZES[0], 3), np.float32)
    objp[:, :2] = np.mgrid[0:CHESS_BOARD_SIZES[0], 0:CHESS_BOARD_SIZES[1]].T.reshape(-1, 2)

    imgs = []

    # Loop through images
    logging.info("Starting looping in images")
    for img_path in images_paths[:i]:
        img = cv2.imread(img_path)
        imgs.append(img)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Find chessboard corners
        ret, corners = cv2.findChessboardCorners(img_gray, CHESS_BOARD_SIZES, None)
        logging.info("Chessboard Corners found" if ret else "No chessboard Corners found")

        if ret:
            objpoints.append(objp)
            
            # Refine corner positions
            corners_subpix = cv2.cornerSubPix(img_gray, corners, (11, 11), (-1, -1),
                                             (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001))
            points_array.append(corners_subpix)
            
            # Draw chessboard corners on the image
            cv2.drawChessboardCorners(img, CHESS_BOARD_SIZES, corners_subpix, ret)
            cv2.imshow('img', img)
            cv2.waitKey(0)

    cv2.destroyAllWindows()

    if len(points_array) > 0:
        logging.info("Start camera calibration")
        
        # Perform camera calibration
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, points_array, img_gray.shape[::-1], None, None)
        
        # Save calibration parameters to a file
        with open('parameters.txt', 'w') as file:
            file.write("RET" + '\n' + str(ret) + '\n' + "MTX" + '\n' + str(mtx) + '\n' + "DIST" + '\n' + str(dist) + '\n' +
                       'RVECS' + '\n' + str(rvecs) + '\n' + "TVECS" + '\n' + str(tvecs))
        
        print("Successful calibration")
    else:
        print("There are no valid calibration points. ERROR.")

    # Get optimal new camera matrix and region of interest
    h, w = img.shape[:2]
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))

    # Undistort the first image
    mapx, mapy = cv2.initUndistortRectifyMap(mtx, dist, None, newcameramtx, (w, h), 5)
    dst = cv2.remap(imgs[0], mapx, mapy, cv2.INTER_LINEAR)
    
    # Crop the image based on the region of interest
    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]
    cv2.imshow('Undistorted', dst)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    # Save the undistorted result
    cv2.imwrite('UndistortedResult.jpg', dst)

    # Calculate and log the mean reprojection error
    mean_error = 0
    for i in range(len(objpoints)):
        imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
        error = cv2.norm(points_array[i], imgpoints2, cv2.NORM_L2) / len(imgpoints2)
        mean_error += error
    
    print("Total mean reprojection error: {}".format(mean_error / len(objpoints)))

    # Append the error to the parameters file
    with open('parameters.txt', 'a') as file:
        file.write('\n' + "ERROR" + '\n' + str(mean_error / len(objpoints)))
