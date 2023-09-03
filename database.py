import firebase_admin
from firebase_admin import credentials, firestore, storage

import csv
import argparse

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {'storageBucket': 'roadeh-f6915.appspot.com'})

def run():
    with open(opt.path, "r") as file:
        csvreader = csv.reader(file)
        for row in csvreader:

            bucket = storage.bucket()
            blob = bucket.blob(row[5])
            blob.upload_from_filename(row[5])
            blob.make_public()

            db = firestore.client()
            db.collection("detections").add({"latitude": row[3], "longitude": row[2], "path": row[4], "date": row[0], "time": row[1]})

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, default='~')
    opt = parser.parse_args()
    run()