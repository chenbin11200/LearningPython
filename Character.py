import decimal
import math
import Helper


class Character:
    WalkSpeed = 5  # m/s
    SearchRange = 20  # meter

    def __init__(self, currentLocationPoint):
        self.currentLocationPoint = currentLocationPoint
        self.routeMemory = []

    def moveTo(self, targetLocationPoint):
        x1 = self.currentLocationPoint['lat']
        y1 = self.currentLocationPoint['lng']
        x2 = self.targetLocationPoint['lat']
        y2 = self.targetLocationPoint['lng']
        lastLat = decimal.Decimal(x1)
        lastLng = decimal.Decimal(y1)
        a = y1 - y2
        b = x1 - x2
        c = math.sqrt(a * a + b * b)
        sinAngle = a / c
        cosAngle = b / c
        distance = decimal.Decimal(Character.WalkSpeed * 0.000001)
        counter = 0
        while counter < c:
            lastLat = lastLat - distance * decimal.Decimal(cosAngle)
            lastLng = lastLng - distance * decimal.Decimal(sinAngle)
            counter = counter + distance
            Helper.updateGPSLocation(lastLat, lastLng)
        Helper.update_gps_location(lastLat, lastLng)
        print("clicking to endpoint!!")
        return

    def recordInMemory(self):
        self.routeMemory.append(self.currentLocationPoint)

    def clearMemory(self):
        self.routeMemory = []
