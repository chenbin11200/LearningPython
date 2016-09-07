from decimal import *
import math
import Helper
import GPSLocationPointCreatetor


class Character:
    WalkSpeed = 5  # m/s
    SearchRange = 20  # meter

    def __init__(self, currentLocationPoint):
        self.currentLocationPoint = currentLocationPoint
        self.routeMemory = []
        self.targetLocationPoint = None
        self.startLocationPoint = None

    def moveTo(self, targetLocationPoint):
        """
            x1 = self.currentLocationPoint['lat']
            y1 = self.currentLocationPoint['lng']
            x2 = self.targetLocationPoint['lat']
            y2 = self.targetLocationPoint['lng']

        latRange = range(min(self.currentLocationPoint['lat'], targetLocationPoint['lat']),
                         max(self.currentLocationPoint['lat'], targetLocationPoint['lat']))
        lngRange = range(min(self.currentLocationPoint['lng'], targetLocationPoint['lng']),
                         max(self.currentLocationPoint['lng'], targetLocationPoint['lng']))
        """
        startPoint = {"lat": self.currentLocationPoint["lat"], "lng": self.currentLocationPoint["lng"]}
        targetPoint = {"lat": targetLocationPoint["lat"], "lng": targetLocationPoint["lng"]}

        pathLineRad = GPSLocationPointCreatetor.getPathLineRad(self.currentLocationPoint, targetLocationPoint)

        distanceAtLat = GPSLocationPointCreatetor.getDistanceInLat(self.currentLocationPoint['lat'],
                                                                   Character.WalkSpeed)
        differenceInX = GPSLocationPointCreatetor.getMaxDeviation(self.currentLocationPoint['lat'],
                                                                  Character.WalkSpeed)['lng']
        differenceInY = differenceInX * math.tan(pathLineRad)

        differenceInLine = differenceInX / math.cos(pathLineRad)

        #  (differenceInX/differenceInLine)*differenceInX

        directionInX = 1 if targetPoint['lng']-startPoint['lng'] >= 0 else -1
        realChangeInX = (differenceInX/differenceInLine)*differenceInX  # * directionInX
        realChangeInY = realChangeInX * math.tan(pathLineRad)

        while self.inRangeOf(self.currentLocationPoint, startPoint, targetPoint):
            self.currentLocationPoint['lng'] += realChangeInX
            self.currentLocationPoint['lat'] += realChangeInY
            #  Helper.updateGPSLocation(self.currentLocationPoint['lat'], self.currentLocationPoint['lng'])
            GPSLocationPointCreatetor.createGPSFile4IOS(float(self.currentLocationPoint['lat']),
                                                        float(self.currentLocationPoint['lng']))
            # Helper.clickAction()
            self.recordInMemory()
        Helper.update_gps_location(targetLocationPoint['lat'], targetLocationPoint['lng'])
        GPSLocationPointCreatetor.createGPSFile4IOS(targetLocationPoint['lat'], targetLocationPoint['lng'])
        Helper.clickAction()
        self.recordInMemory()
        print("Reach and point, wait to start new trip.")
        return

    def setStartPoint(self):
        self.startLocationPoint = GPSLocationPointCreatetor.getLocationFromController()

    def setTargetLocation(self):
        self.targetLocationPoint = GPSLocationPointCreatetor.getLocationFromController()

    def recordInMemory(self):
        self.routeMemory.append(
            {"lat": self.currentLocationPoint["lat"], "lng": self.currentLocationPoint["lng"]})

    def clearMemory(self):
        self.routeMemory = []

    def inRangeOf(self, currentLocation, startLocation, targetLocation):
        latInRange = None
        if startLocation["lat"] > targetLocation["lat"]:
            latInRange = targetLocation["lat"] <= currentLocation["lat"] <= startLocation["lat"]
        else:
            latInRange = targetLocation["lat"] >= currentLocation["lat"] >= startLocation["lat"]
        lngInRange = None
        if startLocation["lng"] > targetLocation["lng"]:
            lngInRange = targetLocation["lng"] <= currentLocation["lng"] <= startLocation["lat"]
        else:
            lngInRange = targetLocation["lng"] >= currentLocation["lng"] >= startLocation["lng"]
        return latInRange and lngInRange
