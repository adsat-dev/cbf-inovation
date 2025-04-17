from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    FIREBASE_SERVICE_ACCOUNT_KEY: str = (
        "desa-digital-6c62c-firebase-adminsdk-dw3k1-cfdcfa90b8.json"
    )
    firebase_apikey: str
    firebase_auth_domain: str
    firebase_project_id: str
    firebase_storage_bucket: str
    firebase_message_sender_id: str
    firebase_app_id: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"  # Menghindari error jika ada variabel ekstra di .env


settings = Settings()
