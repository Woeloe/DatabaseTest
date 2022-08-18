import cloudinary
import cloudinary.uploader
import cloudinary.api
import pyrebase
import json

#cloudinary setup
cloudinary.config(
    cloud_name = 'personen',
    api_key = '431772985299319',
    api_secret = 'fqUEX3GFsUcqMtObHXGzOwtQqwY', 
    secure = True
)

#firebase setup
firebaseConfig = {"apiKey": "AIzaSyAZAeWgkHoF4pqCPARjdRR6-xd7_KwwPz4",
  "authDomain": "database-personen.firebaseapp.com",
  "databaseURL": "https://database-personen-default-rtdb.europe-west1.firebasedatabase.app",
  "projectId": "database-personen",
  "storageBucket": "database-personen.appspot.com",
  "messagingSenderId": "923455214562",
  "appId": "1:923455214562:web:20daf65f425eaed4849fbb",
  "measurementId": "G-NRPGJ0DKS7"
  }

firebase = pyrebase.initialize_app(firebaseConfig)
firebase_db = firebase.database()



def upload(file, name):  
  response = cloudinary.uploader.upload(file,
      folder = "personen/" + name + "/")
  url = response['url']

  download = firebase_db.child(name).get()
  pics = download.val()

  if(pics != None):
    if(pics != ["x"]):
      pics.append(url)
    else:
      pics = [url]
    firebase_db.child(name).set(pics)


def delete(url, name):
  db_download = firebase_db.child(name).get()
  pics = db_download.val()
  badPic = url.split("/", 7)[-1].split(".")[0]
  
  if(len(pics) != 1):
    pics.remove(url)
  else:
    pics = ["x"]
  firebase_db.child(name).set(pics)
  cloudinary.uploader.destroy(badPic)

def download(name):
  download = firebase_db.child(name).get()
  pics = download.val()
  if(pics == ["x"]):
    return []
  else:
    return pics

def createUser(name):
  if(name != ""):
    data = ["x"]
    download = firebase_db.child(name).get().val()
    if(type(download) != list):
      firebase_db.child(name).set(data)
      print("User added")
    else:
      print("User already exists")
