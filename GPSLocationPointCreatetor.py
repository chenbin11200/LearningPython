import xml.etree.cElementTree as ET
import math
import urllib2
import json
from decimal import *

def createGPSFile4IOS(lat, lng):
    gpx = ET.Element("gpx", version="1.1", creator="Xcode")
    wpt = ET.SubElement(gpx, "wpt", lat="%.6f" % lat, lon="%.6f" % lng)
    ET.SubElement(wpt, "name").text = "PokemonLocation"
    ET.ElementTree(gpx).write("PokemonLocation.gpx")


def rad(angle):
    return float(angle) * math.pi / 180


# http://www.cnblogs.com/zrhai/p/3817492.html
# http://www.ucbbs.org/cgi-bin/bbs/ccb/topic_view.cgi?forum=1&article_id=0101080324231941&class=1
# Calculate max latitude & longitude difference according to a certain latitude and distance(in meter)
# The result is a square area
# Distance in meter
def getMaxDeviation(lat, distance):
    EARTH_RADIUS = 6377.830  # in km
    radLat = rad(lat)
    latRatio = 180 / (math.pi * EARTH_RADIUS)
    lngRatio = latRatio / math.cos(radLat)
    latDeviation = distance / 1000.0 * latRatio  # in meter
    lngDeviation = distance / 1000.0 * lngRatio # in meter
    return {"lat": latDeviation, "lng": lngDeviation}


def getDistanceInLat(lat, distance):
    lat = getMaxDeviation(lat, distance)["lat"]
    lng = getMaxDeviation(lat, distance)["lng"]
    return math.sqrt(lat*lat + lng*lng)


def getPathLineRad(startLocationPoint, destinationLocationPoint):
    x1 = Decimal(startLocationPoint['lat'])
    y1 = Decimal(startLocationPoint['lng'])
    x2 = Decimal(destinationLocationPoint['lat'])
    y2 = Decimal(destinationLocationPoint['lng'])
    return math.atan2(y2-y1, x2-x1)


def getLocationFromController():
    try:
        response = urllib2.urlopen("http://192.168.178.25/", timeout=3)
        geo = json.load(response)
        if geo != None:
            lastLat = geo["lat"]
            lastLng = geo["lng"]
        return {"lat":float(lastLat), "lng":float(lastLng)}

    except urllib2.URLError as e:
        print e.reason


def read_from_gps():
    tree = ET.parse("PokemonLocation.gpx")
    lat = tree.findall("./wpt")[0].attrib['lat']
    lng = tree.findall("./wpt")[0].attrib['lon']
    return{"lat": float(lat), "lng": float(lng)}

