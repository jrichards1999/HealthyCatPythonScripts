import pyrebase
import datetime
import json
from json import JSONEncoder

class Cat:
    def __init__(self, name, UID, currentWeightLBS, targetWeightLBS, feedingTimes, feedingSize,):
        self.name = name
        self.UID = UID
        self.currentWeightLBS = currentWeightLBS
        self.targetWeightLBS = targetWeightLBS
        self.feedingTimes = feedingTimes
        self.feedingSize = feedingSize

# subclass JSONEncoder
class CatEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.time):
            return dict(hour=o.hour, minute=o.minute, second=o.second)
        return o.__dict__


config = {
    "apiKey": "AIzaSyB6SIaAjYBqpVSibHJD_ORtk2_NCEYTtbs",
    "authDomain": "healthycatdatabase.firebaseapp.com",
    "databaseURL": "https://healthycatdatabase-default-rtdb.firebaseio.com",
    "storageBucket": "healthycatdatabase.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

name = db.child("usersData").child("password").child("name").get().val()
UID = db.child("usersData").child("password").child("UID").get().val()

#Most recent weight is already stored in the json file, not on firebase
with open('catInfo.json') as json_file:
    data = json.load(json_file)
currentWeightLBS = data['currentWeightLBS']

targetWeightLBS = db.child("usersData").child("password").child("targetWeightLBS").get().val()
feedingSize = db.child("usersData").child("password").child("feedingSize").get().val()
incomingFeedingTimes = db.child("usersData").child("password").child("feedingTimes").get().val()

feedingTimes = []
for i in range(len(incomingFeedingTimes)):
    hour = db.child("usersData").child("password").child("feedingTimes").child(i).child("hour").get().val()
    minute = db.child("usersData").child("password").child("feedingTimes").child(i).child("minute").get().val()
    second = db.child("usersData").child("password").child("feedingTimes").child(i).child("second").get().val()
    time = datetime.time(hour, minute, second)
    feedingTimes.append(time)

cat = Cat(name, UID, currentWeightLBS, targetWeightLBS, feedingTimes, feedingSize)

catJSONData = json.dumps(cat, indent=4, cls=CatEncoder)
json_file = open("catInfo.json", "w")
n = json_file.write(catJSONData)
json_file.close()
