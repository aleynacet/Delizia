import firebase_admin
from firebase_admin import credentials, firestore

# Firebase-Initialisierung
cred = credentials.Certificate('delizia-cc6d1-48416a047928.json') # Der Pfad zu Ihrer Firebase-JSON-Datei
firebase_admin.initialize_app(cred)
db = firestore.client()

def save_data_to_firestore(data):
    for business in data['businesses']:
        doc_ref = db.collection('yelpBusinesses').document(business['id'])
        doc_ref.set(business)

# Beispielaufruf
if __name__ == '__main__':
    from yelp_api import fetch_yelp_data

    yelp_data = fetch_yelp_data('restaurants', 'Berlin', 'korean', 15000)
    save_data_to_firestore(yelp_data)
    print("Data saved to Firestore.")
