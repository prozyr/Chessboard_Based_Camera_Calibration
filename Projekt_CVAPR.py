import cv2
import numpy as np
#img = cv2.imread("lenna.png")

#while True:
#cv2.imshow("obraz", img)

cap = cv2.VideoCapture(0)

while True:
    
    ret, frame  = cap.read()
    
    grayframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #grayframe = cv2.rectangle(frame, (100,100),(400,400), (0,255,0),2 )
    
    _, threshold_frame = cv2.threshold(grayframe, 70, 255, cv2.THRESH_BINARY)    
    
    ret1, corners = cv2.findChessboardCorners(grayframe, (7,7), None)
    
    if ret1 == True:
        cv2.drawChessboardCorners(frame, (7,7),corners,ret1)
        
    
    #cv2.imshow('Wykryte obiekty',threshold_frame)
    
    cv2.imshow("obraz z kamery",frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    
cap.release()
cv2.destroyAllWindows()
