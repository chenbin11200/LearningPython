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

    def moveTo(self, targetLocationPoint):
        """
            x1 = self.currentLocationPoint['lat']
            y1 = self.currentLocationPoint['lng']
            x2 = self.targetLocationPoint['lat']
            y2 = self.targetLocationPoint['lng']
        """
        latRange = range(min(self.currentLocationPoint['lat'], targetLocationPoint['lat']),
                         max(self.currentLocationPoint['lat'], targetLocationPoint['lat']))
        lngRange = range(min(self.currentLocationPoint['lng'], targetLocationPoint['lng']),
                         max(self.currentLocationPoint['lng'], targetLocationPoint['lng']))

        pathLineRad = GPSLocationPointCreatetor.getPathLineRad(self.currentLocationPoint, self.targetLocationPoint)
        distanceAtLat = GPSLocationPointCreatetor.getDistanceInLat(self.currentLocationPoint['lat'],
                                                                   Character.WalkSpeed)
        differenceInLat = GPSLocationPointCreatetor.getDistanceInLat(self.currentLocationPoint['lat'],
                                                                     Character.WalkSpeed)['lat']

        realChangeInLat = (differenceInLat/distanceAtLat)*Character.WalkSpeed
        realChangeInLng = realChangeInLat*math.tan(pathLineRad)

        while self.currentLocationPoint['lat'] in latRange and self.currentLocationPoint['lng'] in lngRange:
            self.currentLocationPoint['lat'] += realChangeInLat
            self.currentLocationPoint['lng'] += realChangeInLng
            Helper.updateGPSLocation(self.currentLocationPoint['lat'], self.currentLocationPoint['lng'])
            self.recordInMemory()
        Helper.update_gps_location(targetLocationPoint['lat'], targetLocationPoint['lng'])
        self.recordInMemory()
        print("Reach and point, wait to start new trip.")
        return

    def recordInMemory(self):
        self.routeMemory.append(self.currentLocationPoint)

    def clearMemory(self):
        self.routeMemory = []
