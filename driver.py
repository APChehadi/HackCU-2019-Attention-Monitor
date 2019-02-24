import cv2
import numpy as np
import time
import random
import requests
import geocoder
import json
from facial import EyeDetector
import distance




cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
cv2.resizeWindow('frame', 1920, 1080)

class Driver:

	def __init__(self):
		#change sourcle of videocapture based on webcam USB slot
		self.cap = cv2.VideoCapture(4)
		self.eyedec = EyeDetector()
		self.runningTotal = 0
		self.runningResult = 0
		self.total = 0
		self.result = 0
		self.looking = False
		self.start = time.time()
		self.begin = time.time()
		self.postTimer = 0
		self.elapsed = 0
		self.nonAttentionTimer = 0
		#as demo is with laptop without gps, location is based on ip address
		self.startLocation = geocoder.ip('me')
		f = open('user_settings.txt', 'r')
		self.user = f.readline().split(':')[1].split(chr(10))[0]
		self.URL = "https://" + f.readline().split(':')[1].split(chr(10))[0]

		f.close()
		self.addresses = []
		f = open('addresses.txt', 'r')
		for line in f.readlines():
			self.addresses += [line.split(chr(10))[0]]
		f.close()

		print(self.URL + "/users/" + self.user + "/")
		r = requests.post(self.URL + "/users/" + self.user + "/", data={'driving': True})
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

			if not res:
				self.nonAttentionTimer += self.elapsed
			else:
				self.nonAttentionTimer = 0

			#adjust post timer
			if self.postTimer > 5:
				instantAverage = self.result / self.total
				overallAverage = self.runningResult / self.runningTotal
				print("Current: %i%%, Running: %i%%" % (int(instantAverage * 100), int(overallAverage * 100)))
				r = requests.post(self.URL + "/users/" + self.user + "/update/", 
					data={'instantAverage':format(instantAverage, '.2f'), 
					'overallAverage':format(overallAverage, '.2f')}
					)
				self.result = 0
				self.total = 0
				self.postTimer = 0

			if self.nonAttentionTimer > 20:
				print("PLEASE PAY ATTENTION")

			frame = self.eyedec.getFrame()
			cv2.imshow('frame', frame)

			k = cv2.waitKey(1) & 0xFF
			if k == 27:
				break
			elif k == ord('s'): 
				# saving images for presenting
				cv2.imwrite('devImage.png', frame)
 
	def __del__(self):
		self.cap.release()
		cv2.destroyAllWindows()

		#this line would be replaced with gps
		#endLocation = geocoder.ip['me']
		position = self.startLocation.latlng
		source = str(position[0]) + "," + str(position[1])
		destpos = distance.getGeocode(random.choice(self.addresses)).json()

		#print(destpos)
		dest = str(destpos['results'][0]['geometry']['location']['lat']) + "," + str(destpos['results'][0]['geometry']['location']['lng'])

		response = distance.getDistance(source, dest)
		print(json.dumps(response.json(), indent=4, sort_keys=True))
		dist = response.json()['rows'][0]['elements'][0]['distance']['value']

		r = requests.post(self.URL + "/users/" + self.user + "/addDrive/", 
			data={'distTraveled': dist, 'eyeRatio':format(self.runningResult/self.runningTotal, '.2f'), 
			'timeSpent':int(time.time() - self.begin)})
		r = requests.post(self.URL + "/users/" + self.user + "/", data={'driving': False})



dr = Driver()
del dr