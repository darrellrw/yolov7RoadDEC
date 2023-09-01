import firebase_admin
from firebase_admin import credentials, firestore, storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {'storageBucket': 'roadeh-f6915.appspot.com'})

def push(ltd, lng, path, date, time):
    db = firestore.client()
    db.collection("detections").add({"latitude": ltd, "longitude": lng, "path": path, "date": date, "time": time})

def upload(fileName):
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)

    blob.make_public()

    return blob.public_url