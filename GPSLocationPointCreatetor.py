import xml.etree.cElementTree as ET
import math

def createGPSFile4IOS(lat, lng):
    gpx = ET.Element("gpx", version="1.1", creator="Xcode")
    wpt = ET.SubElement(gpx, "wpt", lat="%.6f" % lat, lon="%.6f" % lng)
    ET.SubElement(wpt, "name").text = "PokemonLocation"
    ET.ElementTree(gpx).write("PokemonLocation.gpx")


def rad(angle):
    return angle * math.pi / 180


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