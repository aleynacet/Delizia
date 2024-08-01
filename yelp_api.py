import requests
import firebase_admin
from firebase_admin import credentials, firestore
import os
 
# Yelp API Key
API_KEY = 'CO4SfZLlBTHcBcCv7n1Jl0C2H92Yh3ycI9edHOOh3ClgwnWBTlZ1Dfxk1rI_Tc4KAoehowI4W6MwJPEVzhrPFkQuTPrYHUM8_VhwZ6bEh4ES0Sf4dCuefFqTKICnZnYx'
BASE_URL = 'https://api.yelp.com/v3/businesses/search'
 
# prüft ob der Pfad zur Firebase-JSON-Datei korrekt ist
path = 'delizia-cc6d1-6ffb26f4fbba.json'
 
if os.path.exists(path):
    print("Der Pfad ist korrekt.")
else:
    print("Der Pfad ist nicht korrekt.")
 
# initialisiert Firebase
cred = credentials.Certificate('delizia-cc6d1-6ffb26f4fbba.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
 
def search(term, location, categories, radius, offset=0):
    headers = {
        'Authorization': f'Bearer {API_KEY}'
    }
    params = {
        'term': term,
        'location': location,
        'categories': categories,
        'radius': radius,
        'limit': 1,  # limitiert die Anzahl der Ergebnisse auf 1
        'offset': offset  # damit wir verschiedene Ergebnisse erhalten
    }
    response = requests.get(BASE_URL, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        if 'businesses' in data and len(data['businesses']) > 0:
            business = data['businesses'][0]
            save_to_firestore('yelp_businesses', business['id'], business)
            print(f"Business {business['name']} saved to Firestore.")
        else:
            print("No businesses found.")
    else:
        raise Exception(f'Yelp API request failed with status code {response.status_code}')
 
def save_to_firestore(collection_name, document_id, data):
    doc_ref = db.collection(collection_name).document(document_id)
    doc_ref.set(data)
    print(f'Data saved to {collection_name}/{document_id}')
 
if __name__ == '__main__':
    for i in range(15):  # Holt 15 verschiedene restaurants in Berlin
        search('restaurants', 'Berlin', 'japanese', 15000, offset=i)
# Hier haben wir auch andere Kategorien eingesetzt, wie z.B. 'vegan', 'italian', 'asian'