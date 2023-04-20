# Importowanie bibliotek
import numpy as np
import cv2
import glob
# Wymiary planszy szachowej
width = 8
height = 6

# Przygotowanie punktów w przestrzeni 3D
objp = np.zeros((height*width,3), np.float32)
objp[:,:2] = np.mgrid[0:width, 0:height].T.reshape(-1,2)

# Tablice do przechowywania punktów z obrazów i przestrzeni 3D
objpoints = [] # 3D points
imgpoints = [] # 2D points

images = []
# Wczytanie obrazów z plików
for i in range(1,23):
    images = images + [f"images/zdjecie ({i}).jpg"]

print(len(images))

# Iteracja przez wszystkie obrazy
for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # Wykrycie narożników planszy szachowej
    ret, corners = cv2.findChessboardCorners(gray, (width,height),None)

    # Jeśli narożniki zostały znalezione, dodaj punkty do listy
    if ret == True:
        objpoints.append(objp)
        imgpoints.append(corners)

        # Narysuj i wyświetl planszę szachową
        img = cv2.drawChessboardCorners(img, (width,height), corners, ret)
        cv2.imshow('img',img)
        cv2.waitKey(500)

# Kalibracja kamery
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

# Wyświetlenie wyników
print("Camera matrix:\n", mtx)
print("\nDistortion coefficients:\n", dist)
