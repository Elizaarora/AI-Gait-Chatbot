from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from typing import Optional

class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    gemini_api_key: str
    firebase_db_url: str
    firebase_service_account: str = "firebase_service.json"
    port: int = 8000
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding='utf-8',
        case_sensitive=False,
        extra='ignore'
    )

@lru_cache()
def get_settings():
    """Cache settings to avoid reloading .env file multiple times"""
    try:
        return Settings()
    except Exception as e:
        print(f"❌ Error loading settings: {e}")
        print("Make sure your .env file has:")
        print("  - GEMINI_API_KEY=your_key_here")
        print("  - FIREBASE_DB_URL=your_firebase_url")
        print("  - FIREBASE_SERVICE_ACCOUNT=firebase_service.json")
        raise