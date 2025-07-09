import firebase_admin
import os
import json
import base64
from firebase_admin import credentials, firestore
from .settings import settings


def initialize_firebase():
    try:
        firebase_admin.get_app()
    except ValueError:
        try:
            encoded_key = settings.FIREBASE_SERVICE_ACCOUNT_B64
            if not encoded_key:
                raise ValueError("Kredensial Base64 tidak ditemukan.")
            decoded_key = base64.b64decode(encoded_key).decode('utf-8')
            cred_json = json.loads(decoded_key)
            cred = credentials.Certificate(cred_json)
            print("✅ Firebase initialized from Base64 variable.")

        except (ValueError, TypeError):
            # PRIORITAS 2: Kembali ke file (untuk development lokal)
            print("Kredensial Base64 gagal, mencoba dari file lokal...")
            cred = credentials.Certificate(settings.FIREBASE_SERVICE_ACCOUNT_KEY)
            print("✅ Firebase initialized from local file.")

        firebase_admin.initialize_app(cred)

        if settings.APP_ENV == "development" and settings.use_firebase_emulator:
            # Set environment variables for emulator
            os.environ["FIREBASE_PROJECT_ID"] = settings.firebase_project_id
            print(f"Using Firebase project ID: {settings.firebase_project_id}")

            os.environ["FIRESTORE_EMULATOR_HOST"] = settings.firestore_emulator_host
            print(f"🔥 Using Firestore emulator at {settings.firestore_emulator_host}")

    return firestore.client()


db = initialize_firebase()
