import cv2
import numpy as np


class EyeDetector:

	# __init__(): initialize locations of haarcascade xml files
	def __init__(self):
		#change location of these if xml files are moved
		self.faceCascade = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')
		#self.faceCascade = cv2.CascadeClassifier('data/haarcascade_frontalface_alt2.xml')
		self.eyeCascade = cv2.CascadeClassifier('data/haarcascade_eye.xml')
		self.publish = 0

	# getFrame(): returns computed frame with objects 
	def getFrame(self):
		return self.publish

	# detect(frame): takes opencv frame, saves computed image, and returns boolean pupils found
	def detect(self, frame):
		found = False
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		faces = self.faceCascade.detectMultiScale(gray, 1.1, 5)
		for (x, y, w, h) in faces:
			cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
			roi_gray = gray[y:y+h, x:x+w]
			roi_color = frame[y:y+h, x:x+w]
			eyes = self.eyeCascade.detectMultiScale(roi_gray, 1.1, 10)
			for (ex, ey, ew, eh) in eyes:
				cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)				
				blur = cv2.medianBlur(roi_gray[ey:ey+eh, ex:ex + ew], 7)
				edges = cv2.Canny(blur, 100, 200)
				contours, heirarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE, offset=(ex, ey))
				centers = []
				for cont in contours:
					perimeter = cv2.arcLength(cont, True)
					epsilon = 0.04 * perimeter
					approx = cv2.approxPolyDP(cont, epsilon, True)
					(x, y), radius = cv2.minEnclosingCircle(cont)
					center = (int(x), int(y))
					radius = int(radius)
					centers += [center]
					cv2.drawContours(roi_color, [approx], -1, (0, 0, 255), 3)
				if len(centers) > 0:
					found = True
					avg = [0, 0]
					for center in centers:
						avg[0] += center[0]
						avg[1] += center[1]
					avg[0] = avg[0] / len(centers)
					avg[1] = avg[1] / len(centers)
					cv2.circle(roi_color, (int(avg[0]), int(avg[1])), 9, (255, 0, 0), 2)
		self.publish = frame
		return found