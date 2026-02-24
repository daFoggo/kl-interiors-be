from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    database_url: str = "postgresql://postgres:postgres@db:5432/app_db"
    
    # JWT Configs
    jwt_secret_key: str = "supersecret-jwt-key-replace-in-production"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 10080
    jwt_refresh_token_expire_minutes: int = 43200

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding='utf-8', 
        extra='ignore'
    )

settings = Settings()
