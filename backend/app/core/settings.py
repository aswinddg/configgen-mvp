from pydantic_settings import BaseSettings
import os
from pathlib import Path

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./configgen.db"
    # Subir 4 niveles desde backend/app/core/settings.py para llegar a la raíz del proyecto
    TEMPLATE_DIR: str = str(Path(__file__).parent.parent.parent.parent / "templates")

    class Config:
        env_file = ".env"

settings = Settings()