from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGO_URL: str
    DATABASE_NAME: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    GCS_BUCKET_NAME: str
    GCS_PROJECT_ID: str
    GCS_PRIVATE_KEY: str
    GCS_CLIENT_EMAIL: str
    GCS_CLIENT_ID: str
    GCS_TOKEN_URI: str
    GEMINI_API_KEY: str
    class Config:
        env_file = ".env"

settings = Settings()