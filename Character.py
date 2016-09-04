import decimal
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
        self.startLocationPoint = currentLocationPoint

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
        startPoint = {"lat":self.currentLocationPoint["lat"],"lng":self.currentLocationPoint["lng"]}
        targetPoint = {"lat":targetLocationPoint["lat"],"lng":targetLocationPoint["lng"]}

        pathLineRad = GPSLocationPointCreatetor.getPathLineRad(self.currentLocationPoint, targetLocationPoint)
        distanceAtLat = GPSLocationPointCreatetor.getDistanceInLat(self.currentLocationPoint['lat'],
                                                                   Character.WalkSpeed)
        differenceInLat = GPSLocationPointCreatetor.getMaxDeviation(self.currentLocationPoint['lat'],
                                                                     Character.WalkSpeed)['lat']

        realChangeInLat = (differenceInLat/distanceAtLat)*Character.WalkSpeed
        realChangeInLng = realChangeInLat*math.tan(pathLineRad)

        while self.inRangeOf(self.currentLocationPoint, startPoint, targetPoint) :
            self.currentLocationPoint['lat'] += realChangeInLat
            self.currentLocationPoint['lng'] += realChangeInLng
            #  Helper.updateGPSLocation(self.currentLocationPoint['lat'], self.currentLocationPoint['lng'])
            GPSLocationPointCreatetor.createGPSFile4IOS(float(self.currentLocationPoint['lat']), float(self.currentLocationPoint['lng']))
            self.recordInMemory()
        #  Helper.update_gps_location(targetLocationPoint['lat'], targetLocationPoint['lng'])
        GPSLocationPointCreatetor.createGPSFile4IOS(targetLocationPoint['lat'], targetLocationPoint['lng'])
        self.recordInMemory()
        print("Reach and point, wait to start new trip.")
        return

    def setStartPoint(self):
        self.startLocationPoint = GPSLocationPointCreatetor.getLocationFromController()

    def setTargetLocation(self):
        self.targetLocationPoint = GPSLocationPointCreatetor.getLocationFromController()

    def recordInMemory(self):
        self.routeMemory.append(self.currentLocationPoint)

    def clearMemory(self):
        self.routeMemory = []

    def inRangeOf(self, currentLocation, startLocation, targetLocation):
        latInRange = None
        if(startLocation["lat"]>targetLocation["lat"]):
            latInRange = currentLocation["lat"]>=targetLocation["lat"] and currentLocation["lat"]<= startLocation["lat"]
        else:
            latInRange = currentLocation["lat"] <= targetLocation["lat"] and currentLocation["lat"] >= startLocation["lat"]
        lngInRange = None
        if (startLocation["lng"] > targetLocation["lng"]):
            lngInRange = currentLocation["lng"] >= targetLocation["lng"] and currentLocation["lng"] <= startLocation[
                "lat"]
        else:
            lngInRange = currentLocation["lng"] <= targetLocation["lng"] and currentLocation["lng"] >= startLocation[
                "lng"]
        return latInRange and lngInRange
