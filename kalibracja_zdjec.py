import numpy as np
import cv2
import pandas as pd
# Wymiary planszy szachowej
ROWS = 7
COLS = 7

# Przygotowanie pustych list punktów na planszy szachowej i odpowiadających im punktów na obrazie
img_points = []  # lista punktów na obrazie
obj_points = []  # lista odpowiadających im punktów na planszy szachowej

# Przetwarzanie obrazów
for i in range(1, 23):
    # Wczytanie obrazu
    img_path = f"zdjecie ({i}).jpg"
    img = cv2.imread(img_path)
    height, width = img.shape[:2]
    new_height = int(height/6)
    new_width = int(width/6)
    img = cv2.resize(img, (new_width, new_height))
    if img is None:
        print(f"Nie udało się wczytać obrazu {img_path}.")
        continue

    # Przetwarzanie obrazu
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, (COLS, ROWS), None)

    # Jeśli znaleziono punkty planszy szachowej
    if ret:
     obj_points.append(np.zeros((COLS * ROWS, 3), np.float32))
     obj_points[-1][:, :2] = np.mgrid[0:COLS, 0:ROWS].T.reshape(-1, 2)
     img_points.append(corners)

    # Wizualizacja punktów planszy szachowej na obrazie
    img = cv2.drawChessboardCorners(img, (COLS, ROWS), corners, ret)

    # Wyświetlanie obrazu
    cv2.imshow('Calibration', img)
    cv2.waitKey(100)

cv2.destroyAllWindows()

# Kalibracja kamery
if len(obj_points) > 0:
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, gray.shape[::-1], None, None)
    with open('C:/Users/Maciej Wecki/Desktop/Studia Magisterskie/CVAPR/Projekt/parametry.txt','w') as file:
        file.write("RET"+ '\n' +str(ret) + '\n' + "MTX" + '\n' +str(mtx) + '\n' + "DIST" + '\n' + str(dist) + '\n' + 'RVECS' + '\n' + str(rvecs) + '\n' + "TVECS" + '\n' + str(tvecs))
        file.close()
    print("Kalibracja zakończona pomyślnie.")
else:
    print("Nie znaleziono punktów planszy szachowej na żadnym z obrazów.")



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