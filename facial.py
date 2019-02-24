import cv2
import numpy as np

#cap = cv2.VideoCapture(4)

#_, frame = cap.read()
#cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
#cv2.resizeWindow('frame', 1920, 1080)
#cv2.namedWindow('eyes', cv2.WINDOW_NORMAL)
#cv2.resizeWindow('eyes', 1920, 1080)


#faceCascade = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')
#eyeCascade = cv2.CascadeClassifier('data/haarcascade_eye.xml')
#profileCascade = cv2.CascadeClassifier('data/haarcascade_profileface.xml')

#leftEyeCascade = cv2.CascadeClassifier('data/haarcascade_lefteye_2splits.xml')
#rightEyeCascade = cv2.CascadeClassifier('data/haarcascade_righteye_2splits.xml')

class EyeDetector:

	# __init__(): initialize locations of haarcascade xml files
	def __init__(self):
		#change location of these if xml files are moved
		self.faceCascade = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')
		self.eyeCascade = cv2.CascadeClassifier('data/haarcascade_eye.xml')
		self.publish = 0

	def getFrame(self):
		return self.publish

	# detect(frame): takes opencv frame, saves computed image, and returns boolean pupils found
	def detect(self, frame):
		found = False
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		faces = self.faceCascade.detectMultiScale(gray, 1.3, 5)
		for (x, y, w, h) in faces:
			cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
			roi_gray = gray[y:y+h, x:x+w]
			roi_color = frame[y:y+h, x:x+w]
			eyes = self.eyeCascade.detectMultiScale(roi_gray, 1.1, 10)
			#blur = cv2.GaussianBlur(roi_gray, (5, 5), 0)
			#blur = cv2.medianBlur(roi_gray, 7)
			for (ex, ey, ew, eh) in eyes:
				cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)				
				blur = cv2.medianBlur(roi_gray[ey:ey+eh, ex:ex + ew], 7)
				edges = cv2.Canny(blur, 100, 200)
				contours, heirarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE, offset=(ex, ey))
				centers = []
				for cnt in contours:
					perimeter = cv2.arcLength(cnt, True)
					epsilon = 0.04 * perimeter
					approx = cv2.approxPolyDP(cnt, epsilon, True)
					(x, y), radius = cv2.minEnclosingCircle(cnt)
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




		




#while True:
#	_, frame = cap.read()
#	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#	faces = faceCascade.detectMultiScale(gray, 1.3, 5)

	#leftEyes = leftEyeCascade.detectMultiScale(gray, 1.3, 5)
	#rightEyes = rightEyeCascade.detectMultiScale(gray, 1.3, 5)
	#profiles = profileCascade.detectMultiScale(gray, 1.3, 5)

	#for (x, y, w, h) in leftEyes:
	#	cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

	#for (x, y, w, h) in rightEyes:
	#	cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

#	for (x, y, w, h) in faces:
#		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
#		roi_gray = gray[y:y+h, x:x+w]
#		roi_color = frame[y:y+h, x:x+w]
#		eyes = eyeCascade.detectMultiScale(roi_gray, 1.1, 10)
		#blur = cv2.GaussianBlur(roi_gray, (5, 5), 0)
		#blur = cv2.medianBlur(roi_gray, 7)
#		for (ex, ey, ew, eh) in eyes:
#			cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
			
			#thr = cv2.adaptiveThreshold(blur[ey:ey+eh, ex:ex+ew], 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
			#ret, thr = cv2.threshold(blur[ey:ey+eh, ex:ex+ew], 250, 255, cv2.THRESH_BINARY)
#			blur = cv2.medianBlur(roi_gray[ey:ey+eh, ex:ex+ew], 7)
#			edges = cv2.Canny(blur, 100, 200)
#			contours, heirarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE, offset=(ex, ey))
#			centers = []
#			for cnt in contours:
#				perimeter = cv2.arcLength(cnt, True)
#				epsilon = 0.04 * perimeter
#				approx = cv2.approxPolyDP(cnt, epsilon, True)
#				(x, y), radius = cv2.minEnclosingCircle(cnt)
#				center = (int(x), int(y))
#				radius = int(radius)
#				centers += [center]
				#cv2.circle(roi_color, center, radius, (0, 0, 255), 2)
#				cv2.drawContours(roi_color, [approx], -1, (0, 0, 255), 3)
			#find center
#			if len(centers) > 0:
#				avg = [0, 0]
#				for center in centers:
#					avg[0] += center[0]
#					avg[1] += center[1]
#				avg[0] = avg[0] / len(centers)
#				avg[1] = avg[1] / len(centers)
#				cv2.circle(roi_color, (int(avg[0]), int(avg[1])), 9, (255, 0, 0), 2)





		#roi_gray = cv2.medianBlur(roi_gray, 5)
		#roi_gray = cv2.Canny(roi_gray, 100, 200)
		#circles = cv2.HoughCircles(roi_gray, cv2.HOUGH_GRADIENT, 1, roi_gray.shape[0],
		#	param1=100, param2=30, minRadius=1, maxRadius=30)

		#if circles is not None:
		#	circles = np.uint16(np.around(circles))
		#	for i in circles[0, :]:
		#		center = (i[0], i[1])
		#		cv2.circle(roi_color, center, 1, (0, 100, 100), 3)
		#		radius = i[2]
		#		cv2.circle(roi_color, center, radius, (255, 0, 255), 3)

		#cv2.imshow('eyes', thr)






	#for (x, y, w, h) in profiles:
	#	cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

#	cv2.imshow('frame', frame)



#	k = cv2.waitKey(1) & 0xFF
#	if k == 27:
#		break


#cap.release()
#cv2.destroyAllWindows()