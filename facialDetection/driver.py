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
		self.cap = cv2.VideoCapture(0)
		self.eyedec = EyeDetector()
		self.runningTotal = 0
		self.runningResult = 0
		self.total = 0
		self.result = 0
		self.looking = False
		self.strikes = 0
		self.smsSent = False
		self.geolocationRefresh = False
		self.start = time.time()
		self.begin = time.time()
		self.postTimer = 0
		self.elapsed = 0
		self.nonAttentionTimer = 0
		#as demo is with laptop without gps, location is based on ip address
		self.startLocation = geocoder.ip('me')
		f = open('user_settings.txt', 'r')
		self.user = f.readline().split(':')[1].split(chr(10))[0]
		self.URL = "http://" + f.readline().split(':')[1].split(chr(10))[0]
		#self.URL = "https://" + f.readline().split(':')[1].split(chr(10))[0]
		f.close()
		#fill addresses from Boulder CO
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
				self.looking = False
			else:				
				self.nonAttentionTimer = 0
				self.looking = True

			#adjust post timer
			if self.postTimer > 5:
				instantAverage = self.result / self.total
				overallAverage = self.runningResult / self.runningTotal
				print("Current EyeTrack Average: %i%%, Running EyeTrack Average: %i%%" % (int(instantAverage * 100), int(overallAverage * 100)))
				r = requests.post(self.URL + "/users/" + self.user + "/update/", 
					data={'instantEyeRatio':format(instantAverage, '.2f'), 
					'overallEyeRatio':format(overallAverage, '.2f'),
					'time': int(time.time() - self.begin)}
					)
				self.result = 0
				self.total = 0
				self.postTimer = 0

				self.geolocationRefresh = not self.geolocationRefresh
				if self.geolocationRefresh:
					result = distance.getGeolocation().json()
					weather = distance.getWeather(str(result['location']['lat']), str(result['location']['lng'])).json()
					print("At latitude: %.2f and longitude %.2f" % (weather['coord']['lat'], weather['coord']['lon']))
					print("The weather is %s with %i min and %i max" % (weather['weather'][0]['description'],
						int(weather['main']['temp_min']), int(weather['main']['temp_max'])))

			if self.nonAttentionTimer > 10:
				print("PLEASE PAY ATTENTION")
				#r = requests.post(self.URL + "/twilio")
				if not self.smsSent:
					self.smsSent = True
					r = requests.post(self.URL + "/twilio")

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
		dest = str(destpos['results'][0]['geometry']['location']['lat']) + "," + str(destpos['results'][0]['geometry']['location']['lng'])
		response = distance.getDistance(source, dest)
		#print(json.dumps(response.json(), indent=4, sort_keys=True))
		dist = response.json()['rows'][0]['elements'][0]['distance']['value']
		print("Traveling to: %s\n%s" % (response.json()['destination_addresses'][0], response.json()['rows'][0]['elements'][0]['distance']['text']))

		r = requests.post(self.URL + "/users/" + self.user + "/addDrive/", 
			data={'distTraveled': dist, 'eyeRatio':format(self.runningResult/self.runningTotal, '.2f'), 
			'timeSpent':int(time.time() - self.begin)})
		r = requests.post(self.URL + "/users/" + self.user + "/", data={'driving': False})



dr = Driver()
del dr
