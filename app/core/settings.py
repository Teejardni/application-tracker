# app/core/settings.py
from pydantic_settings import BaseSettings
from pathlib import Path
from pydantic import ConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    debug: bool = True
    sqlite_path: str = str(BASE_DIR / "data" / "app.db")

    model_config = ConfigDict(
        env_file = ".env",
        case_sensitive = False
        )

settings = Settings()

