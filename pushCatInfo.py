import pyrebase
from datetime import datetime
import json
from json import JSONEncoder

modelPassword = "password"

config = {
    "apiKey": "AIzaSyB6SIaAjYBqpVSibHJD_ORtk2_NCEYTtbs",
    "authDomain": "healthycatdatabase.firebaseapp.com",
    "databaseURL": "https://healthycatdatabase-default-rtdb.firebaseio.com",
    "storageBucket": "healthycatdatabase.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

with open('catInfo.json') as json_file:
    data = json.load(json_file)

newCurrentWeight = data['currentWeightLBS']

#Update Current Weight
db.child("usersData").child(modelPassword).update({"currentWeightLBS": newCurrentWeight})

#update list of historical weight data
currentHistWeightData = db.child("usersData").child("password").child("historicalWeightData").get().val()
key = str(len(currentHistWeightData))

now = datetime.now()

calendarType = "iso8601"
id = "ISO"
dayOfMonth = now.day
dayOfWeek = now.strftime("%A").upper()
dayOfYear = int(now.strftime('%j'))
hour = now.hour
minute = now.minute
month = now.strftime("%B").upper()
monthValue = now.month
nano = 0
second = now.second
year = now.year

data = {
    "usersData/password/historicalWeightData/" + key: {
        "Time": {
            "chronology": {
                "calendarType": calendarType,
                "id": id
            },
            "dayOfMonth": dayOfMonth,
            "dayOfWeek": dayOfWeek,
            "dayOfYear": dayOfYear,
            "hour": hour,
            "minute": minute,
            "month": month,
            "monthValue": monthValue,
            "nano": nano,
            "second": second,
            "year": year
        },
        "Weight": newCurrentWeight
    }
}

db.update(data)

