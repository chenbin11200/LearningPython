import numpy as np
from matplotlib import pyplot as plt

import math
from decimal import Decimal

Speed = 5  # m/s
SearchRange = 20  # meter


def startSearching(searchCenter):
    searchMaxRadius = 150
    radius = 20
    eachStepPlusRadius = 0.3

    centerX1 = searchCenter["lat"]
    centerY1 = searchCenter["lng"]

    searchMaxRadius_T = getMaxDeviation(centerX1, searchMaxRadius)["lat"]
    radius_T = getDistanceInLat(centerX1, radius)
    eachStepPlusRadius_T = getDistanceInLat(centerX1, eachStepPlusRadius)
    speed_T = getDistanceInLat(centerX1, Speed)

    startPoint = {"lat": centerX1 + getMaxDeviation(centerX1, radius)["lat"], "lng": centerY1}
    x=[]
    y=[]

    print(centerX1, centerY1)
    print(startPoint["lat"], startPoint["lng"])

    x.append(centerX1)
    y.append(centerY1)
    x.append(startPoint["lat"])
    y.append(startPoint["lng"])
    central_rad = 0

    while radius_T <= searchMaxRadius_T:
        radius_T += getEachStepPlusRadius_T(speed_T, radius_T, getDistanceInLat(centerX1, SearchRange))
        central_rad += speed_T / radius_T
        x2 = radius_T * math.cos(central_rad) + centerX1
        y2 = radius_T * math.sin(central_rad) + centerY1
        write_to_GPS({"lat": x2, "lng": y2})
        startPoint["lat"] = x2
        startPoint["lng"] = y2
        print(x2, y2)
        x.append(x2)
        y.append(y2)

    plt.figure()
    #plt.xlim(0, 100)
    #plt.ylim(0, 30)
    plt.plot(x, y, 'o')
    plt.show()


def getEachStepPlusRadius_T (distance_T, currentRadius_T, searchRangeRadius_T):
    return distance_T/(2*math.pi*currentRadius_T) * searchRangeRadius_T


def convertMeter(meter):
    return Decimal(meter / 10000)


# Write to file and then click to pass the GPS
def write_to_GPS(point):
    lastLat = point["lat"]
    lastLng = point["lng"]
    gpx = ET.Element("gpx", version="1.1", creator="Xcode")
    wpt = ET.SubElement(gpx, "wpt", lat=lastLat, lon=lastLng)
    ET.SubElement(wpt, "name").text = "PokemonLocation"
    ET.ElementTree(gpx).write("PokemonLocation.gpx")
    print "Location Updated!", "latitude:", lastLat, "longitude:", lastLng


def click2ChangeGPS(timespan = 1):
    os.system("./autoClicker -x 750 -y 400")
    os.system("./autoClicker -x 750 -y 450")
    os.system("./autoClicker -x 750 -y 450")
    time.sleep(timespan)


def rad(angle):
    return angle * math.pi / 180


# http://www.cnblogs.com/zrhai/p/3817492.html
# http://www.ucbbs.org/cgi-bin/bbs/ccb/topic_view.cgi?forum=1&article_id=0101080324231941&class=1
# 计算在某个纬度的最大偏移经纬度，单位是米，计算的是一个矩形区域
def getMaxDeviation(lat, distance):
    EARTH_RADIUS = 6377.830  # in km
    radLat = rad(lat)
    latRatio = 180 / (math.pi * EARTH_RADIUS)
    lngRatio = latRatio / math.cos(radLat)
    latDeviation = distance / 1000 * latRatio  # in meter
    lngDeviation = distance / 1000 * lngRatio  # in meter
    return {"lat": latDeviation, "lng": lngDeviation}


def getDistanceInLat(lat, distance):
    lat = getMaxDeviation(lat, distance)["lat"]
    lng = getMaxDeviation(lat, distance)["lng"]
    return math.sqrt(lat*lat + lng*lng)



def test():
    startSearching({"lat":53.5529891641475, "lng": 9.99261278100636})

test()
