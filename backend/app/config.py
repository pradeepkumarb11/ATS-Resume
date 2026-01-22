import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./test.db"
    OPENROUTER_API_KEY: str = ""
    OPENROUTER_MODEL: str = "deepseek/deepseek-chat"
    APP_URL: str = "http://localhost:8501"
    REQUEST_TIMEOUT: int = 120

    class Config:
        env_file = ".env"

settings = Settings()
