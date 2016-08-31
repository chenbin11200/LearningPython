import xml.etree.cElementTree as ET
import math


def createGPSFile4IOS(lat, lng):
    gpx = ET.Element("gpx", version="1.1", creator="Xcode")
    wpt = ET.SubElement(gpx, "wpt", lat="%.6f" % lat, lon="%.6f" % lng)
    ET.SubElement(wpt, "name").text = "PokemonLocation"
    ET.ElementTree(gpx).write("PokemonLocation.gpx")


def rad(angle):
    return angle * math.pi / 180


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
    x1 = startLocationPoint['lat']
    y1 = startLocationPoint['lng']
    x2 = destinationLocationPoint['lat']
    y2 = destinationLocationPoint['lng']
    return math.atan2(y2-y1, x2-x1)


