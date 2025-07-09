import firebase_admin
import os
from firebase_admin import credentials, firestore
from .settings import settings


def initialize_firebase():
    try:
        firebase_admin.get_app()

    except ValueError:
        cred = credentials.Certificate(settings.FIREBASE_SERVICE_ACCOUNT_KEY)
        firebase_admin.initialize_app(cred)

        if settings.APP_ENV == "development" and settings.use_firebase_emulator:
            # Set environment variables for emulator
            os.environ["FIREBASE_PROJECT_ID"] = settings.firebase_project_id
            print(f"Using Firebase project ID: {settings.firebase_project_id}")

            os.environ["FIRESTORE_EMULATOR_HOST"] = settings.firestore_emulator_host
            print(f"🔥 Using Firestore emulator at {settings.firestore_emulator_host}")

    return firestore.client()


db = initialize_firebase()
