import firebase_admin
from firebase_admin import credentials, firestore
from .settings import settings

def initialize_firebase():
    try:
        firebase_admin.get_app()
    
    except ValueError as e:
        cred = credentials.Certificate(settings.FIREBASE_SERVICE_ACCOUNT_KEY)
        firebase_admin.initialize_app(cred)

    return firestore.client()

db = initialize_firebase()