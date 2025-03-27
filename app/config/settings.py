from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    FIREBASE_SERVICE_ACCOUNT_KEY: str = "desa-digital-6c62c-firebase-adminsdk-dw3k1-cfdcfa90b8.json"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()