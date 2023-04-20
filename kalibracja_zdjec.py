import numpy as np
import cv2

# Wymiary planszy szachowej
ROWS = 7
COLS = 7

# Przygotowanie pustych list punktów na planszy szachowej i odpowiadających im punktów na obrazie
img_points = []  # lista punktów na obrazie
obj_points = []  # lista odpowiadających im punktów na planszy szachowej

# Przetwarzanie obrazów
for i in range(1, 23):
    # Wczytanie obrazu
    img_path = f"images/zdjecie ({i}).jpg"
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
        print(corners)
    input()
    # Wizualizacja punktów planszy szachowej na obrazie
    img = cv2.drawChessboardCorners(img, (COLS, ROWS), corners, ret)

    # Wyświetlanie obrazu
    cv2.imshow('Calibration', img)
    cv2.waitKey(100)

cv2.destroyAllWindows()

# Kalibracja kamery
# if len(obj_points) > 0:
#     ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, gray.shape[::-1], None, None)
#     np.savetxt('plik.txt', (ret, mtx, dist, rvecs, tvecs))
#     print("Kalibracja zakończona pomyślnie.")
# else:
#     print("Nie znaleziono punktów planszy szachowej na żadnym z obrazów.")
