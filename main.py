from Character import *
from WalkPattern import *
import GPSLocationPointCreatetor


def simpleUI():
    user_input = raw_input("Please set current location, by "
                           "1. from GPS file "
                           "2. from controller")
    currentLocation = None

    if user_input == "1":
        currentLocation = GPSLocationPointCreatetor.read_from_gps()
    elif user_input == "2":
        currentLocation = GPSLocationPointCreatetor.getLocationFromController()


    trainer = Character(currentLocation)

    print("current location "+str(currentLocation["lat"])+"," +str(currentLocation["lng"]))

    print "Dear master, what you want me to do?"

    print "1. Go to target location"

    user_input = raw_input()

    if trainer.targetLocationPoint == None:
        print "unknown target location, please set target location"
        setTargetLocation = raw_input()
        trainer.setTargetLocation()
        print("target location " + str(trainer.targetLocationPoint["lat"]) +"," +str(trainer.targetLocationPoint["lng"]))
        trainer.walkPattern = WalkPattern(trainer, True)
        trainer.walkPattern.start()


def easyTest():
    currentLocation = {"lat": float(32.711517), "lng": float(-117.164686)}
    targetLocation = {"lat": float(32.719835), "lng": float(-117.161195)}
    trainer = Character(currentLocation)
    trainer.targetLocationPoint = targetLocation
    trainer.walkPattern = WalkPattern(trainer, False)
    trainer.walkPattern.start()


easyTest()