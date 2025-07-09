from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):

    APP_ENV: str = "prod"
    FIREBASE_SERVICE_ACCOUNT_B64: Optional[str] = None
    FIREBASE_SERVICE_ACCOUNT_KEY: Optional[str] = (
        "desa-digital-prod-firebase-adminsdk-fbsvc-1cf3138571.json"
    )
    firebase_apikey: str
    firebase_auth_domain: str
    firebase_project_id: str
    firebase_storage_bucket: str
    firebase_message_sender_id: str
    firebase_app_id: str

    use_firebase_emulator: bool = False
    firestore_emulator_host: str = "localhost:8080"
    auth_emulator_host: str = "localhost:9099"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"  # Menghindari error jika ada variabel ekstra di .env


settings = Settings()
