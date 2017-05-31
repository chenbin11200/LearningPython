import os
import time

def clickAction():
    #os.system("./autoClicker -x 750 -y 400")
    #os.system("./autoClicker -x 750 -y 450")
    #os.system("./autoClicker -x 750 -y 450")
    if os.path.isfile("click.applescript"):
        os.system("osascript click.applescript")
    print "changing location"
    time.sleep(1)