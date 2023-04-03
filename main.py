import cv2
import numpy as np

# Za pomocą telefonu wyświetl szachownicę

############### Filtracja obrazu ####################
# Tworzenie maski filtru górnoprzepustowego
kernel = np.array([[-1,-1,-1],
                   [-1, 9,-1],
                   [-1,-1,-1]])

# Tworzenie macierzy dla operacji morfologicznej
kernel_morph = np.ones((2,2), np.uint8)
############### ################ ####################

cap = cv2.VideoCapture(0)

def bin_img(frame):
    # wykrycie krawędzi
    edges = cv2.Canny(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY),100,200)
    # uzupełnieine dziur
    edges = cv2.morphologyEx(edges, cv2.MORPH_DILATE, kernel_morph)
    # szukanie konturów
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    Vframe = frame
    # Wybór czworokątów, które reprezentują interesujący nas kształt
    quads = []
    vector_area = []        # TODO: próba odległości kamery od szachownicy
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 1000:
            vector_area = vector_area +  [area]
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.1 * perimeter, True)
            if len(approx) == 4:
                x, y, w, h = cv2.boundingRect(approx)
                if abs(w - h) < 50:
                    quads.append(approx)
    print(10000*8/(np.mean(vector_area))," mm") # TODO: próba odległości kamery od szachownicy
    # Narysowanie konturu czworokąta na oryginalnym obrazie
    for quad in quads:
        cv2.drawContours(Vframe, [quad], 0, (0, 255, 0), 2)

    return Vframe, edges


while True:

    ret, frame  = cap.read()

    frame_bin, edges = bin_img(frame)

    frame_bin2rgb = frame_bin
    edges = cv2.merge((edges, edges, edges)) # dummy RGB

    cv2.imshow("obraz z kamery",np.concatenate((frame_bin2rgb, frame, edges), axis=1))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()