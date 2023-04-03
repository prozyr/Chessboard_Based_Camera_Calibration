import cv2
import numpy as np


# Wyświetlenie każdego obrazu na osobnym podwykresie

cap = cv2.VideoCapture(0)

# Tworzenie maski filtru górnoprzepustowego
kernel = np.array([[-1,-1,-1],
                   [-1, 9,-1],
                   [-1,-1,-1]])

# Tworzenie kernela
kernel_morph = np.ones((3,3), np.uint8)

def bin_img(frame):
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY),100,200) # wykrywanie krawędzi z użyciem funkcji Canny
    edges = cv2.morphologyEx(edges, cv2.MORPH_DILATE, kernel_morph)
    # ret,Vframe = cv2.threshold(edges,180,255,cv2.THRESH_BINARY) # binaryzacja krawędzi


    # Znalezienie konturów obrazu
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Wybór czworokątów, które reprezentują interesujący nas kształt
    quads = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 100:
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.1 * perimeter, True)
            if len(approx) == 4:
                x, y, w, h = cv2.boundingRect(approx)
                if abs(w - h) < 50:
                    quads.append(approx)

    # Narysowanie konturu czworokąta na oryginalnym obrazie
    for quad in quads:
        cv2.drawContours(frame, [quad], 0, (0, 255, 0), 2)


    Vframe = frame

    return Vframe, edges


while True:

    ret, frame  = cap.read()
    # frame_fHigh = cv2.filter2D(frame, -1, kernel)
    #frame_morph = cv2.morphologyEx(frame, cv2.MORPH_ERODE, kernel_morph)

    frame_bin, edges = bin_img(frame)

    frame_bin2rgb = frame_bin# cv2.merge((frame_bin, frame_bin, frame_bin))
    edges = cv2.merge((edges, edges, edges))

    cv2.imshow("obraz z kamery",np.concatenate((frame_bin2rgb, frame, edges), axis=1))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()