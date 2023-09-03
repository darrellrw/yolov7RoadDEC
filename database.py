import firebase_admin
from firebase_admin import credentials, firestore, storage

import argparse

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {'storageBucket': 'roadeh-f6915.appspot.com'})

def run():
    if opt.push:
        db = firestore.client()
        db.collection("detections").add({"latitude": opt.ltd, "longitude": opt.lng, "path": opt.path, "date": opt.date, "time": opt.time})
        print("Hallo")

    if opt.upload:
        bucket = storage.bucket()
        blob = bucket.blob(opt.fileName)
        blob.upload_from_filename(opt.fileName)

        blob.make_public()

        print(blob.public_url)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ltd', type=str, default='test')
    parser.add_argument('--lng', type=str, default='test')
    parser.add_argument('--path', type=str, default='test')
    parser.add_argument('--date', type=str, default='test')
    parser.add_argument('--time', type=str, default='test')
    parser.add_argument('--fileName', type=str, default='test')
    parser.add_argument('--push', action='store_true', help='push data to firebase')
    parser.add_argument('--upload', action='store_true', help='upload imgae to firebase storage')
    opt = parser.parse_args()
    print(opt)