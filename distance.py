import requests

#google api key
key = ""

#rapidAPI key
rapidapiKey = ""

#Google API
def getDistance(source, dest):
	return requests.post("https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + source + "&destinations=" + dest + "&key=" + key)

def getGeocode(address):
	return requests.post("https://maps.googleapis.com/maps/api/geocode/json?address=" + address + "&key=" + key)

def getGeolocation():
	return requests.post("https://www.googleapis.com/geolocation/v1/geolocate?key=" + key)

def getWeather(lat, lon):
	return requests.get("https://community-open-weather-map.p.rapidapi.com/weather?lat=" + lat + "&lon=" + lon + "&units=imperial", headers={"X-RapidAPI-Key": rapidapiKey})
