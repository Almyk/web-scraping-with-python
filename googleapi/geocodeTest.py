# This is a script made for testing out the google APIs
# for geocode, timezone and elevation
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import time, datetime
import json

# alternative way to get timestamp:
# timestamp = time.mktime(datetime.datetime.today().timetuple())

# open api key
keyFile = open("api.key", 'r')
key = keyFile.readline()
keyFile.close()
address = "1+Science+Park+Boston+MA+02114"

def getGeoInfo(address):
    global key
    response = urlopen("https://maps.googleapis.com/maps/api/geocode/json?address="+address+"&key="+key).read().decode('utf-8')
    return json.loads(response)

def getLatitude(geoInfo):
    return geoInfo.get("results")[0].get("geometry").get("location").get("lat")

def getLongitude(geoInfo):
    return geoInfo.get("results")[0].get("geometry").get("location").get("lng")

def getTimeZoneUsingLongAndLat(lat, lng):
    global key
    timestamp = time.time()
    response = urlopen("https://maps.googleapis.com/maps/api/timezone/json?location=%f"%(lat)+",%f"%(lng)+"&timestamp=%f"%(timestamp)+"&key="+key).read().decode('utf-8')
    jsonObj = json.loads(response)
    return jsonObj.get("timeZoneName")

def getElevation(lat, lng):
    global key
    response = urlopen("https://maps.googleapis.com/maps/api/elevation/json?locations=%f"%lat+",%f"%lng+"&key="+key).read().decode('utf-8')
    jsonObj = json.loads(response)
    return jsonObj.get("results")[0].get("elevation")

def getAddress(jsonObj):
    return jsonObj.get("results")[0].get("formatted_address")

geoInfo = getGeoInfo(address)
latitude = getLatitude(geoInfo)
longitude = getLongitude(geoInfo)
timeZone = getTimeZoneUsingLongAndLat(latitude, longitude)
elevation = getElevation(latitude, longitude)
formattedAddress = getAddress(geoInfo)
print("Address: "+formattedAddress)
print("Time Zone: "+timeZone)
print("Elevation: %.2fm"%elevation)
