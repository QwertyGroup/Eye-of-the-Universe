import pyrebase

config = {
  "apiKey": "d32fd5583685d464c12c2893fd020bdc241d9cb3",
  "authDomain": "eyetheuniversecloud.firebaseio.com",
  "databaseURL": "https://eyetheuniversecloud.firebaseio.com/",
  "storageBucket": "eyetheuniversecloud.appspot.com",
  "serviceAccount": "Storage/Goo/GooCreds.json"
}

firebase = pyrebase.initialize_app(config)

pyre = firebase.database()

def ignite():
    return pyre