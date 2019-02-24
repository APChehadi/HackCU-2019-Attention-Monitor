import numpy as np
import cv2 as cv 
import time


face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv.CascadeClassifier("haarcascade_lefteye_2splits.xml")

cap = cv.VideoCapture(0)
# cv.namedWindow("eye1", cv.WINDOW_NORMAL)
# cv.namedWindow("eye2", cv.WINDOW_NORMAL)
def nothing(z):
    pass

cv.namedWindow("TrackBars", cv.WINDOW_AUTOSIZE)

cv.createTrackbar("Top", 'TrackBars',0,255, nothing)
cv.createTrackbar("Bottom", 'TrackBars',0,255, nothing)

while True:
    
    ret, frame = cap.read()

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        cv.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyes:
            cv.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
        try:
            eye1 = eyes[0]
            eye2 = eyes[1]
            ex1,ey1,ew1,eh1 = eye1
            ex2,ey2,ew2,eh2 = eye2
            roi_eye1 = roi_gray[ey1:ey1+eh1,ex1:ex1+ex1]

            maxval = cv.getTrackbarPos("Top", "TrackBars")
            print("Max",maxvalue)
            minval = cv.getTrackbarPos("Bottom", "TrackBars")
            print("Min",minval)
            ret, thresh1 = cv.threshold(roi_eye1,minval,maxval, cv.THRESH_BINARY)
            cv.imshow("Thresh", thresh1)s


            # cv.imshow("eye1", roi_eye1)
            # cv.resizeWindow("eye1", 600, 600)
            roi_eye2 = roi_gray[ey2:ey2+eh2,ex2:ex2+ew2]
            # cv.imshow("eye2", roi_eye2)
            # roi_eye1 = frame[ey:ey+eh,ex:ex+ex]
        except:
            pass

    cv.imshow("frame", frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
