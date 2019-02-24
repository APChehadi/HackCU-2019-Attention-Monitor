import cv2
import numpy as np
from facial import EyeDetector
import time


cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
cv2.resizeWindow('frame', 1920, 1080)

class Driver:

	def __init__(self):
		#change source of videocapture based on webcam USB slot
		self.cap = cv2.VideoCapture(4)
		self.eyedec = EyeDetector()
		self.runningTotal = 0
		self.runningResult = 0
		self.total = 0
		self.result = 0
		self.looking = False
		self.start = time.time()
		self.postTimer = 0
		self.elapsed = 0

		self.loop()

	def loop(self):
		while True:
			self.start = time.time()
			_, frame = self.cap.read()
			res = self.eyedec.detect(frame)

			self.elapsed = time.time() - self.start
			self.postTimer += self.elapsed

			self.result += res * self.elapsed
			self.total += self.elapsed
			self.runningResult += res * self.elapsed
			self.runningTotal += self.elapsed

			#adjust post timer
			if self.postTimer > 5:
				print("Current: %f%%, Running: %f%%" % (int(self.result * 100 / self.total), int(self.runningResult * 100 / self.runningTotal)))
				self.result = 0
				self.total = 0
				self.postTimer = 0

			frame = self.eyedec.getFrame()
			cv2.imshow('frame', frame)

			k = cv2.waitKey(1) & 0xFF
			if k == 27:
				break

	def __del__(self):
		self.cap.release()
		cv2.destroyAllWindows()



dr = Driver()
del dr