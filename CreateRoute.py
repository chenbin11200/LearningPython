import urllib
import json
import math
import decimal
import Helper


locationDic = {"junfern":"53.553407,9.993283",
			   "junfern2":"53.553515,9.993396",
			   "wandsbek":"53.571726,10.066105",
			   "hbf":"53.5514118205899,10.0028820064209",
			   "Jynx":"53.579645,10.073675",
			   "lubeker3sakula":"53.563918,10.032260",
			   "zara":"53.5514516231933,10.0029038955589",
			   "target":"53.551955,9.994791"}

lastLat = decimal.Decimal(0.00)
lastLng = decimal.Decimal(0.00)


origin = "45.4003990824172,75.6813609156003"
destinaion = "40.780440,-73.963100"
gobackAfterArrive = False
speed = 30

def getPokemonLocation():
	global locationDic, origin, destinaion
	try:
		response = urllib.urlopen("https://maps.googleapis.com/maps/api/directions/json?origin="+origin+"&destination="+destinaion+"&mode=walking&key=", timeout = 3)
		return json.load(response)
	except urllib.URLError as e:
		print(e.reason)

def walking(startPoint, endPoint):
	global lastLat, lastLng
	x1 = startPoint['lat']
	y1 = startPoint['lng']
	x2 = endPoint['lat']
	y2 = endPoint['lng']
	lastLat = decimal.Decimal(x1)
	lastLng = decimal.Decimal(y1)
	a = y1 - y2
	b = x1 - x2
	c = math.sqrt(a*a + b*b)
	sinAngle = a/c
	cosAngle = b/c
	distance = decimal.Decimal(speed*0.000001)
	counter = 0
	while counter < c:
		lastLat = lastLat - distance * decimal.Decimal(cosAngle)
		lastLng = lastLng - distance * decimal.Decimal(sinAngle)
		counter = counter + distance
		Helper.updateGPSLocation(lastLat, lastLng)
	Helper.update_gps_location(lastLat, lastLng)
	print("clicking to endpoint!!")
	return

def generateXML():
	a = getPokemonLocation()
	for item in a["routes"][0]["legs"][0]["steps"]:
		walking(item['start_location'],
				item['end_location'])

def start():
	global origin, destinaion
	while 1:
		generateXML()
		if gobackAfterArrive :
			origin, destinaion = destinaion, origin
			continue
		else:
			break


def start(ori, tar):
	global origin, destinaion
	origin = ori
	destinaion = tar
	while 1:
		generateXML()
		if gobackAfterArrive:
			origin, destinaion = destinaion, origin
			continue
		else:
			break
