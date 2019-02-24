import requests

#google api key
key = "AIzaSyDg8vHOW6g5lLOPhVex902xO4E4QPPDYbc"

#rapidAPI key
rapidapiKey = "27f39824a7msh9e7433c797ab87fp1f6286jsn12e98b6e9682"

#RapidAPI :()
#response = requests.post("https://GoogleMapsDistanceMatrixstefan.skliarovV1.p.rapidapi.com/getBicyclingDistanceMatrix",
#  headers={
#    "X-RapidAPI-Key": "2a44635751msh2243a006353b957p19f690jsn06c4fb17b7fc",
#    "Content-Type": "application/x-www-form-urlencoded"
#  },
#  data={
#  	"origins": "40.5, -100.721",
#  	"destinations": "2414 Regent Dr, Boulder, CO 80309",
#  	"apiKey": "AIzaSyDg8vHOW6g5lLOPhVex902xO4E4QPPDYbc"
#  }
#)

#Google API
def getDistance(source, dest):
	return requests.post("https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + source + "&destinations=" + dest + "&key=" + key)

def getGeocode(address):
	return requests.post("https://maps.googleapis.com/maps/api/geocode/json?address=" + address + "&key=" + key)

def getGeolocation():
	return requests.post("https://www.googleapis.com/geolocation/v1/geolocate?key=" + key)

def getWeather(lat, lon):
	return requests.get("https://community-open-weather-map.p.rapidapi.com/weather?lat=" + lat + "&lon=" + lon + "&units=imperial", headers={"X-RapidAPI-Key": rapidapiKey})