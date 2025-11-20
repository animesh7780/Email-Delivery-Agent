from pydantic_settings import BaseSettings
from typing import Optional
import os
from pathlib import Path

# Get the project root directory (parent of backend folder)
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"


class Settings(BaseSettings):
    gemini_api_key: str
    gemini_model: str = "gemini-1.5-flash"
    database_url: str = "sqlite:///./email_agent.db"
    host: str = "0.0.0.0"
    port: int = 8000
    
    class Config:
        env_file = str(ENV_FILE)
        case_sensitive = False


settings = Settings()
