import urllib2
import json

class WalkPattern:

    def __init__(self, trainer, gobackAfterArrive = True):
        self.description = "Walk by Google map"
        self.origin = str(trainer.currentLocationPoint["lat"])+","+str(trainer.currentLocationPoint["lng"])
        self.destination = str(trainer.targetLocationPoint["lat"])+","+str(trainer.targetLocationPoint["lng"])
        self.trainer = trainer
        self.gobackAfterArrive = gobackAfterArrive
        self.googleApiKey = self.__readGoogleKey()


    def start(self):
        while 1:
            self.walkStrategy()
            if self.gobackAfterArrive:
                self.origin, self.destination = self.destination, self.origin
                continue
            else:
                break


    def walkStrategy(self):
        try:
            response = urllib2.urlopen(
                "https://maps.googleapis.com/maps/api/directions/json?origin=" + self.origin + "&destination="
                + self.destination + "&mode=walking&key="+self.googleApiKey, timeout=3)
            route = json.load(response)

            for item in route["routes"][0]["legs"][0]["steps"]:
                #   self.trainer.moveTo({"lat":item['start_location'], "lng":item['end_location']})
                self.trainer.moveTo(item['end_location'])
        except urllib2.URLError as e:
            print(e.reason)


    def __readGoogleKey(self):
        key = open("GoogleApiKey.ppk", 'r').read()
        return key

